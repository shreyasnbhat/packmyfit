# item_repository_models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class TripChecklistMiscInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trip_checklist_id = db.Column(db.Integer, db.ForeignKey('trip_checklist.id', ondelete='CASCADE', use_alter=True), nullable=False)
    misc_information = db.Column(db.String(512), nullable=False)

# Defines a single checklist item.
class TripChecklistItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trip_checklist_group_id = db.Column(db.Integer, db.ForeignKey('trip_checklist_group.id', ondelete='CASCADE', use_alter=True), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    item_metadata = db.Column(db.String(255), nullable=True)
    quantity = db.Column(db.Integer, nullable=True)
    
    def __repr__(self):
        return f'<TripChecklistItem id={self.id}, item_id={self.item_id}, quantity={self.quantity}>'

# Defined a logical checklist group within a single checklist. For example: Carry On Bag, Toiletry Kit etc.
class TripChecklistGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trip_checklist_id = db.Column(db.Integer, db.ForeignKey('trip_checklist.id', ondelete='CASCADE', use_alter=True), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    items = db.relationship('TripChecklistItem', cascade="all, delete-orphan", backref='trip_checklist_group_items', lazy=True)

# Define the TripChecklist model.
class TripChecklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id', ondelete='CASCADE', use_alter=True), nullable=False)
    name = db.Column(db.String(255), nullable=True)
    creation_timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    checklist_groups = db.relationship('TripChecklistGroup', cascade="all, delete-orphan", backref='trip_checklist_checklist_groups', lazy=True)
    misc_information = db.relationship('TripChecklistMiscInformation', cascade="all, delete-orphan", backref='trip_checklist_misc_information', lazy=True)

    def __repr__(self):
        return f'<TripChecklist id={self.id}, trip_id={self.trip_id}, creation_timestamp={self.creation_timestamp}>'

# Define the Trip model.
class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', use_alter=True), nullable=False)
    departure_city = db.Column(db.String(255), nullable=False)
    destination_city = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    laundry_service_available = db.Column(db.Boolean, nullable=False)
    working_remotely = db.Column(db.Boolean, nullable=False)
    itinerary = db.Column(db.Text, nullable=True)
    misc_information = db.Column(db.Text, nullable=True)

    checklists = db.relationship('TripChecklist', cascade="all, delete-orphan", backref='trip_checklists', lazy=True)

    def __repr__(self):
        return f"""
Trip Parameters
Departure City: {self.departure_city}
Destination City: {self.destination_city}
Start Date: {self.start_date}
End Date: {self.end_date}
Laundry Service Available: {self.laundry_service_available}
Working Remotely: {self.working_remotely}
Itinerary: {self.itinerary}
"""
    
class ItemImage(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id', ondelete='CASCADE', use_alter=True))
    path = db.Column(db.String(1024), nullable=False)

    def __repr__(self):
        return f'<ItemImage id={self.id}, item_id={self.item_id}, path={self.path}>'

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', use_alter=True), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    brand = db.Column(db.String(255), nullable=False)
    colors = db.Column(db.String(255), nullable=True)
    quantity = db.Column(db.Integer, nullable=True)
    care_instruction = db.Column(db.String(255), nullable=True)
    material = db.Column(db.String(255), nullable=True)
    comments = db.Column(db.Text, nullable=True)
    link = db.Column(db.String(255), nullable=True)
    category = db.Column(db.String(255), nullable=False)
    images = db.relationship("ItemImage", backref="item_images", cascade="all, delete-orphan", single_parent=True, foreign_keys=[ItemImage.item_id], lazy=True)

    # Reference a primary image id.
    primary_image_id = db.Column(db.Integer, db.ForeignKey('item_image.id'), nullable=True)

    def __repr__(self):
        return f'<Item id={self.id}, name={self.name}, brand= {self.brand}, colors= {self.colors}, quantity= {self.quantity}, comments= {self.comments}, link= {self.link}, category={self.category}>'

class UserPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    preference = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<UserPreference id={self.id}, preference={self.preference}>'

# Define the User model.
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    display_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    items = db.relationship('Item', cascade="all, delete-orphan", backref='user_items', lazy=True, foreign_keys=[Item.user_id])
    trips = db.relationship('Trip', cascade="all, delete-orphan", backref='uses_trips', lazy=True, foreign_keys=[Trip.user_id])
    preferences = db.relationship('UserPreference', backref='users_preferences', lazy=True)

    def __repr__(self):
        return f'<User id={self.id}, username={self.username}, email={self.email}>'