import requests
import json
from datetime import date, datetime

from geopy.geocoders import Nominatim
from prettytable import PrettyTable
from constants import OPEN_WEATHER_API_KEY

class WeatherForecast:

  def __init__(self):
      self.geolocator = Nominatim(user_agent="weather_app")

  def get_weather_data(self, city: str, api_key: str = OPEN_WEATHER_API_KEY) -> str:
      """Fetches daily weather forecast and formats it into a table.

      Args:
          city: The city name.
          api_key: Your Open Weather API key.

      Returns:
          A formatted table string containing daily weather forecasts or an error message.
      """
      latlng = self.geolocator.geocode(city)
      if not latlng:
          return f"Could not find weather data for {city}. Please check the city name."
      lat = latlng.latitude
      lon = latlng.longitude

      forecast_data = []
      url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
      response = requests.get(url)
      forecast_json = json.loads(response.text)

      for forecast in forecast_json['list']:
          forecast_date = date.fromtimestamp(forecast['dt'])
          forecast_data.append({
              'date': forecast_date.strftime('%Y-%m-%d'),
              'weather': forecast['weather'][0]['main'],
              'min_temp': round(forecast['main']['temp_min']),
              'max_temp': round(forecast['main']['temp_max']),
              'humidity': forecast['main']['humidity']
          })

      forecast_table = PrettyTable()
      forecast_table.field_names = ["Date", "Weather", "Min Temp (°C)", "Max Temp (°C)", "Humidity (%)"]
      for day_data in forecast_data:
          forecast_table.add_row([day_data['date'], day_data['weather'], day_data['min_temp'], 
                        day_data['max_temp'], day_data['humidity']])

      return forecast_table.get_string()
