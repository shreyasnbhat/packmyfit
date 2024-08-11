#### Creating your Digital Closet

# Re Initializaing the SQL Alchemy DB
Every time the flasks server starts by using the following command the DB may be re-initialized if you want to clear out any new things you may have added. Set `RE_INIT_DB=True` in `flags.py` to perform the re-initialization on every server restart.

```
flask run
```

# Logging In
For testing purposes, a default user is provided to you. The login details are:

```
username: testuser
password: abcd1234
```

# Creating Itinerary
- A Trip from San Jose to New York from August 11, 2024 to August 15, 2024 is created for you.
- If OpenWeather API Key is not provided, we will use the dummy weather forecast data to show you the destination weather in New York. Set `WEATHER_TESTING` flag in `flags.py` to enable Dummy Weather Data.
- If a Gemini API Key is not available, the AI Packing & Itinerary features will not work. Dummy packing and itinerary information provided in this case. Set `LLM_TESTING=True` flag in `flags.py` to enable Itinerary and Checklists.
- If a Gemini API Key is available, override the  GEMINI_API_KEY constant in the `api_keys.py`, and make sure you set 
`LLM_TESTING=False` flag in `flags.py`.
- Upon clicking Generate Itinerary Button, a itinerary will be created for New York.
- Upon clicking Generate Checklist Button, a checklist will be created that reference the items you own.