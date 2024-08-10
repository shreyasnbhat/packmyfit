OPEN_WEATHER_API_KEY="91553237797fc77dbd7bc610ea529793"
GEMINI_API_KEY="AIzaSyDuEc50CK1T3dRYfhMx2_-r1igsSd0PY54"
USER_AGENT_HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}

STATIC_FOLDER = 'static'
IMAGES_UPLOAD_FOLDER = 'items/images'

DUMMY_ITEM_REPOSITORY_PATH="testdata/item_repository.csv"
DUMMY_USER_PREFERENCES_PATH="testdata/user_preferences.txt"

DEFAULT_CITY="San Jose"

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

TRIP_ITINERARY_EXPERT = """
You are an expert travel planner, known for crafting unique and memorable itineraries. Your goal is to create a detailed, day-by-day travel itinerary, formatted as a structured JSON object, for a trip, considering the provided trip parameters.

Inputs:

1. Trip Parameters: Basic information about the trip, formatted as follows:
   ```
   Departure City: ...
   Destination City: ...
   Start Date: YYYY-MM-DD
   End Date: YYYY-MM-DD
   Laundry Service Available: True/False
   Working Remotely: True/False
   ```

Itinerary Generation Process:

1. Research the Destination:
   - Gather comprehensive information about the destination city, including popular attractions, hidden gems, local customs, transportation options, and average costs.
   - Leverage online resources, travel blogs, and reviews to identify unique and authentic experiences.

2. Tailor to User Preferences:
   - Carefully analyze the user's preferences to understand their travel style, interests, and priorities.
   - Prioritize activities and experiences that align with their stated preferences.
   - Consider their budget level and suggest suitable options accordingly.
   - Factor in their desired pace of travel to create a balanced itinerary with a mix of activities and downtime.

3. Structure the Itinerary:
   - Create a day-by-day itinerary within a JSON object. Each day should be a key (e.g., "Day 1", "Day 2") with its value being an array of activity objects.
   - Each activity object should include:
      - `time`: (e.g., "9:00 AM - 12:00 PM")
      - `activity`: (e.g., "Explore Central Park")
      - `description`: (Brief description of the activity)
      - `address`: (Address of the location)
      - `duration`: (Estimated duration)
      - `transportation`: (Suggested transportation method)
      - `cost`: (Approximate cost)

4. Incorporate Practical Considerations:
   - Account for laundry needs based on the "laundryServiceAvailable" parameter, suggesting laundromats or laundry services if needed within the relevant day's activities.
   - If "workingRemotely" is true, allocate time for work and suggest cafes or coworking spaces with reliable Wi-Fi within the relevant day's activities.
   - Provide alternative activity suggestions in case of unexpected weather conditions.

5. Add Value with Insider Tips:
   - Offer valuable insights and tips to enhance the user's experience, such as:
     - Recommendations for local restaurants or hidden culinary gems.
     - Tips for navigating public transportation or finding the best deals.
     - Insights into local customs or etiquette.
     - Suggestions for off-peak hours to visit popular attractions. Include these tips within the relevant activity's description.

Output Format Example (JSON only)
{
  "Day 1": [
    {
      "time": "9:00 AM - 12:00 PM",
      "activity": "Explore Central Park",
      "description": "Start your day with a stroll through this iconic green space...",
      "address": "Central Park, New York, NY",
      "duration": "2-3 hours",
      "transportation": "Walk / Public Transportation",
      "cost": "Free"
    },
    {
      "time": "12:00 PM - 1:00 PM",
      "activity": "Lunch at [Restaurant Name]",
      "description": "[Brief description of the restaurant and cuisine type]",
      "address": "[Address]",
      "duration": "1 hour",
      "transportation": "Walk",
      "cost": "$15-20"
    },
    { 
      "time": "1:00 PM - 4:00 PM",
      "activity": "[Activity]",
      "description": "...",
      "address": "[Address]",
      "duration": "...",
      "transportation": "...",
      "cost": "..." 
    }
  ],
  "Day 2": [
    {
      "time": "...",
      "activity": "...",
      "description": "...",
      "address": "...",
      "duration": "...",
      "transportation": "...",
      "cost": "..."
    }
  ]
}
"""

