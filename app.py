from flask import Flask
from constants import DUMMY_ITEM_REPOSITORY_PATH, DUMMY_USER_PREFERENCES_PATH, IMAGES_UPLOAD_FOLDER, STATIC_FOLDER
from item_repository_utils import csv_to_dict
from datetime import datetime
import os
import shutil
import subprocess
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from models import *

# Configure Flask App.
app = Flask(__name__)
app.config['STATIC_FOLDER'] = STATIC_FOLDER
app.config['IMAGES_UPLOAD_FOLDER'] = IMAGES_UPLOAD_FOLDER
os.makedirs(IMAGES_UPLOAD_FOLDER, exist_ok=True)

# Configure SQL Alchemy.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

# Configure Flask-Login.
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Configure Celery.
from celery import Celery, Task

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

# Register all the blueprints.
from routes import item_repository_bp, trip_manager_bp, user_preferences_bp, auth_blueprint_bp, index
app.register_blueprint(item_repository_bp)
app.register_blueprint(trip_manager_bp)
app.register_blueprint(user_preferences_bp)
app.register_blueprint(auth_blueprint_bp)

from flags import *

#### Dummy Data ####
def populate_database():
    db.drop_all()
    db.create_all()

    # Clear all files recursively under static.
    for root, _ , files in os.walk(app.config['STATIC_FOLDER']):
        for file in files:
            if file != "homepage.png":
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

# Create the database tables.
with app.app_context():
    if RE_INIT_DB:
        populate_database()

#### Default Route ####
@app.route('/', methods=['GET', 'POST'])
def home():
    return index()

if __name__ == '__main__':
    subprocess.Popen(['brew', 'services', 'restart', 'redis'])
    app.run(debug=True)
