from llms import OutfitExpert
from constants import GEMINI_API_KEY

def generate_outfits():
  outfit_expert = OutfitExpert(api_key=GEMINI_API_KEY, testing=True)

  wardrobe_inventory = [
    "<Item id=1, name=Summer Polo, brand= All In Motion, colors= Navy, quantity= 1, comments= None, link= None, category=Clothes>",
    "<Item id=2, name=SuperSoft Lounge Pants, brand= Pair of Thieves, colors= Black, quantity= 2, comments= None, link= https://pairofthieves.com/products/off-duty-lounge-pant-supersoft-lounge-pant-2, category=Clothes>"
  ]

  user_style_preferences = [
    "Like to wear oversized T-Shirts",
    "Prefer wearing Allbirds Loungers for chill social hangs with friends"
  ]
  event_details = "Fine Dine dinner with friends."
  weather_data = """|    Date    | Weather | Min Temp (°C) | Max Temp (°C) | Humidity (%) |
+------------+---------+---------------+---------------+--------------+
| 2024-07-29 |  Clouds |       21      |       24      |      87      |
| 2024-07-29 |  Clouds |       22      |       24      |      78      |
"""

  outfits = outfit_expert.generate_outfits(wardrobe_inventory,
                         user_style_preferences,
                         event_details,
                         weather_data)

if __name__ == "__main__":
  generate_outfits()