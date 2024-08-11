import requests
import json
from collections import defaultdict
from datetime import date, datetime

from geopy.geocoders import Nominatim
from prettytable import PrettyTable
from constants import OPEN_WEATHER_API_KEY, TEST_WEATHER_FORECAST
from flags import WEATHER_TESTING

class WeatherForecast:

    def __init__(self, api_key: str = OPEN_WEATHER_API_KEY, testing: bool = WEATHER_TESTING):
        self.geolocator = Nominatim(user_agent="weather_app")
        self.api_key = api_key
        self.testing = testing

    def get_forecast_from_openweather(self, city: str):
        """Fetches daily weather forecast in JSON.

        Args:
            city: The city name.

        Returns:
            A JSON object containing the Open Weather forecast.
        """
        if not self.testing:
            latlng = self.geolocator.geocode(city)
            if not latlng:
                return f"Could not find weather data for {city}. Please check the city name."
            lat = latlng.latitude
            lon = latlng.longitude

            url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"
            response = requests.get(url)
            return json.loads(response.text)
        else:
            return json.loads(TEST_WEATHER_FORECAST)

    def get_forecast_table_from_data(self, forecast_data) -> str:
        forecast_table = PrettyTable()

        if len(forecast_data) == 0:
            return ""
        
        is_forecast_daily = 'time' not in forecast_data[0].keys()

        if is_forecast_daily:
            forecast_table.field_names = ["Date", "Weather", "Min Temp (°C)", "Max Temp (°C)", "Humidity (%)"]
        else:
            forecast_table.field_names = ["Date", "Time", "Weather", "Min Temp (°C)", "Max Temp (°C)", "Humidity (%)"]
        for forecast_data_item in forecast_data:
            if is_forecast_daily:
                forecast_table.add_row([str(forecast_data_item['date']),
                                        str(forecast_data_item['weather']), 
                                        str(forecast_data_item['min_temp']), 
                                        str(forecast_data_item['max_temp']), 
                                        str(forecast_data_item['humidity'])])
            else:
                forecast_table.add_row([str(forecast_data_item['date']), 
                                        str(forecast_data_item['time']),
                                        str(forecast_data_item['weather']), 
                                        str(forecast_data_item['min_temp']), 
                                        str(forecast_data_item['max_temp']), 
                                        str(forecast_data_item['humidity'])]) 
        return forecast_table.get_string()
    
    def get_forecast_table(self, city: str) -> str:
        forecast_data = self.get_forecast_data_table(self.get_forecast_data(city, self.api_key))
        return self.get_forecast_table_from_data(forecast_data)

    def get_forecast_data_hourly(self, city: str, date_filter: date = None) -> str:
        """Fetches hourly weather forecast for a particular city & date combination.

        Args:
            city: The city name.
            date_filter: The date for which we want the weather.

        Returns:
            A list containing hourly weather forecasts for date_filter else None.
        """
        forecast_json = self.get_forecast_from_openweather(city=city)
        
        hourly_forecast_data = []
        for forecast in forecast_json['list']:
            forecast_date = date.fromtimestamp(forecast['dt'])
            forecast_time = datetime.fromtimestamp(forecast['dt']).strftime('%H:%M')

            # Filter out the data that don't match date_filter.
            if date_filter and forecast_date.strftime('%Y-%m-%d') != date_filter.strftime('%Y-%m-%d'):
                continue

            hourly_forecast_data.append({
                'date': str(forecast_date),
                'time': str(forecast_time),
                'weather': forecast['weather'][0]['main'],
                'icon': forecast['weather'][0]['icon'],
                'min_temp': round(forecast['main']['temp_min']),
                'max_temp': round(forecast['main']['temp_max']),
                'humidity': forecast['main']['humidity']
            })
        return hourly_forecast_data
    
    def get_forecast_data_daily(self, city: str) -> str:
        """
        Fetches daily weather forecast for a particular city, showing the range of 
        min/max temperatures and humidity, and keeping all unique icons.

        Args:
            city: The city name.

        Returns:
            A list containing daily weather forecasts with ranges and icons.
        """
        forecast_json = self.get_forecast_from_openweather(city=city)
        
        forecast_data_per_day = defaultdict(list)
        for forecast in forecast_json['list']:
            forecast_date = date.fromtimestamp(forecast['dt'])
            forecast_data_per_day[forecast_date].append({
                'date': str(forecast_date),
                'weather': forecast['weather'][0]['main'],
                'icon': forecast['weather'][0]['icon'],
                'min_temp': round(forecast['main']['temp_min']),
                'max_temp': round(forecast['main']['temp_max']),
                'humidity': forecast['main']['humidity']
            })
        
        daily_forecast_data = []
        for forecast_date, hourly_forecasts in forecast_data_per_day.items():
            min_min_temp = min(hourly_forecast['min_temp'] for hourly_forecast in hourly_forecasts)
            max_min_temp = max(hourly_forecast['min_temp'] for hourly_forecast in hourly_forecasts)
            min_max_temp = min(hourly_forecast['max_temp'] for hourly_forecast in hourly_forecasts)
            max_max_temp = max(hourly_forecast['max_temp'] for hourly_forecast in hourly_forecasts)
            min_humidity = min(hourly_forecast['humidity'] for hourly_forecast in hourly_forecasts)
            max_humidity = max(hourly_forecast['humidity'] for hourly_forecast in hourly_forecasts)
            
            mid_idx = len(hourly_forecasts) // 2
            daily_forecast_data.append({
                'date': str(forecast_date),
                'weather': hourly_forecasts[mid_idx]['weather'],
                'icon': hourly_forecasts[mid_idx]['icon'],
                'min_temp': [min_min_temp, max_min_temp],
                'max_temp': [min_max_temp, max_max_temp],
                'humidity': [min_humidity, max_humidity]
            })

        return daily_forecast_data
