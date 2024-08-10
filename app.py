from flask import Flask
from constants import DUMMY_ITEM_REPOSITORY_PATH, DUMMY_USER_PREFERENCES_PATH, IMAGES_UPLOAD_FOLDER, STATIC_FOLDER
from utils import item_repository_csv_to_json
from datetime import datetime, timedelta
import os
import shutil
import json
from utils import resize_image_to_target
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
from routes import item_repository_bp, trip_manager_bp, outfit_manager_bp, user_preferences_bp, auth_blueprint_bp, index, weather_forecast
app.register_blueprint(item_repository_bp)
app.register_blueprint(trip_manager_bp)
app.register_blueprint(outfit_manager_bp)
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
            if file not in ["homepage.jpg", "hanger-icon.svg", "checklist.svg", "inventory.svg", "gemini.svg"]:
                os.remove(os.path.join(root, file))
        
    # Add a Dummy User.
    dummy_user = User(username='testuser', display_name="Beta Broski", email='betabroski@gmail.com', password=generate_password_hash('1234', method='pbkdf2'))
    db.session.add(dummy_user)
    db.session.flush()

    # Add Dummy User's Item Repository.
    dummy_item_repository_data = item_repository_csv_to_json(DUMMY_ITEM_REPOSITORY_PATH)
    
    items = []
    for dummy_item_data in dummy_item_repository_data:
        new_item = Item(
            name=dummy_item_data['Name'],
            brand=dummy_item_data['Brand'],
            colors=dummy_item_data['Colors'],
            quantity=dummy_item_data['Quantity'],
            comments=dummy_item_data['Comments'],
            link=dummy_item_data['Link'],
            category=dummy_item_data['Category'],
        )
        items.append(new_item)
        dummy_user.items.append(new_item)
    db.session.add_all(items)

    # Add Dummy User's Preferences.
    with open(DUMMY_USER_PREFERENCES_PATH, 'r') as user_preferences_file:
        dummy_user.packing_preferences = [UserPackingPreference(preference=line.strip()) for line in user_preferences_file]

    # Add a Dummy Trip.
    dummy_trip = Trip(
        user_id = dummy_user.id,
        departure_city="San Jose",
        destination_city="New York",
        start_date=(datetime.now() + timedelta(days=1)).date(),  # Start date is tomorrow
        end_date=(datetime.now() + timedelta(days=5)).date(),  # End date is 4 days from tomorrow
        laundry_service_available=False,
        working_remotely=False,
        purpose="City Break",
        weather=json.dumps(weather_forecast.get_forecast_data_daily(city="New York")),
        itinerary="Day 1: Sightseeing, Day 2: Sightseeing, Day 3: Sightseeing",
    )
    db.session.add(dummy_trip)
    dummy_user.trips.append(dummy_trip)

    # Add a Dummy Event.
    event_date = datetime.now() + timedelta(days=1)
    dummy_event1 = Event(
        user_id=dummy_user.id,
        city="San Jose",
        datetime=event_date,
        description="Hiking Trip",
        weather=json.dumps(weather_forecast.get_forecast_data_hourly(city="San Jose", date_filter=event_date.date()))
    )
    dummy_event2 = Event(
        user_id=dummy_user.id,
        city="San Jose",
        datetime=event_date,
        description="Fine Dining with friends",
        weather=json.dumps(weather_forecast.get_forecast_data_hourly(city="San Jose", date_filter=event_date.date()))
    )
    dummy_user.events.append(dummy_event1)
    dummy_user.events.append(dummy_event2)
    db.session.commit()

    dummy_user_id = dummy_user.id
    image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp", ".avif"]
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

            # Downsize the image and save it efficiently.
            with open(item_image_dst_path, "rb") as item_image_file:
                item_image_data = item_image_file.read()
                resized_item_image_data = resize_image_to_target(item_image_data)
                if resized_item_image_data:
                    resized_item_image_data.save(item_image_dst_path)
                    # Update ItemImage DB Object.
                    dummy_item_with_images.images.append(ItemImage(item_id = dummy_item_id,
                                                                   path=os.path.join(item_image_db_basepath, item_image_dst_filename)))

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
    app.run(debug=True)