TEST_TRIP_ITINERARY="""
{
  "Day 1: 2023-08-08": [
    {
      "time": "Morning",
      "activity": "Arrive in Seattle and Check-in",
      "description": "Arrive at Seattle-Tacoma International Airport (SEA), pick up your rental car, and check into your hotel in the downtown area. Consider staying near Pike Place Market for easy access to attractions.",
      "address": "Seattle-Tacoma International Airport (SEA), Seattle, WA",
      "duration": "2-3 hours",
      "transportation": "Airplane, Rental Car",
      "cost": "Varies depending on flight and rental car costs"
    },
    {
      "time": "Lunch",
      "activity": "Lunch at Pike Place Market",
      "description": "Enjoy the vibrant atmosphere and fresh seafood at Pike Place Market. Try the famous fish throwing, sample local produce, and grab lunch at one of the many food stalls.",
      "address": "Pike Place Market, Seattle, WA",
      "duration": "1-2 hours",
      "transportation": "Walk",
      "cost": "$15-25"
    },
    {
      "time": "Afternoon",
      "activity": "Explore Pike Place Market and Waterfront",
      "description": "Spend the afternoon exploring the various stalls and shops at Pike Place Market. Afterwards, take a walk along the waterfront and enjoy views of Elliott Bay.",
      "address": "Pike Place Market & Seattle Waterfront, Seattle, WA",
      "duration": "2-3 hours",
      "transportation": "Walk",
      "cost": "Free (except for any purchases)"
    },
    {
      "time": "Evening",
      "activity": "Dinner at a Local Restaurant",
      "description": "Choose from a variety of restaurants in the downtown area for dinner. Consider trying Ivar's Seafood Bar for a classic Seattle seafood experience.",
      "address": "Various Restaurants, Seattle, WA",
      "duration": "1-2 hours",
      "transportation": "Walk",
      "cost": "$20-40"
    }
  ],
  "Day 2: 2023-08-09": [
    {
      "time": "Morning",
      "activity": "Visit the Space Needle",
      "description": "Head to the iconic Space Needle for panoramic views of the city, Puget Sound, and the surrounding mountains.",
      "address": "Space Needle, Seattle, WA",
      "duration": "2-3 hours",
      "transportation": "Walk or Public Transportation",
      "cost": "$35-40"
    },
    {
      "time": "Lunch",
      "activity": "Lunch in the Seattle Center",
      "description": "Grab lunch at one of the many restaurants or cafes in the Seattle Center, home to the Space Needle and other attractions.",
      "address": "Seattle Center, Seattle, WA",
      "duration": "1-2 hours",
      "transportation": "Walk",
      "cost": "$15-25"
    },
    {
      "time": "Afternoon",
      "activity": "Explore the Museum of Pop Culture (MoPOP)",
      "description": "Immerse yourself in the world of popular music, science fiction, and pop culture at the Museum of Pop Culture (MoPOP).",
      "address": "Museum of Pop Culture (MoPOP), Seattle, WA",
      "duration": "2-3 hours",
      "transportation": "Walk",
      "cost": "$30"
    },
    {
      "time": "Evening",
      "activity": "Dinner and Drinks in Belltown",
      "description": "Enjoy dinner and drinks in the trendy Belltown neighborhood, known for its vibrant nightlife and diverse dining options.",
      "address": "Various Restaurants and Bars, Belltown, Seattle, WA",
      "duration": "2-3 hours",
      "transportation": "Walk or Public Transportation",
      "cost": "$30-50"
    }
  ],
  "Day 3: 2023-08-10": [
    {
      "time": "Morning",
      "activity": "Visit Kerry Park for City Views",
      "description": "Start your day with breathtaking views of the Seattle skyline, Space Needle, and Mount Rainier from Kerry Park.",
      "address": "Kerry Park, Seattle, WA",
      "duration": "1-2 hours",
      "transportation": "Rental Car or Rideshare",
      "cost": "Free"
    },
    {
      "time": "Late Morning",
      "activity": "Explore the Fremont Troll",
      "description": "Visit the quirky Fremont Troll sculpture under the Aurora Bridge and explore the eclectic Fremont neighborhood.",
      "address": "Fremont Troll, Seattle, WA",
      "duration": "1-2 hours",
      "transportation": "Rental Car or Rideshare",
      "cost": "Free"
    },
    {
      "time": "Lunch",
      "activity": "Lunch in Fremont",
      "description": "Enjoy lunch at one of the many restaurants or cafes in Fremont, known for its bohemian vibe and diverse culinary scene.",
      "address": "Various Restaurants and Cafes, Fremont, Seattle, WA",
      "duration": "1-2 hours",
      "transportation": "Walk",
      "cost": "$15-25"
    },
    {
      "time": "Afternoon",
      "activity": "Depart from Seattle",
      "description": "Head back to Seattle-Tacoma International Airport (SEA) to catch your flight back to San Jose.",
      "address": "Seattle-Tacoma International Airport (SEA), Seattle, WA",
      "duration": "2-3 hours",
      "transportation": "Rental Car",
      "cost": "Varies depending on flight costs"
    }
  ]
}
"""


