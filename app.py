from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash
from llms import TripChecklistExpert, ProductImageToMetadataExpert
from constants import GEMINI_API_KEY, DUMMY_ITEM_REPOSITORY_PATH, DUMMY_USER_PREFERENCES_PATH, IMAGES_UPLOAD_FOLDER
from item_repository_utils import csv_to_dict
from datetime import datetime
import os
import shutil
import json
import re
import subprocess
from celery import Celery, Task
from utils import generate_item_image_id
from flask_sqlalchemy import SQLAlchemy
from collections import defaultdict
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import * # Import all models

ENABLE_CELERY=False

app = Flask(__name__)

# Configure Celery.
def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://localhost:6379",
        result_backend="redis://localhost:6379",
        task_ignore_result=True,
    ),
)
celery_app = celery_init_app(app)

# Configure SQL Alchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['STATIC_FOLDER'] = 'static'
db.init_app(app)

# Configure Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Image Folder Setup
app.config['IMAGES_UPLOAD_FOLDER'] = IMAGES_UPLOAD_FOLDER
os.makedirs(IMAGES_UPLOAD_FOLDER, exist_ok=True)

# Flask Blueprint Setup
item_repository_bp = Blueprint('item_repository', __name__, 
                               url_prefix='/item_repository')
trip_manager_bp = Blueprint('trip_manager', __name__, 
                            url_prefix='/trip_manager')
user_preferences_bp = Blueprint('user_preferences', __name__, 
                                url_prefix='/user_preferences')

# Expert Setup
trip_checklist_expert = TripChecklistExpert(api_key=GEMINI_API_KEY, testing=False)
product_image_to_metadata_expert = ProductImageToMetadataExpert(api_key=GEMINI_API_KEY, testing=False)

# Define all Celery Tasks.
from celery_tasks import generate_product_metadata

def populate_database():
    db.drop_all()
    db.create_all()

    # Clear all files recursively under static.
    for root, _ , files in os.walk(app.config['STATIC_FOLDER']):
        for file in files:
            os.remove(os.path.join(root, file))
        
    # Add a Dummy User.
    dummy_user = User(username='testuser', display_name="Beta Broski", email='betabroski@gmail.com', password=generate_password_hash('1234', method='pbkdf2'))
    db.session.add(dummy_user)
    db.session.flush()

    # Add Dummy User's Item Repository.
    dummy_item_repository = csv_to_dict(DUMMY_ITEM_REPOSITORY_PATH)
    items = []  # Store items to add in a single transaction
    for category, item_list in dummy_item_repository.items():
        for item_data in item_list:
            new_item = Item(
                name=item_data['Name'],
                brand=item_data['Brand'],
                colors=item_data['Colors'],
                quantity=item_data['Quantity'],
                comments=item_data['Comments'],
                link=item_data['Link'],
                category=category,
            )
            items.append(new_item)
            dummy_user.items.append(new_item)
    db.session.add_all(items)

    # Add Dummy User's Preferences.
    with open(DUMMY_USER_PREFERENCES_PATH, 'r') as user_preferences_file:
        dummy_user.preferences = [UserPreference(preference=line.strip()) for line in user_preferences_file]

    # Add a Dummy Trip.
    dummy_trip = Trip(
        user_id = dummy_user.id,
        departure_city="San Jose",
        destination_city="New York",
        start_date=datetime.strptime("2024-07-02", '%Y-%m-%d').date(),
        end_date=datetime.strptime("2024-07-06", '%Y-%m-%d').date(),
        laundry_service_available=False,
        working_remotely=False,
        itinerary="Day 1: Sightseeing, Day 2: Sightseeing, Day 3: Sightseeing",
        misc_information=""
    )
    db.session.add(dummy_trip)
    dummy_user.trips.append(dummy_trip)
    db.session.commit()

    dummy_user_id = dummy_user.id
    image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif"]
    for dummy_item_id in range(1, 100):
        dummy_item_with_images = db.session.get(Item, dummy_item_id)

        # Create ItemImage objects directly and append to the item's images list
        # TODO(shbhat): Create functions for this path wrangling.
        item_id_dir = f"""testdata/user_{dummy_user_id}_item_{dummy_item_id}/"""
        item_image_src_paths = [os.path.join(item_id_dir, filename) for filename in os.listdir(item_id_dir) 
                                 if filename.lower().endswith(tuple(image_extensions))]
        item_image_db_basepath = os.path.join(app.config['IMAGES_UPLOAD_FOLDER'], f"""user_{dummy_user_id}""")
        item_image_dst_basepath = os.path.join(app.config['STATIC_FOLDER'], item_image_db_basepath)
        for idx, item_image_src_path in enumerate(item_image_src_paths):
            item_image_dst_filename = f"""item_{dummy_item_id}_image_{idx + 1}_""" + os.path.basename(item_image_src_path)
            item_image_dst_path = os.path.join(item_image_dst_basepath, item_image_dst_filename)
            
            # Copy the image from source to destination.
            os.makedirs(os.path.dirname(item_image_dst_path), exist_ok=True)
            shutil.copy(item_image_src_path, item_image_dst_path)
            
            # Update ItemImage DB Object.
            dummy_item_with_images.images.append(ItemImage(item_id = dummy_item_id,path=os.path.join(item_image_db_basepath, item_image_dst_filename)))

    # Commit the changes to the database.
    db.session.commit()

