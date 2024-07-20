import unittest
from trip_checklist_models import db, TripChecklist, TripChecklistGroup, TripChecklistItem, Trip, User, Item, UserPreference, TripChecklistMiscInformation
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

class TripChecklistModelsTest(unittest.TestCase):

    def setUp(self):
        """Setup for the test cases."""
        self.engine = create_engine('sqlite:///:memory:')
        db.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def tearDown(self):
        """Cleanup after each test case."""
        self.session.close()
        db.metadata.drop_all(self.engine)

    def test_trip_checklist_creation(self):
        """Test creating a TripChecklist."""
        trip = Trip(user_id=1, departure_city='New York', destination_city='London', start_date=datetime(2024, 3, 10), end_date=datetime(2024, 3, 17), laundry_service_available=True, working_remotely=False)
        self.session.add(trip)
        self.session.commit()

        checklist = TripChecklist(trip_id=trip.id)
        self.session.add(checklist)
        self.session.commit()

        self.assertIsNotNone(checklist.id)
        self.assertEqual(checklist.trip_id, trip.id)

    def test_trip_checklist_group_creation(self):
        """Test creating a TripChecklistGroup."""
        trip = Trip(user_id=1, departure_city='New York', destination_city='London', start_date=datetime(2024, 3, 10), end_date=datetime(2024, 3, 17), laundry_service_available=True, working_remotely=False)
        self.session.add(trip)
        self.session.commit()

        checklist = TripChecklist(trip_id=trip.id)
        self.session.add(checklist)
        self.session.commit()

        group = TripChecklistGroup(trip_checklist_id=checklist.id, name='Carry-on Bag')
        self.session.add(group)
        self.session.commit()

        self.assertIsNotNone(group.id)
        self.assertEqual(group.trip_checklist_id, checklist.id)
        self.assertEqual(group.name, 'Carry-on Bag')

    def test_trip_checklist_item_creation(self):
        """Test creating a TripChecklistItem."""
        item = Item(user_id=1, name='Laptop', brand='Apple', category='Electronics')
        self.session.add(item)
        self.session.commit()

        trip = Trip(user_id=1, departure_city='New York', destination_city='London', start_date=datetime(2024, 3, 10), end_date=datetime(2024, 3, 17), laundry_service_available=True, working_remotely=False)
        self.session.add(trip)
        self.session.commit()

        checklist = TripChecklist(trip_id=trip.id)
        self.session.add(checklist)
        self.session.commit()

        group = TripChecklistGroup(trip_checklist_id=checklist.id, name='Electronics')
        self.session.add(group)
        self.session.commit()

        checklist_item = TripChecklistItem(trip_checklist_group_id=group.id, item_id=item.id, quantity=1)
        self.session.add(checklist_item)
        self.session.commit()

        self.assertIsNotNone(checklist_item.id)
        self.assertEqual(checklist_item.trip_checklist_group_id, group.id)
        self.assertEqual(checklist_item.item_id, item.id)
        self.assertEqual(checklist_item.quantity, 1)

    def test_trip_creation(self):
        """Test creating a Trip."""
        user = User(username='testuser', display_name='Test User', email='test@example.com', password='password')
        self.session.add(user)
        self.session.commit()

        trip = Trip(user_id=user.id, departure_city='New York', destination_city='London', start_date=datetime(2024, 3, 10), end_date=datetime(2024, 3, 17), laundry_service_available=True, working_remotely=False)
        self.session.add(trip)
        self.session.commit()

        self.assertIsNotNone(trip.id)
        self.assertEqual(trip.user_id, user.id)
        self.assertEqual(trip.departure_city, 'New York')
        self.assertEqual(trip.destination_city, 'London')
        self.assertEqual(trip.start_date, datetime(2024, 3, 10))
        self.assertEqual(trip.end_date, datetime(2024, 3, 17))
        self.assertTrue(trip.laundry_service_available)
        self.assertFalse(trip.working_remotely)

    def test_item_creation(self):
        """Test creating an Item."""
        user = User(username='testuser', display_name='Test User', email='test@example.com', password='password')
        self.session.add(user)
        self.session.commit()

        item = Item(user_id=user.id, name='Laptop', brand='Apple', category='Electronics')
        self.session.add(item)
        self.session.commit()

        self.assertIsNotNone(item.id)
        self.assertEqual(item.user_id, user.id)
        self.assertEqual(item.name, 'Laptop')
        self.assertEqual(item.brand, 'Apple')
        self.assertEqual(item.category, 'Electronics')

    def test_user_preference_creation(self):
        """Test creating a UserPreference."""
        user = User(username='testuser', display_name='Test User', email='test@example.com', password='password')
        self.session.add(user)
        self.session.commit()

        preference = UserPreference(user_id=user.id, preference='Carry-on Only')
        self.session.add(preference)
        self.session.commit()

        self.assertIsNotNone(preference.id)
        self.assertEqual(preference.user_id, user.id)
        self.assertEqual(preference.preference, 'Carry-on Only')

    def test_user_creation(self):
        """Test creating a User."""
        user = User(username='testuser', display_name='Test User', email='test@example.com', password='password')
        self.session.add(user)
        self.session.commit()

        self.assertIsNotNone(user.id)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.display_name, 'Test User')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.password, 'password')

    def test_trip_checklist_misc_information_creation(self):
        """Test creating a TripChecklistMiscInformation."""
        trip = Trip(user_id=1, departure_city='New York', destination_city='London', start_date=datetime(2024, 3, 10), end_date=datetime(2024, 3, 17), laundry_service_available=True, working_remotely=False)
        self.session.add(trip)
        self.session.commit()

        checklist = TripChecklist(trip_id=trip.id)
        self.session.add(checklist)
        self.session.commit()

        misc_info = TripChecklistMiscInformation(trip_checklist_id=checklist.id, misc_information='Important Notes: ...')
        self.session.add(misc_info)
        self.session.commit()

        self.assertIsNotNone(misc_info.id)
        self.assertEqual(misc_info.trip_checklist_id, checklist.id)
        self.assertEqual(misc_info.misc_information, 'Important Notes: ...')