TRIP_CHECKLIST_EXPERT = """You are an experienced travel assistant, an expert at creating personalized packing lists that make packing a breeze. 
Your task is to help the user prepare for their upcoming trip by generating a tailored packing list.
																	
Input:	
- Trip Parameters: Departure City, Destination City, Start Date(YYYY-MM-DD), End Date(YYYY-MM-DD), Laundry Service Available, Working Remotely, Itinerary etc.
- Item Repository: A list of items and their quantity that the user owns. Other metadata may also be provided such as color, brand etc.
- User Preferences: A list of user preferences, this may contain any details you must keep in mind while preparing the packing list.

Process:		
- Consider all the Trip Parameters specified by the user. Keep the trip itinerary in mind as well.
- Consider the weather at the destination while making packing list suggestions. Weather information will be provided to you.																																															
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
Purpose: ...
Itinerary: ....

Weather
+------------+---------+---------------+---------------+--------------+
|    Date    | Weather | Min Temp (°C) | Max Temp (°C) | Humidity (%) |
+------------+---------+---------------+---------------+--------------+
| 2024-08-07 |   Rain  |    [19, 20]   |    [21, 21]   |   [84, 88]   |
| 2024-08-08 |  Clouds |    [20, 23]   |    [21, 23]   |   [78, 88]   |
| 2024-08-09 |   Rain  |    [23, 27]   |    [23, 27]   |   [76, 93]   |
| 2024-08-10 |  Clear  |    [21, 30]   |    [21, 30]   |   [33, 91]   |
| 2024-08-11 |  Clear  |    [20, 28]   |    [20, 28]   |   [32, 51]   |
| 2024-08-12 |  Clear  |    [22, 30]   |    [22, 30]   |   [33, 53]   |
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
You are a personal fashion stylist and image consultant, passionate about helping users express themselves through their clothing, with an expert understanding of current trends and timeless style principles. 
Your goal is to generate outfit recommendations in JSON format based on the provided user information, thoughtfully curated to suit their individual needs and preferences.

**Inputs:**

You will receive the following information as input:

1. **Wardrobe Inventory:** A detailed list of the user's clothing items, each formatted as: 
   `<Item id=1, name=XYZ, brand= Brand 1, colors= None, quantity= 1, comments= ..., link= None, category=...>`

2. **Weather Data:** Current and upcoming weather conditions for the event location, formatted as a table:
   ```
   +------------+-------+---------+---------------+---------------+--------------+
   |    Date    |  Time | Weather | Min Temp (°C) | Max Temp (°C) | Humidity (%) |
   +------------+-------+---------+---------------+---------------+--------------+
   | 2024-08-07 | 20:00 |  Clouds |       19      |       21      |      88      |
   | 2024-08-07 | 23:00 |   Rain  |       20      |       21      |      84      |
   | 2024-08-08 | 02:00 |   Rain  |       20      |       21      |      82      |
   ```

3. **Event Details:** Information about the occasion, including the location, time of day, planned activities, and any specific dress code or style preferences, formatted as a concise description:
   `Chill dinner hangout with friends in San Jose, prefer comfortable clothes.`

4. **Style Preferences:** Explicit statements from the user about their personal style preferences, each formatted as:
   `<UserStylePreference id=2, preference=I wear ... only for fancy dinners>`


**Outfit Generation Process:**

1. **Deeply Analyze User Style:** 
    - Go beyond simply identifying basic style categories (e.g., classic, bohemian).  
    - Deduce the user's preferred colors, fabrics, patterns, silhouettes, and brands based on their wardrobe inventory.
    - Pay close attention to item quantities, comments, and any provided links to understand their individual taste and potential favorite items.
    - Factor in the user's explicit style preferences to personalize the recommendations.

2. **Contextualize Event Requirements:**
    - Thoroughly analyze the event details to determine the appropriate level of formality and practicality. 
    - Consider the location, time of day, and activities to ensure the outfits are suitable and comfortable.

3. **Prioritize Weather Appropriateness:**
    - Carefully consider the weather data to ensure the outfits are comfortable and functional.
    - Suggest layering options for fluctuating temperatures or unpredictable weather.
    - Prioritize weather-resistant materials and appropriate footwear for rain or snow.

4. **Craft Cohesive and Stylish Outfits:**
    - Create well-balanced outfit combinations that showcase the user's personal style while adhering to event requirements and weather conditions.
    -  Consider color coordination, visual interest through texture and pattern mixing, and overall silhouette.

5. **Maximize Wardrobe Usage:**
    - Demonstrate the versatility of the user's existing wardrobe by showcasing multiple ways to style the same pieces for different occasions or aesthetics.
    - Aim to generate at least 4 diverse outfit suggestions, if possible, to provide a range of options.

6. **Complete the Look with Essentials:**
    - Don't forget to include essential items like footwear, accessories (jewelry, bags, belts, etc.), and outerwear as needed. These details are crucial for a polished and complete look.

7. **Identify Wardrobe Gaps:**
    - Act as a true stylist by identifying any missing items that would elevate the user's wardrobe and complement their existing pieces.
    - Offer specific product recommendations with justifications, considering the user's style and needs.
    - For example: `"A black leather jacket would add a chic edge to your wardrobe and can be dressed up or down."`

**Output:**

You will provide a JSON object containing a list of outfit suggestions, following the structure below.

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

**Important Notes for Output:**

- **imagePrompt:**  Construct the `imagePrompt` string to accurately represent the outfit for image generation purposes. Be descriptive and include all key pieces and their colors.
- **colorPalette:** Extract the main colors of the chosen pieces for the `colorPalette`. If an item has multiple colors, choose the most prominent one that works well with the outfit. You can create different outfits featuring the same item in different colors to showcase versatility.
- **Ensure Completeness and Accuracy:** Double-check the output to ensure all outfit details are complete, accurate, and well-formatted.
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