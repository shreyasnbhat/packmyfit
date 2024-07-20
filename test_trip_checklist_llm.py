from llms import TripChecklistExpert
from constants import GEMINI_API_KEY

def generate_trip_checklist():
  trip_checklist_expert = TripChecklistExpert(api_key=GEMINI_API_KEY, testing = True)

  trip_prompt = """
Trip Parameters
Departure City: San Jose
Destination City: Boston
Start Date: 2024-06-10
End Date: 2024-06-14
Laundry Service Available: True
Working Remotely: True
Itinerary: Sleeping & Snoring
"""
  item_repository = []
  user_preferences = []

  trip_checklist = trip_checklist_expert.generate_trip_checklist(item_repository, user_preferences, trip_prompt)
  print(trip_checklist)

if __name__ == "__main__":
  generate_trip_checklist()