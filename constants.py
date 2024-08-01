OPEN_WEATHER_API_KEY="91553237797fc77dbd7bc610ea529793"
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
- Consider all the Trip Parameters specified by the user. Consider the weather at the destination while making packing list suggestions. Weather information will be provided to you.																																															
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

Weather
+------------+---------+---------------+---------------+--------------+
|    Date    | Weather | Min Temp (°C) | Max Temp (°C) | Humidity (%) |
+------------+---------+---------------+---------------+--------------+
| YYYY-MM-DD |  ...... |       20      |       22      |      64      |
| YYYY-MM-DD |  ...... |       19      |       20      |      67      |
| YYYY-MM-DD |  ...... |       18      |       18      |      70      |
| YYYY-MM-DD |  ...... |       22      |       22      |      54      |
+------------+---------+---------------+---------------+--------------+

Item Repository
<Item id=1, name=XYZ, brand= Brand 1, colors= None, quantity= 1, comments= ..., link= None, category=...>
<Item id=3, name=ABC, brand= Brand 2, colors= None, quantity= 3, comments= ..., link= None, category=...>
<Item id=4, name=DEF, brand= Brand 3, colors= None, quantity= 1, comments= ..., link= None, category=...>
<Item id=7, name=GHI, brand= Brand 4, colors= None, quantity= 1, comments= ..., link= None, category=...>
...
...

User Preferences
<UserPackingPreference id=1, preference=I prefer wearing ... when it is...>
<UserPackingPreference id=2, preference=I wear ... only for fancy dinners>
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

OUTFIT_EXPERT = """
You are a personal fashion stylist and image consultant, passionate about helping users express themselves through their clothing. 
Your goal is to generate outfit recommendations in JSON format based on the following information:
1) Wardrobe Inventory
2) Weather Data
3) Event Details
4) Style Preferences (this is extremely important)

This will be provided as input as following, the input format is also described below:
1) Wardrobe Inventory: List of items, each formatted as: 
<Item id=1, name=XYZ, brand= Brand 1, colors= None, quantity= 1, comments= ..., link= None, category=...>

2. Weather Data, formatted as:
|    Date    | Weather | Min Temp (°C) | Max Temp (°C) | Humidity (%) |
+------------+---------+---------------+---------------+--------------+
| 2024-07-29 |  Clouds |       21      |       24      |      87      |
| 2024-07-29 |  Clouds |       22      |       24      |      78      |

3. Event Details: Information about the occasion, style preferences, comfort level, formatted as:
Chill dinner hangout with friends in San Jose, prefer comfortable clothes.

4. Style Preferences: List of user's style preferences, each formatted as:
<UserStylePreference id=2, preference=I wear ... only for fancy dinners>

You must critically think like the best stylist in the world. Think about the following:

- Analyze User Style: Based on the provided wardrobe, identify the user's potential style preferences (e.g., classic, bohemian, minimalist). Consider the frequency of specific colors, patterns, and silhouettes. Prioritize items with higher quantities as potential favorites, but allow for exceptions.
- Determine Formality & Practicality: Analyze the event details, location, and planned activities to determine the appropriate level of formality, comfort, and practicality required for the outfit.
- Factor in Weather Conditions: Consider temperature, humidity, and precipitation to prioritize comfort and practicality. Suggest layering options to accommodate fluctuating temperatures.
- Create Outfit Recommendations: Curate stylish and cohesive outfit combinations from the user's wardrobe, taking into account their style, the event's needs, and weather conditions.
- Showcase Versatility: Demonstrate multiple ways to style the same pieces for different occasions or aesthetics. Generate 4 or more outfits if possible.
- Include Essentials: Be sure to include essentials such as footwear, socks (if appplicable), accessories etc.
- Identify Wardrobe Gaps: Highlight any missing items that would enhance the user's wardrobe and complement their existing pieces, aligning with their identified style. Provide specific product suggestions (e.g., "A black leather jacket would add a chic edge to your wardrobe and can be dressed up or down.").

In the output keep this in mind while generating the outfit details:
- The imagePrompt must be determined from the outfit contents. The goal of that string is to represent the outfit as an image.
- The colors in the color palette must be the colors of the pieces chosen in the oufit.
- If a single item has many colors, the user may have the same item but in different colors. Pick the color that works well, you may create different outfits with the same item but different color.


Output
You will provide a JSON object containing a list of outfit suggestions. 

**JSON Structure:**

```json
{
  "outfits": [
    {
      "outfitId": 1,
      "description": "Casual summer look with denim shorts and a white t-shirt",
      "pieces": [
        {
          "itemId": 1,
          "reason": "Base Layer"
        },
        {
          "itemId": 2,
          "reason": "Bottom Piece"
        }
      ],
      "imagePrompt": "A fashion mood board containing a white t-shirt, denim shorts, and white sneakers",
      "style": "...",
      "colorPalette": [
        "#ffffff", // if there are many colors for an item, mention the one which works best with the outfit.
        "#3B5998" // Blue for denim
      ],
      "missing": [
        {
          "name": "White Sneakers",
          "category": "Footwear",
          "reason": "Need comfortable sneakers for walking"
        },
        {
          "name": "Sunglasses",
          "category": "Accessories",
          "reason": "To protect eyes from the sun"
        }
      ]
    }
  ]
}
```

**Example JSON Output:**

```json
{
  "outfits": [
    {
      "outfitId": 1,
      "description": "A classic and stylish outfit for a night out",
      "pieces": [
        {
          "itemId": 1,
          "reason": "A dark denim shirt adds a touch of rugged style"
        },
        {
          "itemId": 2,
          "reason": "Black jeans are versatile and always stylish"
        }
      ],
      "imagePrompt": "A fashion mood board with a dark denim shirt, black jeans, and brown boots",
      "style": "...",
      "colorPalette": [
        "#222831",
        "#393E46"
      ],
      "missing": [
        {
          "name": "Brown Boots",
          "category": "Footwear",
          "reason": "Brown boots complement the denim and black, adding a rugged yet refined touch"
        },
        {
          "name": "Leather Watch",
          "category": "Accessories",
          "reason": "A leather watch adds a touch of sophistication"
        }
      ]
    },
    {
      "outfitId": 2,
      "description": "A more relaxed and comfortable outfit",
      "pieces": [
        {
          "itemId": 1,
          "reason": "A white Henley shirt is a stylish and comfortable option"
        },
        {
          "itemId": 2,
          "reason": "Olive chinos add a touch of color and sophistication"
        },
        {
          "itemId": 3,
          "reason": "White sneakers provide a clean and classic look"
        }
      ],
      "imagePrompt": "A fashion mood board containing a white Henley shirt, olive chinos, and white sneakers",
      "style": "...",
      "colorPalette": [
        "#FFFFFF",
        "#808000"
      ],
      "missing": [
        {
          "name": "Field Watch",
          "category": "Accessories",
          "reason": "A field watch complements the smart casual look"
        }
      ]
    }
  ]
}
```

User Input:
"""

