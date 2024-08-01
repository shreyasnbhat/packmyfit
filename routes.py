from flask import Blueprint

# Flask Blueprint Setup
item_repository_bp = Blueprint('item_repository', __name__, 
                               url_prefix='/item_repository')
trip_manager_bp = Blueprint('trip_manager', __name__, 
                            url_prefix='/trip_manager')
outfit_manager_bp = Blueprint('outfit_manager', __name__, 
                              url_prefix='/outfit_manager')
user_preferences_bp = Blueprint('user_preferences', __name__, 
                                url_prefix='/user_preferences')
auth_blueprint_bp = Blueprint('auth', __name__, url_prefix='/auth')

from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
import os
from constants import STATIC_FOLDER, IMAGES_UPLOAD_FOLDER
import json
import re
from utils import get_image_path_from_item_image_id, upload_item_images
from collections import defaultdict
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import *
from flags import *
from experts import *
from celery_tasks import generate_product_metadata
from weather_forecast import WeatherForecast

weather_forecast = WeatherForecast()

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

    return render_template('trip_manager_main.html', 
                           trips=current_user.trips)

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
    for preference in current_user.packing_preferences:
        user_preferences.append(str(preference))

    weather_data = weather_forecast.get_weather_data(trip.destination_city)
    expert_result = trip_checklist_expert.generate_trip_checklist(item_repository=item_repository,
                                                                    user_preferences=user_preferences,
                                                                    trip_prompt=str(trip),
                                                                    weather_data=weather_data)
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

##### Outfit Manager Routes #####
@outfit_manager_bp.route('/', methods=['GET', 'POST'])
@login_required
def events():
    """Handles creating new events."""
    if request.method == 'POST':
        event_details = request.form.get('event_details')
        city = request.form.get('city')
        date = request.form.get('date')
        time = request.form.get('time')

        if city is None:
            city = "San Francisco"  # Default City

        if not all([event_details, date, time]): 
            flash('Please provide Event Details, City, Date, and Time!', 'danger')
            return redirect(url_for('outfit_manager.events')) 

        try:
            # Combine date and time into a single datetime object.
            datetime_str = f"{date} {time}"
            event_datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
        except ValueError:
            flash('Invalid date or time format!', 'danger')
            return redirect(url_for('outfit_manager.events'))

        event = Event(description=event_details, city=city, datetime=event_datetime)
        current_user.events.append(event)
        db.session.add(event)
        db.session.commit()

        flash('Event created successfully!', 'success')
        return redirect(url_for('outfit_manager.event', event_id=event.id))

    return render_template("outfit_manager_main.html", events=current_user.events)

@outfit_manager_bp.route('/event_id:<int:event_id>', methods=['GET'])
@login_required
def event(event_id):
    event = db.session.get(Event, event_id)
    outfits_data = []
    for outfit in event.outfits:
        outfit_data = {
            'outfitId': outfit.id,
            'description': outfit.description,
            'pieces': [],  
            'imagePrompt': outfit.image_prompt,
            'style': outfit.style,
            'colorPalette': json.loads(outfit.color_palette) if outfit.color_palette else [], # Parse color_palette
            'missing': [{'name': missing_item.name, 'category': missing_item.category, 'reason': missing_item.reason} for missing_item in outfit.missing_items]
        }
        # Query the item details and substitute in the JSON
        outfit_data['pieces'] = [{'item': Item.query.get(outfit_item.item_id), 'reason': outfit_item.reason} for outfit_item in outfit.outfit_items]
        outfits_data.append(outfit_data)

    return render_template("outfit_display.html", event=event, outfits=outfits_data)