def get_image_path_from_item_image_id(item_image_id):
    image_path = None
    if item_image_id:
        item_image = db.session.get(ItemImage, item_image_id)
        if item_image:
            image_path = item_image.path
    return image_path

# Create the database tables.
with app.app_context():
    populate_database()
    pass

##### Trip Manager Routes #####
@trip_manager_bp.route('/', methods=['GET', 'POST'])
@login_required
def trips():
    if request.method == 'POST':
        departure_city = request.form['departure_city']
        destination_city = request.form['destination_city']
        start_date_str = request.form['start_date']  # Get the date string
        end_date_str = request.form['end_date']  # Get the date string
        laundry_service_available = request.form['laundry_service_available'] == 'yes'
        working_remotely = request.form['working_remotely'] == 'yes'
        itinerary = request.form['itinerary']

        # Convert date strings to datetime objects
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        # Generate trip object and add it to the list of trips.
        trip = Trip(
            user_id = current_user.id,
            departure_city=departure_city,
            destination_city=destination_city,
            start_date=start_date,
            end_date=end_date,
            laundry_service_available=laundry_service_available,
            working_remotely=working_remotely,
            itinerary=itinerary,
            misc_information=""
        )
        current_user.trips.append(trip)        
        db.session.commit()

    return render_template('trip_manager_main.html', trips=current_user.trips)

@trip_manager_bp.route('/trip_id:<int:trip_id>', methods=['GET'])
@login_required
def trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    trip_checklists = db.session.query(TripChecklist).filter_by(trip_id=trip_id).order_by(TripChecklist.creation_timestamp.desc()).all()

    checklists = []
    for _, trip_checklist in enumerate(trip_checklists):
        checklists.append({
            "name" : trip_checklist.name,
            "checklist_groups" : [],
            "misc_information": []
        })
        for checklist_group in trip_checklist.checklist_groups:
            checklists[-1]["checklist_groups"].append({
                "name" : checklist_group.name,
                "contents" : []
            })
            for checklist_item in checklist_group.items:
                item = db.session.query(Item).filter_by(id=checklist_item.item_id).first()
                checklists[-1]["checklist_groups"][-1]["contents"].append({
                    "id": item.id,
                    "name" : item.name,
                    "quantity" : checklist_item.quantity,
                    "metadata" : checklist_item.item_metadata
                })
        for misc_info in trip_checklist.misc_information:
            checklists[-1]["misc_information"].append(misc_info.misc_information)
    print(checklists)
    return render_template('trip_display.html', trip=trip, checklists=checklists)

@trip_manager_bp.route('/delete/trip_id:<int:trip_id>', methods=['POST'])
@login_required
def delete_trip(trip_id):
    trip = db.session.get(Trip, trip_id)

    if trip:
        if trip.user_id != current_user.id:
            flash('You are not authorized to delete this trip.', 'danger')
            return redirect(url_for('trip_manager.trips'))

        try:
            db.session.delete(trip)
            db.session.commit()  # Commit changes here
            db.session.refresh(current_user)
            flash('Trip deleted successfully.', 'success') 
        except Exception as e:
            db.session.rollback()
            flash(f'Error deleting trip: {e}', 'danger')
    else:
        flash('Trip not found.', 'danger')

    return redirect(url_for('trip_manager.trips'))