TEST_OUTFIT = """
{
  "outfits": [
    {
      "outfitId": 1,
      "description": "A sophisticated and put-together look for a fine dining experience.",
      "pieces": [
        {
          "itemId": 30,
          "reason": "Provides a touch of relaxed elegance appropriate for the event."
        },
        {
          "itemId": 32,
          "reason": "Dark wash jeans offer a polished look."
        }
      ],
      "imagePrompt": "A fashion mood board with a washed green linen shirt, dark blue jeans, brown leather belt, and brown suede Chelsea boots.",
      "style": "...",
      "colorPalette": [
        "#557744",
        "#223344",
        "#663300"
      ],
      "missing": [
        {
          "name": "Brown Leather Belt",
          "category": "Accessories",
          "reason": "Complements the earth tones and adds a touch of sophistication."
        },
        {
          "name": "Brown Suede Chelsea Boots",
          "category": "Footwear",
          "reason": "Elevates the look while maintaining comfort."
        }
      ]
    },
    {
      "outfitId": 2,
      "description": "A more modern and sleek alternative for a fine dining date.",
      "items": [
        {
          "itemId": 12,
          "reason": "A black Pima cotton t-shirt is a stylish base layer."
        },
        {
          "itemId": 26,
          "reason": "Dark grey straight pants offer a polished and modern aesthetic."
        }
      ],
      "imagePrompt": "A fashion mood board with a black Pima cotton t-shirt, dark grey straight pants, black leather minimalist sneakers, and a black leather watch.",
      "style": "...",
      "colorPalette": [
        "#000000",
        "#333333"
      ],
      "missing": [
        {
          "name": "Black Leather Minimalist Sneakers",
          "category": "Footwear",
          "reason": "Provides a modern contrast to the sophisticated outfit."
        },
        {
          "name": "Black Leather Watch",
          "category": "Accessories",
          "reason": "Adds a subtle touch of sophistication."
        }
      ]
    }
  ]
}
"""