# PackMyFit: Your AI-Powered Personal Stylist and Packing Assistant

PackMyFit is your one-stop solution for managing your wardrobe, creating perfect packing lists, and discovering stunning outfit combinations for any occasion. This web application, written in Python using Flask and SQL Alchemy, leverages the power of Gemini APIs via Google AI Studio and the Open Weather API for weather-aware recommendations.

## Features

* **Digital Closet:** Organize your clothing items effortlessly.
* **AI Packing Lists:** Generate customized packing lists based on your trip details and weather conditions.
* **Itinerary Generation:**  Create detailed itineraries for your trips.
* **AI Outfit Recommendations:** Discover stylish outfit combinations tailored to your preferences and the weather.
* **Weather Integration:** Incorporates real-time weather data for optimal packing suggestions and outfit recommendations.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/shreyasnbhat/packmyfit.git
   ```

2. **Navigate to the project directory:**

   ```bash
   cd packmyfit
   ```

3. **Create a virtual environment:**

   ```bash
   python3 -m venv .
   ```

4. **Activate the virtual environment:**

   ```bash
   source bin/activate
   ```

5. **Install dependencies:**

   ```bash
   pip3 install -r requirements.txt
   ```

## Configuration

* **API Keys:** Manage your API keys in `api_keys.py`.
* **Feature Flags:** Control application behavior using the flags in `flags.py`.


## API Key Setup
* **Weather Data:**
    * PackMyFit can obtain weather forecast data for your trips & events, but this will require an OpenWeather API key.
    * If an OpenWeather API Key is NOT available, dummy weather data will be used. Set `WEATHER_TESTING=True` in `flags.py`.
    * If you have an OpenWeather API Key, set `OPEN_WEATHER_API_KEY` in `api_keys.py` & set `WEATHER_TESTING=False` in `flags.py` to enable real-time weather data features.

* **AI Features (Packing & Itinerary):**
    * PackMyFit is an Gemini powered application and requires a Google AI Studio API Key for the AI Generated Checklists, Itineraries, Outfits etc.
    * If a Gemini API Key is NOT available, dummy packing and itinerary information will be displayed. Set `LLM_TESTING=True` in `flags.py`.
    * If you have a Gemini API Key set `GEMINI_API_KEY` in `api_keys.py` & set `LLM_TESTING=False` in `flags.py`.


## Testing Data

The `testdata` directory includes sample data for testing the AI features:

* **Item Images & Metadata:** Over 15 items across different categories with stock images and descriptions stored in `item_repository.csv`.
* **User Preferences:** Default user preferences are defined in `user_preferences.txt`.

**Directory Structure:**

```
testdata/
    - user_1_item_1/   # Stores the testdata images for User ID: 1, Item ID: 1
    - user_1_item_2/   # Stores the testdata images for User ID: 1, Item ID: 2
    - user_1_item_3/
    - ....
    - item_repository.csv
    - user_preferences.txt
```

## Re-Initializing the SQL Alchemy Database

To clear the database and re-initialize it on each server restart, set `RE_INIT_DB=True` in `flags.py`. Then, start the Flask server:

```bash
flask run
```

## Logging In

A default user account is provided for testing:

* **Username:** `testuser`
* **Password:** `abcd1234`

## Creating an Itinerary

A sample trip from San Jose to New York (August 11, 2024 - August 15, 2024) is pre-configured. You may also add/remove trips as needed.

* **Generating Itinerary & Checklist:**
    * Click the "Generate Itinerary" button to create an itinerary for New York.
    * Click the "Generate Checklist" button to create a packing checklist referencing your wardrobe items. Generated checklists contain sub-checklists for each bag such as Carry On Bag, Backpack etc. Each sub-checklist references the items you own and provides deep links to the digital closet.

## Creating an Outfit

A sample Hiking event in San Jose (August 11, 2024) is pre-configured. You may also add/remove events as needed.

* **AI-Powered Outfit Recommendations:**
    * PackMyFit leverages your digital closet, weather data, event description, time, and date to provide various outfit suggestions.
    * Click "Generate Outfits" to obtain options. The application will also suggest items you might want to add to your digital closet to complete an outfit.
    * A Gemini API key is required for this feature.

* **Weather Integration:**
    * Outfit recommendations take into account real-time weather conditions to ensure you're dressed appropriately.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.