@trip_manager_bp.route('/trip_id:<int:trip_id>/gen_checklist', methods=['POST'])
@login_required
def gen_checklist(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    
    # Query and format the User Item Repository.
    item_repository = []
    for item in current_user.items:
        item_repository.append(str(item))
    
    # Query and format the User Preferences.
    user_preferences = []
    for preference in current_user.preferences:
        user_preferences.append(str(preference))

    expert_result = trip_checklist_expert.generate_trip_checklist(item_repository=item_repository,
                                                                    user_preferences=user_preferences,
                                                                    trip_prompt=str(trip))
    # Store the generated checklist.
    generated_trip_checklist = TripChecklist(
        trip_id=trip_id,
        name=expert_result["name"],
    )
    db.session.add(generated_trip_checklist)
    db.session.flush()

    # Fill Misc Information.
    for expert_result_misc_info in expert_result["misc_information"]:
        generated_misc_info = TripChecklistMiscInformation(
            trip_checklist_id=generated_trip_checklist.id,
            misc_information=expert_result_misc_info
        )
        db.session.add(generated_misc_info)
        generated_trip_checklist.misc_information.append(generated_misc_info)
        
    # Fill Trip Checklist Groups.
    for expert_result_checklist_group in expert_result["checklist_groups"]:
        generated_trip_checklist_group = TripChecklistGroup(
            trip_checklist_id=generated_trip_checklist.id,
            name=expert_result_checklist_group["name"]
        )
        db.session.add(generated_trip_checklist_group)
        db.session.flush()
        
        # Fill Trip Checklist Items.
        for expert_result_checklist_item in expert_result_checklist_group["contents"]:
            generated_checklist_item = TripChecklistItem(item_id=expert_result_checklist_item["id"], 
                                                trip_checklist_group_id=generated_trip_checklist_group.id,
                                                item_metadata=expert_result_checklist_item["metadata"],
                                                quantity=expert_result_checklist_item["quantity"])
            db.session.add(generated_checklist_item)
            generated_trip_checklist_group.items.append(generated_checklist_item)    
        generated_trip_checklist.checklist_groups.append(generated_trip_checklist_group)
    
    db.session.add(generated_trip_checklist)
    db.session.commit()
    return redirect(url_for('trip_manager.trip', trip_id=trip_id))


@trip_manager_bp.route('/trip_id:<int:trip_id>/checklists/checklist_id:<int:checklist_id>', methods=['GET', 'POST'])
@login_required
def checklist(trip_id, checklist_id):
    pass


##### Item Repository Routes #####
@item_repository_bp.route('/', methods=['GET', 'POST'])
@login_required
def items():
    items = current_user.items
    category_to_items = defaultdict(list)
    if request.method == 'POST':
        # Get form data
        category = request.form['category']
        name = request.form['name']
        brand = request.form['brand']
        colors = request.form['colors']
        quantity = request.form['quantity']
        comments = request.form['comments']
        care_instruction = request.form['care_instructions']
        images = request.files.getlist('images')

        # Create a new Item object and save it to the database
        user_item = Item(
            user_id=current_user.id,
            category=category,
            name=name,
            brand=brand,
            colors=colors,
            quantity=quantity,
            comments=comments,
            care_instruction=care_instruction,
        )
        db.session.add(user_item)
        db.session.flush()

        # Save uploaded images
        user_item_id = user_item.id

        for image in images:
            if image.filename == '':
                flash('No selected file!')
                continue  # Skip to the next file if no file is selected
            filename = image.filename
            filepath = os.path.join(app.config['IMAGES_UPLOAD_FOLDER'], "user_" + str(current_user.id), "image_" + generate_item_image_id() + "_" + filename)
            static_filepath = os.path.join(app.config['STATIC_FOLDER'], filepath)
            os.makedirs(os.path.dirname(static_filepath), exist_ok=True)
            image.save(static_filepath)

            # Create ItemImage DB Object.
            item_image = ItemImage(
                item_id=user_item.id,
                path=filepath
            )
            db.session.add(item_image)
            user_item.images.append(item_image)

        db.session.commit()
        flash('Item added successfully!')
        return redirect(url_for('item_repository.items'))
    else:
        for item in items:
            primary_image_path = get_image_path_from_item_image_id(item_image_id=item.primary_image_id)
            if primary_image_path is None and len(item.images) > 0:
                primary_image_path = item.images[0].path
            category_to_items[item.category].append({
                'name': item.name,
                'brand': item.brand,
                'colors': item.colors,
                'quantity': item.quantity,
                'comments': item.comments,
                'link': item.link,
                'id': item.id,
                'images': [image.path for image in item.images],
                'primary_image' : primary_image_path
            })
    return render_template('item_repository_main.html', category_to_items=category_to_items)

@item_repository_bp.route('/item_id:<int:item_id>', methods=['GET'])
@login_required
def item(item_id):
    item_repository_item = Item.query.get_or_404(item_id)
    materials = item_repository_item.material
    if materials is not None:
        materials = json.loads(materials)
    primary_item_image_path = get_image_path_from_item_image_id(item_image_id=item_repository_item.primary_image_id)

    return render_template('item_display.html', 
                           item=item_repository_item,
                           primary_image_path=primary_item_image_path,
                           metadata=None,
                           materials=materials)

@item_repository_bp.route('/item_id:<int:item_id>/upload_image', methods=['POST'])
@login_required
def item_image_upload(item_id):
    user_id = current_user.id
    if request.method == 'POST':
        # Check if the post request has the file part.
        if 'image' not in request.files:
            flash('No file part!')
            return redirect(request.url)
        file = request.files['image']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file!')
            return redirect(request.url)
        if file:
            # Create ItemImage DB Object.
            item_image = ItemImage(
                item_id = item_id,
                path="temp"
            )
            db.session.add(item_image)
            db.session.flush()

            filepath = os.path.join(app.config['IMAGES_UPLOAD_FOLDER'], "user_" + str(user_id), "image_" + str(item_image.id) + "_"+ file.filename)
            static_filepath = os.path.join(app.config['STATIC_FOLDER'], filepath)
            os.makedirs(os.path.dirname(static_filepath), exist_ok=True)
            file.save(static_filepath)

            # Update item's list of image file paths.
            item_image.path = filepath            
            item = Item.query.get_or_404(item_id)
            item.images.append(item_image)
            db.session.commit()
            flash('File uploaded successfully!')
    return redirect(url_for('item_repository.item', item_id = item_id))

@item_repository_bp.route('/item_id:<int:item_id>/gen_metadata', methods=['GET', 'POST'])
@login_required
def item_generate_metadata(item_id):
    item = db.session.get(Item, item_id)
    if request.method == 'POST':
        expert_result = {}
        if not ENABLE_CELERY:
            # Call the product metadata expert and render item_repository_item with the resulting json.
            item_image_paths = [os.path.join(app.config['STATIC_FOLDER'], image.path) for image in item.images]
            expert_result = product_image_to_metadata_expert.generate_product_metadata(image_paths=item_image_paths)
        else:
            # Call the Celery task to generate metadata asynchronously.
            generate_product_metadata.delay(item_id)

        # LLM already sees the images.        
        if "brand" in expert_result and expert_result["brand"] is not None:
            item.brand = expert_result["brand"]
        if "care_instruction" in expert_result:
            item.care_instruction = expert_result["care_instruction"]
        if "material" in expert_result:
            item.material = json.dumps(expert_result["material"])
        if "primary_image_path" in expert_result:
            primary_image_path = re.sub(r"^static/", "", expert_result["primary_image_path"])
            primary_item_image = ItemImage.query.filter_by(path=primary_image_path).first()
            if primary_item_image:
                item.primary_image_id = primary_item_image.id
            else:
                print(f"Warning: Could not find ItemImage with path {primary_image_path}")

        if not ENABLE_CELERY:
            db.session.add(item)
            db.session.commit()

    return redirect(url_for('item_repository.item', item_id=item_id))

##### User Preference Routes #####
@user_preferences_bp.route('/', methods=['GET', 'POST'])
@login_required
def user_preferences():
    if request.method == 'POST':
        new_preference = request.form.get('new_preference')
        if new_preference:
            current_user.preferences.append(UserPreference(user_id=current_user.id, preference=new_preference))
            db.session.commit()
        return redirect(url_for('user_preferences.user_preferences'))
    else:
        # Display the user's preferences
        preferences = [preference.preference for preference in current_user.preferences]
        return render_template('user_preferences.html', preferences=preferences)

#### User Signup & Login Routes ####
# Define to routes.
@app.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        return redirect(url_for('item_repository.items'))
    else:
        return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('item_repository.items'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('login'))
        else:
            flash('Invalid username or password.')
    else:
        users = User.query.all()
        usernames = [user.username for user in users]
        return render_template('login.html', usernames=usernames)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('item_repository.items'))
    if request.method == 'POST':
        username = request.form['username']
        display_name = request.form['display_name']
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.')
            return redirect(url_for('signup'))
        new_user = User(username=username, display_name=display_name, email=email, password=generate_password_hash(password, method='pbkdf2'))
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully. Please log in.')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('home'))

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

app.register_blueprint(item_repository_bp)
app.register_blueprint(trip_manager_bp)
app.register_blueprint(user_preferences_bp)

if __name__ == '__main__':
    subprocess.Popen(['brew', 'services', 'restart', 'redis'])
    app.run(debug=False)
