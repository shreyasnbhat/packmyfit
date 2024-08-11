import system_prompts
import api_keys
import testsdata_constants

# API Keys
OPEN_WEATHER_API_KEY=api_keys.OPEN_WEATHER_API_KEY
GEMINI_API_KEY=api_keys.GEMINI_API_KEY

USER_AGENT_HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}

STATIC_FOLDER = 'static'
IMAGES_UPLOAD_FOLDER = 'items/images'
DEFAULT_CITY="San Jose"

# Dummy dataset paths
DUMMY_TESTDATA_SRC_PATH=testsdata_constants.TESTDATA_SRC_FOLDER
DUMMY_ITEM_REPOSITORY_PATH=testsdata_constants.ITEM_REPOSITORY_PATH
DUMMY_USER_PREFERENCES_PATH=testsdata_constants.USER_PREFERENCES_PATH

# System prompts
PRODUCT_IMAGE_TO_METADATA_EXPERT = system_prompts.PRODUCT_IMAGE_TO_METADATA_EXPERT
TRIP_ITINERARY_EXPERT = system_prompts.TRIP_ITINERARY_EXPERT
TRIP_CHECKLIST_EXPERT = system_prompts.TRIP_CHECKLIST_EXPERT
OUTFIT_EXPERT = system_prompts.OUTFIT_EXPERT

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
    "primary_image_path" : ""
}
"""

TEST_TRIP_ITINERARY="""
{
  "Day 1: 2024-08-11": [
    {
      "time": "Morning",
      "activity": "Arrive in New York City & Check-in",
      "description": "Arrive at John F. Kennedy International Airport (JFK) or Newark Liberty International Airport (EWR). Take a taxi, ride-share, or public transportation to your hotel in Manhattan. Consider staying in Midtown or Lower Manhattan for easy access to attractions.",
      "address": "JFK Airport or EWR Airport, New York, NY",
      "duration": "2-3 hours",
      "transportation": "Airplane, Taxi, Ride-share, or Public Transportation",
      "cost": "Varies depending on flight and transportation costs"
    },
    {
      "time": "Lunch",
      "activity": "Lunch in Greenwich Village",
      "description": "Enjoy lunch in the charming Greenwich Village neighborhood. This area is known for its cozy cafes and diverse restaurants.",
      "address": "Greenwich Village, New York, NY",
      "duration": "1-2 hours",
      "transportation": "Subway or Walk",
      "cost": "$15-25"
    },
    {
      "time": "Afternoon",
      "activity": "Explore Washington Square Park",
      "description": "Relax and people-watch in Washington Square Park, a popular gathering place for locals and tourists. Enjoy street performers and the iconic arch.",
      "address": "Washington Square Park, New York, NY",
      "duration": "2-3 hours",
      "transportation": "Walk",
      "cost": "Free"
    },
    {
      "time": "Evening",
      "activity": "Dinner and a Broadway Show",
      "description": "Experience the magic of Broadway with a captivating performance. Have dinner before or after the show at one of the many restaurants in the Theater District.",
      "address": "Theater District, New York, NY",
      "duration": "4-5 hours",
      "transportation": "Subway or Walk",
      "cost": "$100-200 (depending on show and dinner choices)"
    }
  ],
  "Day 2: 2024-08-12": [
    {
      "time": "Morning",
      "activity": "Visit the Empire State Building",
      "description": "Ascend to the top of the Empire State Building for breathtaking panoramic views of New York City.",
      "address": "Empire State Building, New York, NY",
      "duration": "2-3 hours",
      "transportation": "Subway",
      "cost": "$40-50"
    },
    {
      "time": "Lunch",
      "activity": "Lunch near Bryant Park",
      "description": "Enjoy lunch at one of the many restaurants or food stalls near Bryant Park, a beautiful green space in Midtown Manhattan.",
      "address": "Bryant Park, New York, NY",
      "duration": "1-2 hours",
      "transportation": "Walk",
      "cost": "$15-25"
    },
    {
      "time": "Afternoon",
      "activity": "Explore Times Square & M&M's World",
      "description": "Experience the bright lights and bustling energy of Times Square. Visit M&M's World for a fun and colorful experience.",
      "address": "Times Square, New York, NY",
      "duration": "2-3 hours",
      "transportation": "Walk",
      "cost": "Free (except for any purchases)"
    },
    {
      "time": "Evening",
      "activity": "Dinner in Little Italy",
      "description": "Indulge in delicious Italian cuisine in the historic Little Italy neighborhood. Enjoy the lively atmosphere and traditional dishes.",
      "address": "Little Italy, New York, NY",
      "duration": "2-3 hours",
      "transportation": "Subway",
      "cost": "$30-50"
    }
  ],
  "Day 3: 2024-08-13": [
    {
      "time": "Morning",
      "activity": "Visit the Statue of Liberty & Ellis Island",
      "description": "Take a ferry to Liberty Island and visit the iconic Statue of Liberty. Afterwards, explore Ellis Island and learn about the history of immigration to the United States.",
      "address": "Battery Park, New York, NY (Ferry Departure Point)",
      "duration": "4-5 hours",
      "transportation": "Ferry",
      "cost": "$25-30"
    },
    {
      "time": "Lunch",
      "activity": "Lunch in the Financial District",
      "description": "Grab lunch in the Financial District, near the ferry terminal. There are numerous options ranging from casual to upscale dining.",
      "address": "Financial District, New York, NY",
      "duration": "1-2 hours",
      "transportation": "Walk",
      "cost": "$15-25"
    },
    {
      "time": "Afternoon",
      "activity": "Explore the 9/11 Memorial & Museum",
      "description": "Pay your respects at the 9/11 Memorial and reflect on the events of September 11, 2001. Visit the museum to learn more about the history and impact of this tragic day.",
      "address": "9/11 Memorial & Museum, New York, NY",
      "duration": "3-4 hours",
      "transportation": "Walk",
      "cost": "$26"
    },
    {
      "time": "Evening",
      "activity": "Dinner in Chinatown",
      "description": "Experience the vibrant culture and delicious food of Chinatown. Explore the bustling streets and enjoy an authentic Chinese dinner.",
      "address": "Chinatown, New York, NY",
      "duration": "2-3 hours",
      "transportation": "Subway",
      "cost": "$20-40"
    }
  ],
  "Day 4: 2024-08-14": [
    {
      "time": "Morning",
      "activity": "Visit the Metropolitan Museum of Art",
      "description": "Explore one of the world's largest and finest art museums, The Metropolitan Museum of Art. Admire masterpieces from various cultures and periods.",
      "address": "The Metropolitan Museum of Art, New York, NY",
      "duration": "3-4 hours",
      "transportation": "Subway",
      "cost": "$25"
    },
    {
      "time": "Lunch",
      "activity": "Lunch in Central Park",
      "description": "Enjoy a picnic lunch or dine at one of the cafes in Central Park, a sprawling oasis in the heart of Manhattan.",
      "address": "Central Park, New York, NY",
      "duration": "1-2 hours",
      "transportation": "Walk",
      "cost": "$15-25"
    },
    {
      "time": "Afternoon",
      "activity": "Explore Central Park & Strawberry Fields",
      "description": "Spend the afternoon exploring the scenic landscapes of Central Park. Visit Strawberry Fields, a memorial dedicated to John Lennon.",
      "address": "Central Park, New York, NY",
      "duration": "2-3 hours",
      "transportation": "Walk",
      "cost": "Free"
    },
    {
      "time": "Evening",
      "activity": "Dinner and Drinks in Chelsea",
      "description": "Enjoy dinner and drinks in the trendy Chelsea neighborhood, known for its art galleries, restaurants, and nightlife.",
      "address": "Chelsea, New York, NY",
      "duration": "2-3 hours",
      "transportation": "Subway",
      "cost": "$30-50"
    }
  ],
  "Day 5: 2024-08-15": [
    {
      "time": "Morning",
      "activity": "Visit the Top of the Rock Observation Deck",
      "description": "Enjoy stunning views of the city from the Top of the Rock Observation Deck at Rockefeller Center. Capture iconic photos of Central Park and the Empire State Building.",
      "address": "Rockefeller Center, New York, NY",
      "duration": "2-3 hours",
      "transportation": "Subway",
      "cost": "$40-50"
    },
    {
      "time": "Lunch",
      "activity": "Lunch near Rockefeller Center",
      "description": "Have lunch at one of the many restaurants or cafes near Rockefeller Center.",
      "address": "Rockefeller Center, New York, NY",
      "duration": "1-2 hours",
      "transportation": "Walk",
      "cost": "$15-25"
    },
    {
      "time": "Afternoon",
      "activity": "Depart from New York City",
      "description": "Head to JFK Airport or EWR Airport to catch your flight home. Allow ample time for transportation and airport security.",
      "address": "JFK Airport or EWR Airport, New York, NY",
      "duration": "2-3 hours",
      "transportation": "Taxi, Ride-share, or Public Transportation",
      "cost": "Varies depending on transportation costs"
    }
  ]
}
"""

TEST_TRIP_CHECKLIST = """
{
  "name": "The NYC Hustle Checklist",
  "checklist_groups": [
    {
      "name": "Carry On Bag",
      "contents": [
        {
          "id": "16",
          "name": "Monos Carry On Pro",
          "quantity": 1,
          "metadata": "Carry on Luggage"
        },
        {
          "id": "1",
          "name": "Summer Polo",
          "quantity": 1,
          "metadata": "To wear on a sunny day"
        },
        {
          "id": "2",
          "name": "Pima Cotton T-Shirt",
          "quantity": 1,
          "metadata": "A comfortable Olive Green T-shirt"
        },
        {
          "id": "3",
          "name": "Supima T-Shirt",
          "quantity": 2,
          "metadata": "One of each color"
        },
        {
          "id": "8",
          "name": "Full Sleeve Fleece Hoodie",
          "quantity": 1,
          "metadata": "Carry one of the two, for cooler evenings"
        },
        {
          "id": "9",
          "name": "SuperSoft Lounge Pants",
          "quantity": 1,
          "metadata": "Comfortable pants for relaxing at the hotel"
        },
        {
          "id": "11",
          "name": "541 Athletic Taper Jeans (32 x 32)",
          "quantity": 1,
          "metadata": "A pair of jeans for the trip"
        },
        {
          "id": "13",
          "name": "Tree Loungers",
          "quantity": 1,
          "metadata": "Comfortable shoes for walking"
        },
        {
          "id": "15",
          "name": "Slippers",
          "quantity": 1,
          "metadata": "For use at the hotel"
        }
      ]
    },
    {
      "name": "Backpack",
      "contents": [
        {
          "id": "17",
          "name": "ReFraction Packable Backpack",
          "quantity": 1,
          "metadata": "Your backpack for daily adventures"
        },
        {
          "id": "4",
          "name": "24x7 T-Shirt",
          "quantity": 1,
          "metadata": "In case you need an extra T-shirt"
        }
      ]
    }
  ],
  "misc_information": [
    "Remember to pack your travel essentials like your wallet, phone charger, and any necessary medications.",
    "Don't forget to apply sunscreen, especially during the day.",
    "Stay hydrated by carrying a reusable water bottle.",
    "Download offline maps of New York City in case you don't have internet access.",
    "Purchase a MetroCard for easy transportation on the subway.",
    "Book your flights and accommodation in advance, especially during peak season.",
    "Let your bank know about your travel dates to avoid any issues with your cards.",
    "Pack a light jacket or sweater for cooler evenings or air-conditioned places.",
    "Familiarize yourself with local customs and etiquette.",
    "Have a great trip to New York City!"
  ]
}
"""

TEST_OUTFIT = """
{
  "outfits": [
    {
      "outfitId": 1,
      "description": "Comfortable hiking outfit for a warm day",
      "pieces": [
        {
          "itemId": 6,
          "reason": "Moisture-wicking T-shirt for a hike"
        },
        {
          "itemId": 10,
          "reason": "Lightweight and stretchy jogger pants"
        },
        {
          "itemId": 14,
          "reason": "Comfortable and supportive hiking shoes"
        }
      ],
      "imagePrompt": "A man hiking in a heather navy T-shirt, olive green jogger pants, and terracotta hiking shoes",
      "style": "Activewear",
      "colorPalette": [
        "#3B5998",
        "#556B2F",
        "#E97451"
      ],
      "missing": [
        {
          "name": "Hiking Backpack",
          "category": "Accessories",
          "reason": "To carry water and essentials"
        }
      ]
    },
    {
      "outfitId": 2,
      "description": "Casual hiking look with a comfortable T-shirt and denim jeans",
      "pieces": [
        {
          "itemId": 2,
          "reason": "Lightweight and breathable T-shirt"
        },
        {
          "itemId": 11,
          "reason": "Durable denim jeans for hiking"
        },
        {
          "itemId": 14,
          "reason": "Sturdy hiking shoes"
        }
      ],
      "imagePrompt": "A man wearing an olive green T-shirt, dark wash denim jeans, and terracotta hiking shoes",
      "style": "Casual",
      "colorPalette": [
        "#556B2F",
        "#3B5998",
        "#E97451"
      ],
      "missing": [
        {
          "name": "Baseball Cap",
          "category": "Accessories",
          "reason": "To protect from the sun"
        }
      ]
    },
    {
      "outfitId": 3,
      "description": "A slightly dressier option for hiking with a polo shirt and beige pants",
      "pieces": [
        {
          "itemId": 1,
          "reason": "Polo shirt for a slightly more polished look"
        },
        {
          "itemId": 12,
          "reason": "Comfortable and breathable cotton pants"
        },
        {
          "itemId": 14,
          "reason": "Supportive hiking shoes"
        }
      ],
      "imagePrompt": "A man wearing a navy blue polo shirt, beige relaxed ankle pants, and terracotta hiking shoes",
      "style": "Smart Casual",
      "colorPalette": [
        "#3B5998",
        "#F5F5DC",
        "#E97451"
      ],
      "missing": []
    },
    {
      "outfitId": 4,
      "description": "Layering option for cooler weather with a fleece hoodie",
      "pieces": [
        {
          "itemId": 3,
          "reason": "Base layer for warmth"
        },
        {
          "itemId": 8,
          "reason": "Fleece hoodie for added warmth"
        },
        {
          "itemId": 10,
          "reason": "Lightweight and breathable jogger pants"
        },
        {
          "itemId": 14,
          "reason": "Sturdy hiking shoes"
        }
      ],
      "imagePrompt": "A man wearing a black T-shirt, a brick red fleece hoodie, olive green jogger pants, and terracotta hiking shoes",
      "style": "Activewear",
      "colorPalette": [
        "#000000",
        "#B22222",
        "#556B2F",
        "#E97451"
      ],
      "missing": []
    }
  ]
}
"""

TEST_WEATHER_FORECAST="""
{
  "cod": "200",
  "message": 0,
  "cnt": 40,
  "list": [
    {
      "dt": 1723334400,
      "main": {
        "temp": 28.96,
        "feels_like": 29.15,
        "temp_min": 28.17,
        "temp_max": 28.96,
        "pressure": 1012,
        "sea_level": 1012,
        "grnd_level": 1012,
        "humidity": 46,
        "temp_kf": 0.79
      },
      "weather": [
        {
          "id": 803,
          "main": "Clouds",
          "description": "broken clouds",
          "icon": "04d"
        }
      ],
      "clouds": {
        "all": 56
      },
      "wind": {
        "speed": 4.93,
        "deg": 264,
        "gust": 6.71
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "d"
      },
      "dt_txt": "2024-08-11 00:00:00"
    },
    {
      "dt": 1723345200,
      "main": {
        "temp": 27.01,
        "feels_like": 27.37,
        "temp_min": 25.84,
        "temp_max": 27.01,
        "pressure": 1013,
        "sea_level": 1013,
        "grnd_level": 1012,
        "humidity": 49,
        "temp_kf": 1.17
      },
      "weather": [
        {
          "id": 802,
          "main": "Clouds",
          "description": "scattered clouds",
          "icon": "03n"
        }
      ],
      "clouds": {
        "all": 48
      },
      "wind": {
        "speed": 2.95,
        "deg": 284,
        "gust": 6.33
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "n"
      },
      "dt_txt": "2024-08-11 03:00:00"
    },
    {
      "dt": 1723356000,
      "main": {
        "temp": 23.5,
        "feels_like": 23.32,
        "temp_min": 23.5,
        "temp_max": 23.5,
        "pressure": 1015,
        "sea_level": 1015,
        "grnd_level": 1014,
        "humidity": 54,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 801,
          "main": "Clouds",
          "description": "few clouds",
          "icon": "02n"
        }
      ],
      "clouds": {
        "all": 20
      },
      "wind": {
        "speed": 3.79,
        "deg": 337,
        "gust": 6.34
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "n"
      },
      "dt_txt": "2024-08-11 06:00:00"
    },
    {
      "dt": 1723366800,
      "main": {
        "temp": 21.76,
        "feels_like": 21.38,
        "temp_min": 21.76,
        "temp_max": 21.76,
        "pressure": 1015,
        "sea_level": 1015,
        "grnd_level": 1014,
        "humidity": 53,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 803,
          "main": "Clouds",
          "description": "broken clouds",
          "icon": "04n"
        }
      ],
      "clouds": {
        "all": 68
      },
      "wind": {
        "speed": 3.97,
        "deg": 354,
        "gust": 6.54
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "n"
      },
      "dt_txt": "2024-08-11 09:00:00"
    },
    {
      "dt": 1723377600,
      "main": {
        "temp": 22.41,
        "feels_like": 21.96,
        "temp_min": 22.41,
        "temp_max": 22.41,
        "pressure": 1016,
        "sea_level": 1016,
        "grnd_level": 1015,
        "humidity": 48,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 803,
          "main": "Clouds",
          "description": "broken clouds",
          "icon": "04d"
        }
      ],
      "clouds": {
        "all": 51
      },
      "wind": {
        "speed": 2.2,
        "deg": 343,
        "gust": 2.79
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "d"
      },
      "dt_txt": "2024-08-11 12:00:00"
    },
    {
      "dt": 1723388400,
      "main": {
        "temp": 25.74,
        "feels_like": 25.39,
        "temp_min": 25.74,
        "temp_max": 25.74,
        "pressure": 1016,
        "sea_level": 1016,
        "grnd_level": 1015,
        "humidity": 39,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 804,
          "main": "Clouds",
          "description": "overcast clouds",
          "icon": "04d"
        }
      ],
      "clouds": {
        "all": 100
      },
      "wind": {
        "speed": 2.62,
        "deg": 254,
        "gust": 3.68
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "d"
      },
      "dt_txt": "2024-08-11 15:00:00"
    },
    {
      "dt": 1723399200,
      "main": {
        "temp": 28.27,
        "feels_like": 27.57,
        "temp_min": 28.27,
        "temp_max": 28.27,
        "pressure": 1015,
        "sea_level": 1015,
        "grnd_level": 1013,
        "humidity": 35,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 804,
          "main": "Clouds",
          "description": "overcast clouds",
          "icon": "04d"
        }
      ],
      "clouds": {
        "all": 90
      },
      "wind": {
        "speed": 4.49,
        "deg": 222,
        "gust": 6.92
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "d"
      },
      "dt_txt": "2024-08-11 18:00:00"
    },
    {
      "dt": 1723410000,
      "main": {
        "temp": 27.87,
        "feels_like": 27.62,
        "temp_min": 27.87,
        "temp_max": 27.87,
        "pressure": 1013,
        "sea_level": 1013,
        "grnd_level": 1012,
        "humidity": 41,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 800,
          "main": "Clear",
          "description": "clear sky",
          "icon": "01d"
        }
      ],
      "clouds": {
        "all": 8
      },
      "wind": {
        "speed": 5.01,
        "deg": 205,
        "gust": 7.5
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "d"
      },
      "dt_txt": "2024-08-11 21:00:00"
    },
    {
      "dt": 1723420800,
      "main": {
        "temp": 26.19,
        "feels_like": 26.19,
        "temp_min": 26.19,
        "temp_max": 26.19,
        "pressure": 1014,
        "sea_level": 1014,
        "grnd_level": 1012,
        "humidity": 43,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 800,
          "main": "Clear",
          "description": "clear sky",
          "icon": "01n"
        }
      ],
      "clouds": {
        "all": 7
      },
      "wind": {
        "speed": 4.65,
        "deg": 260,
        "gust": 6.34
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "n"
      },
      "dt_txt": "2024-08-12 00:00:00"
    },
    {
      "dt": 1723431600,
      "main": {
        "temp": 23.88,
        "feels_like": 23.71,
        "temp_min": 23.88,
        "temp_max": 23.88,
        "pressure": 1015,
        "sea_level": 1015,
        "grnd_level": 1013,
        "humidity": 53,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 800,
          "main": "Clear",
          "description": "clear sky",
          "icon": "01n"
        }
      ],
      "clouds": {
        "all": 6
      },
      "wind": {
        "speed": 4.04,
        "deg": 296,
        "gust": 6.76
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "n"
      },
      "dt_txt": "2024-08-12 03:00:00"
    },
    {
      "dt": 1723442400,
      "main": {
        "temp": 22.19,
        "feels_like": 21.82,
        "temp_min": 22.19,
        "temp_max": 22.19,
        "pressure": 1015,
        "sea_level": 1015,
        "grnd_level": 1013,
        "humidity": 52,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 800,
          "main": "Clear",
          "description": "clear sky",
          "icon": "01n"
        }
      ],
      "clouds": {
        "all": 4
      },
      "wind": {
        "speed": 3.38,
        "deg": 314,
        "gust": 5.83
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "n"
      },
      "dt_txt": "2024-08-12 06:00:00"
    },
    {
      "dt": 1723453200,
      "main": {
        "temp": 21.16,
        "feels_like": 20.77,
        "temp_min": 21.16,
        "temp_max": 21.16,
        "pressure": 1014,
        "sea_level": 1014,
        "grnd_level": 1013,
        "humidity": 55,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 803,
          "main": "Clouds",
          "description": "broken clouds",
          "icon": "04n"
        }
      ],
      "clouds": {
        "all": 65
      },
      "wind": {
        "speed": 2.55,
        "deg": 296,
        "gust": 4.07
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "n"
      },
      "dt_txt": "2024-08-12 09:00:00"
    },
    {
      "dt": 1723464000,
      "main": {
        "temp": 21.84,
        "feels_like": 21.46,
        "temp_min": 21.84,
        "temp_max": 21.84,
        "pressure": 1015,
        "sea_level": 1015,
        "grnd_level": 1013,
        "humidity": 53,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 803,
          "main": "Clouds",
          "description": "broken clouds",
          "icon": "04d"
        }
      ],
      "clouds": {
        "all": 78
      },
      "wind": {
        "speed": 3.22,
        "deg": 278,
        "gust": 4.8
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "d"
      },
      "dt_txt": "2024-08-12 12:00:00"
    },
    {
      "dt": 1723474800,
      "main": {
        "temp": 25.38,
        "feels_like": 25.1,
        "temp_min": 25.38,
        "temp_max": 25.38,
        "pressure": 1015,
        "sea_level": 1015,
        "grnd_level": 1013,
        "humidity": 43,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 801,
          "main": "Clouds",
          "description": "few clouds",
          "icon": "02d"
        }
      ],
      "clouds": {
        "all": 12
      },
      "wind": {
        "speed": 5.32,
        "deg": 269,
        "gust": 7.38
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "d"
      },
      "dt_txt": "2024-08-12 15:00:00"
    },
    {
      "dt": 1723485600,
      "main": {
        "temp": 27.41,
        "feels_like": 27.01,
        "temp_min": 27.41,
        "temp_max": 27.41,
        "pressure": 1013,
        "sea_level": 1013,
        "grnd_level": 1012,
        "humidity": 37,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 802,
          "main": "Clouds",
          "description": "scattered clouds",
          "icon": "03d"
        }
      ],
      "clouds": {
        "all": 27
      },
      "wind": {
        "speed": 5.95,
        "deg": 265,
        "gust": 8.21
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "d"
      },
      "dt_txt": "2024-08-12 18:00:00"
    },
    {
      "dt": 1723496400,
      "main": {
        "temp": 27.19,
        "feels_like": 26.95,
        "temp_min": 27.19,
        "temp_max": 27.19,
        "pressure": 1013,
        "sea_level": 1013,
        "grnd_level": 1011,
        "humidity": 39,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 804,
          "main": "Clouds",
          "description": "overcast clouds",
          "icon": "04d"
        }
      ],
      "clouds": {
        "all": 85
      },
      "wind": {
        "speed": 6.01,
        "deg": 303,
        "gust": 8.32
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "d"
      },
      "dt_txt": "2024-08-12 21:00:00"
    },
    {
      "dt": 1723507200,
      "main": {
        "temp": 24.41,
        "feels_like": 24.24,
        "temp_min": 24.41,
        "temp_max": 24.41,
        "pressure": 1014,
        "sea_level": 1014,
        "grnd_level": 1013,
        "humidity": 51,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 803,
          "main": "Clouds",
          "description": "broken clouds",
          "icon": "04n"
        }
      ],
      "clouds": {
        "all": 57
      },
      "wind": {
        "speed": 5.46,
        "deg": 304,
        "gust": 8.29
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "n"
      },
      "dt_txt": "2024-08-13 00:00:00"
    },
    {
      "dt": 1723518000,
      "main": {
        "temp": 21.5,
        "feels_like": 21.25,
        "temp_min": 21.5,
        "temp_max": 21.5,
        "pressure": 1016,
        "sea_level": 1016,
        "grnd_level": 1014,
        "humidity": 59,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 800,
          "main": "Clear",
          "description": "clear sky",
          "icon": "01n"
        }
      ],
      "clouds": {
        "all": 2
      },
      "wind": {
        "speed": 5.46,
        "deg": 323,
        "gust": 8.75
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "n"
      },
      "dt_txt": "2024-08-13 03:00:00"
    },
    {
      "dt": 1723528800,
      "main": {
        "temp": 20.32,
        "feels_like": 19.95,
        "temp_min": 20.32,
        "temp_max": 20.32,
        "pressure": 1016,
        "sea_level": 1016,
        "grnd_level": 1014,
        "humidity": 59,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 800,
          "main": "Clear",
          "description": "clear sky",
          "icon": "01n"
        }
      ],
      "clouds": {
        "all": 7
      },
      "wind": {
        "speed": 3.5,
        "deg": 321,
        "gust": 4.39
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "n"
      },
      "dt_txt": "2024-08-13 06:00:00"
    },
    {
      "dt": 1723539600,
      "main": {
        "temp": 19.53,
        "feels_like": 19.16,
        "temp_min": 19.53,
        "temp_max": 19.53,
        "pressure": 1015,
        "sea_level": 1015,
        "grnd_level": 1014,
        "humidity": 62,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 803,
          "main": "Clouds",
          "description": "broken clouds",
          "icon": "04n"
        }
      ],
      "clouds": {
        "all": 65
      },
      "wind": {
        "speed": 3.78,
        "deg": 339,
        "gust": 4.79
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "n"
      },
      "dt_txt": "2024-08-13 09:00:00"
    },
    {
      "dt": 1723550400,
      "main": {
        "temp": 20.23,
        "feels_like": 19.82,
        "temp_min": 20.23,
        "temp_max": 20.23,
        "pressure": 1016,
        "sea_level": 1016,
        "grnd_level": 1015,
        "humidity": 58,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 803,
          "main": "Clouds",
          "description": "broken clouds",
          "icon": "04d"
        }
      ],
      "clouds": {
        "all": 83
      },
      "wind": {
        "speed": 3.27,
        "deg": 318,
        "gust": 4.75
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "d"
      },
      "dt_txt": "2024-08-13 12:00:00"
    },
    {
      "dt": 1723561200,
      "main": {
        "temp": 24.2,
        "feels_like": 23.77,
        "temp_min": 24.2,
        "temp_max": 24.2,
        "pressure": 1016,
        "sea_level": 1016,
        "grnd_level": 1015,
        "humidity": 42,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 804,
          "main": "Clouds",
          "description": "overcast clouds",
          "icon": "04d"
        }
      ],
      "clouds": {
        "all": 98
      },
      "wind": {
        "speed": 3.08,
        "deg": 332,
        "gust": 4.14
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "d"
      },
      "dt_txt": "2024-08-13 15:00:00"
    },
    {
      "dt": 1723572000,
      "main": {
        "temp": 27.36,
        "feels_like": 26.92,
        "temp_min": 27.36,
        "temp_max": 27.36,
        "pressure": 1015,
        "sea_level": 1015,
        "grnd_level": 1013,
        "humidity": 36,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 804,
          "main": "Clouds",
          "description": "overcast clouds",
          "icon": "04d"
        }
      ],
      "clouds": {
        "all": 99
      },
      "wind": {
        "speed": 2.46,
        "deg": 298,
        "gust": 3.07
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "d"
      },
      "dt_txt": "2024-08-13 18:00:00"
    },
    {
      "dt": 1723582800,
      "main": {
        "temp": 27.12,
        "feels_like": 26.9,
        "temp_min": 27.12,
        "temp_max": 27.12,
        "pressure": 1014,
        "sea_level": 1014,
        "grnd_level": 1012,
        "humidity": 39,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 804,
          "main": "Clouds",
          "description": "overcast clouds",
          "icon": "04d"
        }
      ],
      "clouds": {
        "all": 100
      },
      "wind": {
        "speed": 2.41,
        "deg": 282,
        "gust": 3.42
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "d"
      },
      "dt_txt": "2024-08-13 21:00:00"
    },
    {
      "dt": 1723593600,
      "main": {
        "temp": 26.49,
        "feels_like": 26.49,
        "temp_min": 26.49,
        "temp_max": 26.49,
        "pressure": 1014,
        "sea_level": 1014,
        "grnd_level": 1012,
        "humidity": 41,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 804,
          "main": "Clouds",
          "description": "overcast clouds",
          "icon": "04n"
        }
      ],
      "clouds": {
        "all": 100
      },
      "wind": {
        "speed": 1.74,
        "deg": 287,
        "gust": 3.42
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "n"
      },
      "dt_txt": "2024-08-14 00:00:00"
    },
    {
      "dt": 1723604400,
      "main": {
        "temp": 25.01,
        "feels_like": 24.85,
        "temp_min": 25.01,
        "temp_max": 25.01,
        "pressure": 1014,
        "sea_level": 1014,
        "grnd_level": 1013,
        "humidity": 49,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 804,
          "main": "Clouds",
          "description": "overcast clouds",
          "icon": "04n"
        }
      ],
      "clouds": {
        "all": 98
      },
      "wind": {
        "speed": 2.48,
        "deg": 280,
        "gust": 3.34
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "n"
      },
      "dt_txt": "2024-08-14 03:00:00"
    },
    {
      "dt": 1723615200,
      "main": {
        "temp": 24.13,
        "feels_like": 23.96,
        "temp_min": 24.13,
        "temp_max": 24.13,
        "pressure": 1014,
        "sea_level": 1014,
        "grnd_level": 1013,
        "humidity": 52,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 804,
          "main": "Clouds",
          "description": "overcast clouds",
          "icon": "04n"
        }
      ],
      "clouds": {
        "all": 91
      },
      "wind": {
        "speed": 2.48,
        "deg": 10,
        "gust": 4.62
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "n"
      },
      "dt_txt": "2024-08-14 06:00:00"
    },
    {
      "dt": 1723626000,
      "main": {
        "temp": 22.71,
        "feels_like": 22.55,
        "temp_min": 22.71,
        "temp_max": 22.71,
        "pressure": 1014,
        "sea_level": 1014,
        "grnd_level": 1013,
        "humidity": 58,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 801,
          "main": "Clouds",
          "description": "few clouds",
          "icon": "02n"
        }
      ],
      "clouds": {
        "all": 24
      },
      "wind": {
        "speed": 2.75,
        "deg": 356,
        "gust": 4.75
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "n"
      },
      "dt_txt": "2024-08-14 09:00:00"
    },
    {
      "dt": 1723636800,
      "main": {
        "temp": 23.1,
        "feels_like": 22.88,
        "temp_min": 23.1,
        "temp_max": 23.1,
        "pressure": 1015,
        "sea_level": 1015,
        "grnd_level": 1014,
        "humidity": 54,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 801,
          "main": "Clouds",
          "description": "few clouds",
          "icon": "02d"
        }
      ],
      "clouds": {
        "all": 19
      },
      "wind": {
        "speed": 3.32,
        "deg": 7,
        "gust": 5.22
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "d"
      },
      "dt_txt": "2024-08-14 12:00:00"
    },
    {
      "dt": 1723647600,
      "main": {
        "temp": 27.03,
        "feels_like": 26.94,
        "temp_min": 27.03,
        "temp_max": 27.03,
        "pressure": 1015,
        "sea_level": 1015,
        "grnd_level": 1014,
        "humidity": 41,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 800,
          "main": "Clear",
          "description": "clear sky",
          "icon": "01d"
        }
      ],
      "clouds": {
        "all": 7
      },
      "wind": {
        "speed": 3.19,
        "deg": 14,
        "gust": 3.27
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "d"
      },
      "dt_txt": "2024-08-14 15:00:00"
    },
    {
      "dt": 1723658400,
      "main": {
        "temp": 29.27,
        "feels_like": 28.45,
        "temp_min": 29.27,
        "temp_max": 29.27,
        "pressure": 1014,
        "sea_level": 1014,
        "grnd_level": 1013,
        "humidity": 35,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 802,
          "main": "Clouds",
          "description": "scattered clouds",
          "icon": "03d"
        }
      ],
      "clouds": {
        "all": 33
      },
      "wind": {
        "speed": 0.85,
        "deg": 78,
        "gust": 2.56
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "d"
      },
      "dt_txt": "2024-08-14 18:00:00"
    },
    {
      "dt": 1723669200,
      "main": {
        "temp": 27.69,
        "feels_like": 27.4,
        "temp_min": 27.69,
        "temp_max": 27.69,
        "pressure": 1014,
        "sea_level": 1014,
        "grnd_level": 1012,
        "humidity": 40,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 804,
          "main": "Clouds",
          "description": "overcast clouds",
          "icon": "04d"
        }
      ],
      "clouds": {
        "all": 93
      },
      "wind": {
        "speed": 2.88,
        "deg": 183,
        "gust": 2.52
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "d"
      },
      "dt_txt": "2024-08-14 21:00:00"
    },
    {
      "dt": 1723680000,
      "main": {
        "temp": 26.74,
        "feels_like": 26.92,
        "temp_min": 26.74,
        "temp_max": 26.74,
        "pressure": 1015,
        "sea_level": 1015,
        "grnd_level": 1013,
        "humidity": 45,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 804,
          "main": "Clouds",
          "description": "overcast clouds",
          "icon": "04n"
        }
      ],
      "clouds": {
        "all": 93
      },
      "wind": {
        "speed": 1.65,
        "deg": 140,
        "gust": 2.11
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "n"
      },
      "dt_txt": "2024-08-15 00:00:00"
    },
    {
      "dt": 1723690800,
      "main": {
        "temp": 25.13,
        "feels_like": 25.06,
        "temp_min": 25.13,
        "temp_max": 25.13,
        "pressure": 1016,
        "sea_level": 1016,
        "grnd_level": 1014,
        "humidity": 52,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 801,
          "main": "Clouds",
          "description": "few clouds",
          "icon": "02n"
        }
      ],
      "clouds": {
        "all": 13
      },
      "wind": {
        "speed": 1.54,
        "deg": 9,
        "gust": 3.52
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "n"
      },
      "dt_txt": "2024-08-15 03:00:00"
    },
    {
      "dt": 1723701600,
      "main": {
        "temp": 24,
        "feels_like": 23.87,
        "temp_min": 24,
        "temp_max": 24,
        "pressure": 1015,
        "sea_level": 1015,
        "grnd_level": 1014,
        "humidity": 54,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 801,
          "main": "Clouds",
          "description": "few clouds",
          "icon": "02n"
        }
      ],
      "clouds": {
        "all": 16
      },
      "wind": {
        "speed": 2.59,
        "deg": 21,
        "gust": 5.07
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "n"
      },
      "dt_txt": "2024-08-15 06:00:00"
    },
    {
      "dt": 1723712400,
      "main": {
        "temp": 22.96,
        "feels_like": 22.83,
        "temp_min": 22.96,
        "temp_max": 22.96,
        "pressure": 1016,
        "sea_level": 1016,
        "grnd_level": 1014,
        "humidity": 58,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 500,
          "main": "Rain",
          "description": "light rain",
          "icon": "10n"
        }
      ],
      "clouds": {
        "all": 60
      },
      "wind": {
        "speed": 2.69,
        "deg": 15,
        "gust": 4.78
      },
      "visibility": 10000,
      "pop": 0.2,
      "rain": {
        "3h": 0.11
      },
      "sys": {
        "pod": "n"
      },
      "dt_txt": "2024-08-15 09:00:00"
    },
    {
      "dt": 1723723200,
      "main": {
        "temp": 21.95,
        "feels_like": 21.79,
        "temp_min": 21.95,
        "temp_max": 21.95,
        "pressure": 1017,
        "sea_level": 1017,
        "grnd_level": 1016,
        "humidity": 61,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 500,
          "main": "Rain",
          "description": "light rain",
          "icon": "10d"
        }
      ],
      "clouds": {
        "all": 61
      },
      "wind": {
        "speed": 3.61,
        "deg": 21,
        "gust": 4.81
      },
      "visibility": 10000,
      "pop": 0.27,
      "rain": {
        "3h": 0.53
      },
      "sys": {
        "pod": "d"
      },
      "dt_txt": "2024-08-15 12:00:00"
    },
    {
      "dt": 1723734000,
      "main": {
        "temp": 26.47,
        "feels_like": 26.47,
        "temp_min": 26.47,
        "temp_max": 26.47,
        "pressure": 1017,
        "sea_level": 1017,
        "grnd_level": 1016,
        "humidity": 45,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 803,
          "main": "Clouds",
          "description": "broken clouds",
          "icon": "04d"
        }
      ],
      "clouds": {
        "all": 61
      },
      "wind": {
        "speed": 2.19,
        "deg": 34,
        "gust": 2.83
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "d"
      },
      "dt_txt": "2024-08-15 15:00:00"
    },
    {
      "dt": 1723744800,
      "main": {
        "temp": 29.13,
        "feels_like": 28.48,
        "temp_min": 29.13,
        "temp_max": 29.13,
        "pressure": 1016,
        "sea_level": 1016,
        "grnd_level": 1015,
        "humidity": 37,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 803,
          "main": "Clouds",
          "description": "broken clouds",
          "icon": "04d"
        }
      ],
      "clouds": {
        "all": 74
      },
      "wind": {
        "speed": 1.91,
        "deg": 139,
        "gust": 2.56
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "d"
      },
      "dt_txt": "2024-08-15 18:00:00"
    },
    {
      "dt": 1723755600,
      "main": {
        "temp": 26.32,
        "feels_like": 26.32,
        "temp_min": 26.32,
        "temp_max": 26.32,
        "pressure": 1015,
        "sea_level": 1015,
        "grnd_level": 1014,
        "humidity": 48,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 804,
          "main": "Clouds",
          "description": "overcast clouds",
          "icon": "04d"
        }
      ],
      "clouds": {
        "all": 100
      },
      "wind": {
        "speed": 4.14,
        "deg": 156,
        "gust": 3.73
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "d"
      },
      "dt_txt": "2024-08-15 21:00:00"
    }
  ],
  "city": {
    "id": 5128581,
    "name": "New York",
    "coord": {
      "lat": 40.7127,
      "lon": -74.006
    },
    "country": "US",
    "population": 8175133,
    "timezone": -14400,
    "sunrise": 1723284116,
    "sunset": 1723334449
  }
}"""