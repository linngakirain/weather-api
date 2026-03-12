import requests
from django.conf import settings
from datetime import datetime

class OpenWeatherService:
    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY
        self.CURRENT_WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'
        self.FORECAST_URL = 'https://api.openweathermap.org/data/2.5/forecast'
        self.GEOCODING_URL = 'https://api.openweathermap.org/geo/1.0/direct'
        self.AIR_POLLUTION_URL = 'https://api.openweathermap.org/data/2.5/air_pollution'
      
    def search_cities(self, query):
        # search for cities by name to get lat and lon
        url = f'{self.GEOCODING_URL}?q={query}&limit=5&appid={self.api_key}'
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            cities = response.json()
            
            result = []
            for city in cities:
                result.append({
                    'name': city['name'],
                    'country': city['country'],
                    'state': city.get('state', ''),
                    'lat': city['lat'],
                    'lon': city['lon'],
                })
            
            return {
                'success': True,
                'data': result
            }
        else:
            return {
                'success': False,
                'error': 'Search failed'
            }
      
    def get_current_weather(self, lat, lon):
        # get current weather of a location
        url = f'{self.CURRENT_WEATHER_URL}?lat={lat}&lon={lon}&units=metric&appid={self.api_key}'
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            return {
                'success': True,
                'data': {
                    'city': data['name'],
                    'country': data['sys']['country'],
                    'lat': lat,
                    'lon': lon,
                    'temperature': data['main']['temp'],
                    'feels_like': data['main']['feels_like'],
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'weather': data['weather'][0]['description'],
                    'wind_speed': data['wind']['speed'],
                    'wind_direction': data['wind']['deg'],
                    'clouds': data['clouds']['all'],
                    'sunrise': data['sys']['sunrise'],
                    'sunset': data['sys']['sunset'],
                }
            }
        else:
            return {
                'success': False,
                'error': f'Location not found: {lat}, {lon}'
            }

    def get_forecast(self, lat, lon):
        # get 5-day forecast of a location
        url = f'{self.FORECAST_URL}?lat={lat}&lon={lon}&units=metric&appid={self.api_key}'
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            forecast_list = []
            for item in data['list']:
                forecast_list.append({
                    'datetime': item['dt_txt'],
                    'temperature': item['main']['temp'],
                    'weather': item['weather'][0]['description'],
                    'humidity': item['main']['humidity'],
                    'wind_speed': item['wind']['speed'],
                })
            
            return {
                'success': True,
                'data': {
                    'city': data['city']['name'],
                    'country': data['city']['country'],
                    'lat': lat,
                    'lon': lon,
                    'forecast': forecast_list
                }
            }
        else:
            return {
                'success': False,
                'error': f'Location not found: {lat}, {lon}'
            }

    def get_air_pollution(self, lat, lon):
        # get air pollution data
        url = f'{self.AIR_POLLUTION_URL}?lat={lat}&lon={lon}&appid={self.api_key}'
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data['list']:
                pollution = data['list'][0]
                # Air Quality Index: 1=Good, 2=Fair, 3=Moderate, 4=Poor, 5=Very Poor
                aqi = pollution['main']['aqi']
                aqi_text = ['Good', 'Fair', 'Moderate', 'Poor', 'Very Poor'][aqi-1]
                
                return {
                    'success': True,
                    'data': {
                        'aqi': aqi,
                        'aqi_text': aqi_text,
                        'components': pollution['components']
                    }
                }
            else:
                return {
                    'success': False,
                    'error': 'No pollution data'
                }
        else:
            return {
                'success': False,
                'error': f'Pollution data error: {response.status_code}'
            }