@outfit_manager_bp.route('/event_id:<int:event_id>/generate_outfits', methods=['POST'])
@login_required
def generate_outfits(event_id):
    event = db.session.get(Event, event_id)
    
    # Check weather at event city.
    weather_data = weather_forecast.get_weather_data(city=event.city)

    # Query the Item Repository to obtain the user's Wardrobe Inventory.
    wardrobe_inventory = [str(item) for item in current_user.items if item.category in ["Clothes", "Footwear"]]

    # Collect the user's style preferences.
    user_style_preferences = current_user.style_preferences

    # Query the expert to obtain the outfits.
    expert_result = outfit_expert.generate_outfits(wardrobe_inventory,
                        user_style_preferences,
                        event.description,
                        weather_data)
    
    # Delete all existing outfits that were generated for this event.
    try:
        outfits = db.session.query(Outfit).filter_by(event_id=event_id).all()
        for outfit in outfits:
            # Delete related OutfitItems.
            for outfit_item in outfit.outfit_items:
                db.session.delete(outfit_item)

            # Delete related MissingItems.
            for missing_item in outfit.missing_items:
                db.session.delete(missing_item)

            # Now delete the Outfit.
            db.session.delete(outfit)

        db.session.commit()
        flash('Outfits deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting outfits: {e}!', 'danger')

    # Save generated outfits.
    for outfit_data in expert_result['outfits']:
        outfit = Outfit(
            event_id=event_id,
            image_prompt=outfit_data['imagePrompt'],
            style=outfit_data['style'],
            color_palette=json.dumps(outfit_data['colorPalette']), # Store as JSON string
            description=outfit_data['description']
        )
        db.session.flush()  # To get the outfit.outfit_id

        for outfit_piece in outfit_data['pieces']:
            outfit_item = OutfitItem(
                outfit_id=outfit.id,
                item_id=outfit_piece['itemId'],
                reason=outfit_piece['reason']
            )
            outfit.outfit_items.append(outfit_item)

        for missing_item_data in outfit_data['missing']:
            missing_item = MissingItem(
                outfit_id=outfit.id,
                name=missing_item_data['name'],
                category=missing_item_data['category'],
                reason=missing_item_data.get('reason')  # 'reason' may not always be present
            )
            outfit.missing_items.append(missing_item)
        event.outfits.append(outfit) 
    db.session.commit()

    return redirect(url_for('outfit_manager.event', event_id=event.id))


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

        # Create a new Item object and save it to the database.
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
        user_item_id = user_item.id
        db.session.commit()

        status_codes = upload_item_images(db=db,
                           user_id=current_user.id,
                           item_id=user_item_id,
                           images=images)
        flash(f"Item Created w/ {status_codes['success']}/{status_codes['all']} images uploaded!")
        return redirect(url_for('item_repository.items'))
    else:
        for item in items:
            primary_image_path = get_image_path_from_item_image_id(db, item_image_id=item.primary_image_id)
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
    primary_item_image_path = get_image_path_from_item_image_id(db, item_image_id=item_repository_item.primary_image_id)

    return render_template('item_display.html', 
                           item=item_repository_item,
                           primary_image_path=primary_item_image_path,
                           metadata=None,
                           materials=materials)

@item_repository_bp.route('/item_id:<int:item_id>/upload_image', methods=['POST'])
@login_required
def item_image_upload(item_id):
    if request.method == 'POST':
        if 'images' not in request.files:
            flash('No file part!')
            return redirect(request.url)
        status_codes = upload_item_images(db=db,
                           user_id=current_user.id,
                           item_id=item_id,
                           images=request.files.getlist('images'))
        flash(f"Images Uploaded: {status_codes['success']}/{status_codes['all']}")

    return redirect(url_for('item_repository.item', item_id = item_id))

@item_repository_bp.route('/item_id:<int:item_id>/gen_metadata', methods=['GET', 'POST'])
@login_required
def item_generate_metadata(item_id):
    item = db.session.get(Item, item_id)
    if request.method == 'POST':
        expert_result = {}
        if not ENABLE_CELERY:
            # Call the product metadata expert and render item_repository_item with the resulting json.
            item_image_paths = [os.path.join(STATIC_FOLDER, image.path) for image in item.images]
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
        packing_preference = request.form.get('packing_preference')
        style_preference = request.form.get('style_preference')
        if packing_preference:
            current_user.packing_preferences.append(UserPackingPreference(user_id=current_user.id, preference=packing_preference))
            db.session.commit()
        if style_preference:
            current_user.style_preferences.append(UserStylePreference(user_id=current_user.id, preference=style_preference))
            db.session.commit() 
        return redirect(url_for('user_preferences.user_preferences'))
    else:
        # Display the user's preferences
        packing_preferences = [packing_preference.preference for packing_preference in current_user.packing_preferences]
        style_preferences = [style_preference.preference for style_preference in current_user.style_preferences]
        return render_template('user_preferences.html', packing_preferences=packing_preferences, style_preferences=style_preferences)

#### User Signup & Login Routes ####
@auth_blueprint_bp.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('auth.login'))
        else:
            flash('Invalid username or password.')
    else:
        users = User.query.all()
        usernames = [user.username for user in users]
        return render_template('login.html', usernames=usernames)

@auth_blueprint_bp.route('/signup', methods=['GET', 'POST'])
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
            return redirect(url_for('auth.signup'))
        new_user = User(username=username, display_name=display_name, email=email, password=generate_password_hash(password, method='pbkdf2'))
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully. Please log in.')
        return redirect(url_for('auth.login'))
    return render_template('signup.html')

@auth_blueprint_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return render_template('home.html')


#### Home Route Function ####
def index():
    if current_user.is_authenticated:
        return redirect(url_for('item_repository.items'))
    else:
        return render_template('home.html')