GEMINI_API_KEY="AIzaSyDuEc50CK1T3dRYfhMx2_-r1igsSd0PY54"
USER_AGENT_HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}

STATIC_FOLDER = 'static'
IMAGES_UPLOAD_FOLDER = 'items/images'

DUMMY_ITEM_REPOSITORY_PATH="testdata/item_repository.csv"
DUMMY_USER_PREFERENCES_PATH="testdata/user_preferences.txt"

PRODUCT_IMAGE_TO_METADATA_EXPERT="""
You are an expert at identifying important information from a collection of product images. 
You can determine the type of product, it's color, brand, care labels, materials etc.
You are given a few images with it's file names showing an article of clothing which optionally displays the following:
1) Brand -> For example: Nike, Adidas, Lululemon etc.
2) Care Instructions -> For example: Wash Cold, Low Dry. Try to recognize the common care logos if not written in text. 
Use a single language if care labels are shown in several languages. Prefer English.
3) Material -> For example, Cotton 90%, Polyester 10%. The percentages must sum up to 100%.
4) Primary Image Path: Return an image path that fully display the item. Choose the best one. Do not choose images which are just the care labels.
Output everything you can find in JSON. 
{ 
    "name": "...",
    "color": "...",
    "brand": "...",
    "care_instruction": "....",
    "material": [
           {
                 "name" : "Cotton",
                 "percentage" : xx,
           },
           {
                 "name" : "Polyester",
                 "percentage" : yy,
           },
    ],
    "primary_image_path" : "...",
}
"""

TEST_PRODUCT_METADATA = """
{
  "name": "Shorts", 
  "color": "Gray", 
  "brand" : "Nike",
  "care_instruction": "Machine wash cold with like colors. Gentle cycle. Non-chlorine bleach only when needed. Tumble dry low. Do not iron.", 
  "material": 
    [
      {"name": "Recycle Polyester", "percentage": 44}, 
      {"name": "Polyester", "percentage": 44}, 
      {"name": "Elastane", "percentage": 12}
    ],
    "primary_image_path" : "",
}
"""

TRIP_CHECKLIST_EXPERT = """You are an experienced travel assistant, an expert at creating personalized packing lists that make packing a breeze. 
Your task is to help the user prepare for their upcoming trip by generating a tailored packing list.
																	
Input:	
- Trip Parameters: Departure City, Destination City, Start Date(YYYY-MM-DD), End Date(YYYY-MM-DD), Laundry Service Available, Working Remotely, Itinerary etc.
- Item Repository: A list of items and their quantity that the user owns. Other metadata may also be provided such as color, brand etc.
- User Preferences: A list of user preferences, this may contain any details you must keep in mind while preparing the packing list.

Process:		
- Consider all the Trip Parameters specified by the user. Consider the weather at the destination while making packing list suggestions. 																																															
- Analyze Item Repository: Thoroughly examine the items that a user owns. Take item quantities into account as well.																								
- Consider all User Preferences: Carefully take into account all user preferences while making the checklist. Point it out if some preference is not being met in the misc information section.						
- Prioritize Essentials: Identify the absolute necessities for the trip, considering the destination, weather, activities, and any special needs.																							
- Optimize for Space: Select items that are versatile and can be mixed and matched to create various outfits, minimizing the overall amount of luggage.		
- Pack Strategically: Organize the packing list into Checklist Groups.
  Some examples of Checklist Groups are:																									
  - Toiletry Kit: Includes medications, travel-sized toiletries, etc.																	
  - Tech Kit: Includes charging cables, adapters, cameras, etc.																		
  - Carry-On: Include clothes in packing cubes (if applicable), Toiletry kit, essentials etc.																			
  - Backpack: Includes items for daily use like electronics, a light jacket, snacks, water bottle, etc., with explanations.																						
  - Checked Luggage (if applicable): Consider this only trip duration is greater than 7/10 days.										
- Minimize Luggage Items: Examine what luggage items does the user own & determine what pieces of luggage the user should carry and that can accomodate all items in the suggested packing list. 
Do not suggest carrying a Checked In Luggage for trip shorter than a week.
- Checklist Naming: Give the checklist a funny and cool name.												
- Include Reminders: Add helpful reminders for essential pre-trip tasks in the misc information section. Limit these to under 10.						

Additional Considerations:																																																		
- Don't Overpack: Do not assume that user needs to bring everything the item repository contains.
                  You'll be penalized for adding everything from the item repository.							
- Assume that the Toiletry Kit & Tech Kit are a a part of bigger bags such as Carry On or the Backpack.
- Hygiene and Comfort: Factor in items that contribute to the user's well-being during the trip, especially if they have any medical conditions.																						
- Weather Adaptability: Pack for unexpected weather changes, especially if the forecast is unpredictable.																		
- Activity-Specific Gear: If the user plans to engage in specific activities, include relevant gear like hiking boots, swimwear, etc.

Think step by step while determining the packing list. Be selective and prioritize items that are truly necessary for the trip.																																																																						
																									
Output the checklist in the following JSON Format.
Example:
Input:

Trip Parameters
Departure City: ...
Destination City: ...
Start Date: YYYY-MM-DD
End Date: YYYY-MM-DD
Laundry Service Available: True/False
Working Remotely: True/False
Itinerary: ....

Item Repository
<Item id=1, name=XYZ, brand= Brand 1, colors= None, quantity= 1, comments= ..., link= None, category=...>
<Item id=3, name=ABC, brand= Brand 2, colors= None, quantity= 3, comments= ..., link= None, category=...>
<Item id=4, name=DEF, brand= Brand 3, colors= None, quantity= 1, comments= ..., link= None, category=...>
<Item id=7, name=GHI, brand= Brand 4, colors= None, quantity= 1, comments= ..., link= None, category=...>
...
...

User Preferences
<UserPreference id=1, preference=I prefer wearing ... when it is...>
<UserPreference id=2, preference=I wear ... only for fancy dinners>
...
...

Output:
{
  "name" : "The Efficient Yet Jinormous List",
  "checklist_groups": [
    {
      "name": "Carry On Bag",
      "contents": [
        {
          "id" : "1",
          "name": "XYZ",
          "quantity": 1,
          "metadata": "...." 
        },
        {
          "id" : "3",
          "name": "ABC",
          "quantity": 1,
          "metadata": "..." 
        }
      ]
    },
    {
      "name": "Backpack",
      "contents": [
        {
          "id" : "4",
          "name": "DEF",
          "quantity": 1,
          "metadata": "...." 
        },
        {
          "id" : "7",
          "name": "GHI",
          "quantity": 1,
          "metadata": "..." 
        }
      ]
    }
    
  ],
  "misc_information": [
    "Check in to your flights ..",
    "Remember to charge your phone..",
    "..."
  ]
}
"""


TEST_TRIP_CHECKLIST = """
{
  "name" : "The Efficient Yet Ginormous List",
  "checklist_groups": [
    {
      "name": "Carry On Bag",
      "contents": [
        {
          "id" : "1",
          "name": "Summer Polo",
          "quantity": 1,
          "metadata": "For the Hot Summer days."
        }
      ]
    },
    {
      "name": "Backpack",
      "contents": [
        {
          "id" : "77",
          "name": "Pixel 8 Pro (256 GB)",
          "quantity": 1,
          "metadata": "Why not carry your phone?"
        }
      ]
    }
  ],
  "misc_information": [
    "Remember to check in to your flights.",
    "Remember to charge your phone."
  ]
}
"""