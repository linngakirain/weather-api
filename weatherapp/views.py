from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login, logout
import json
from django.contrib.auth.decorators import login_required
from .models import City, FavoriteLocation, WeatherAlert  # Added WeatherAlert
from .services import OpenWeatherService

weather = OpenWeatherService()

@csrf_exempt
def register(request):
    # user registration
    if request.method == 'POST':
        # get data from request
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        # validation
        if not username or not email or not password:
            return JsonResponse({
                'success': False,
                'error': 'Username, email and password required'
            }, status=400)
        
        # check if username already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'success': False,
                'error': 'Username already taken'
            }, status=400)
        
        # check if email already exists
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'success': False,
                'error': 'Email already registered'
            }, status=400)
        
        # create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        return JsonResponse({
            'success': True,
            'message': 'User created successfully',
            'user_id': user.id,
            'username': user.username
        }, status=201)
        
    else:
        return JsonResponse({
            'success': False,
            'error': 'Registration requires POST method'
        }, status=405)

@csrf_exempt
def login(request):
    # user login
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # login successful
            django_login(request, user)
            return JsonResponse({
                'success': True,
                'message': 'Login successful',
                'user_id': user.id,
                'username': user.username
            }, status=200)
        else:
            return JsonResponse({
                'success': False,
                'error': 'Invalid username or password'
            }, status=401)

@csrf_exempt
def logout_view(request):
    # logout user
    if request.method == 'POST':
        logout(request)
        return JsonResponse({
            'success': True,
            'message': 'Logged out successfully'
        }, status=200)
    else:
        return JsonResponse({
            'success': False,
            'error': 'Method not allowed. Use POST'
        }, status=405)

@csrf_exempt
def check_auth(request):
    # check if user is logged in
    if request.user.is_authenticated:
        return JsonResponse({
            'success': True,
            'authenticated': True,
            'user_id': request.user.id,
            'username': request.user.username
        })
    else:
        return JsonResponse({
            'success': True,
            'authenticated': False
        })

@csrf_exempt
def search(request):
    # search for cities and return their lat and lon
    query = request.GET.get('q', '')
    
    result = weather.search_cities(query)
    return JsonResponse(result)

@csrf_exempt
def current(request):
    # get current weather by coordinates
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    
    lat = float(lat)
    lon = float(lon)
    
    result = weather.get_current_weather(lat, lon)
    return JsonResponse(result)

@csrf_exempt
def forecast(request):
    # get 5 day forecast by coordinates
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    lat = float(lat)
    lon = float(lon)
     
    result = weather.get_forecast(lat, lon)
    return JsonResponse(result)

@csrf_exempt
def pollution(request):
    # get air pollution data by coordinates
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    lat = float(lat)
    lon = float(lon)
    
    result = weather.get_air_pollution(lat, lon)
    return JsonResponse(result)

@login_required
@csrf_exempt
def add_favorite(request):
    # add a city to user's favorites
    if request.method == 'POST':
        data = json.loads(request.body)
        
        city_name = data.get('name')
        country = data.get('country')
        lat = data.get('lat')
        lon = data.get('lon')
        
        if not city_name or not country or not lat or not lon:
            return JsonResponse({
                'success': False,
                'error': 'Missing fields'
            }, status=400)
        
        city, created = City.objects.get_or_create(
            name=city_name,
            country=country,
            lat=lat,
            lon=lon
        )
        
        if FavoriteLocation.objects.filter(user=request.user, city=city).exists():
            return JsonResponse({
                'success': False,
                'error': 'Already in favorites'
            }, status=400)
        
        favorite = FavoriteLocation.objects.create(
            user=request.user,
            city=city
        )
        
        return JsonResponse({
            'success': True,
            'favorite_id': favorite.id
        }, status=201)
    
    return JsonResponse({
        'success': False,
        'error': 'Use POST'
    }, status=405)

@login_required
@csrf_exempt
def get_favorites(request):
    # get user's favorite locations
    if request.method == 'GET':
        favorites = FavoriteLocation.objects.filter(user=request.user).select_related('city')
        
        data = []
        for fav in favorites:
            data.append({
                'id': fav.id,
                'name': fav.city.name,
                'country': fav.city.country,
                'lat': fav.city.lat,
                'lon': fav.city.lon,
                'created_at': fav.created_at
            })
        
        return JsonResponse({
            'success': True,
            'favorites': data
        })
    
    return JsonResponse({
        'success': False,
        'error': 'Use GET'
    }, status=405)
    
@login_required
@csrf_exempt
def delete_favorite(request, favorite_id):
    # delete a favorite location
    if request.method == 'DELETE':
        try:
            favorite = FavoriteLocation.objects.get(id=favorite_id, user=request.user)
            favorite.delete()
            return JsonResponse({
                'success': True,
                'message': 'Deleted'
            })
        except FavoriteLocation.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Not found'
            }, status=404)
    
    return JsonResponse({
        'success': False,
        'error': 'Use DELETE'
    }, status=405)
    
@login_required
@csrf_exempt
def create_alert(request):
    # create a weather alert
    if request.method == 'POST':
        data = json.loads(request.body)
        
        city_id = data.get('city_id')
        alert_type = data.get('alert_type')
        threshold = data.get('threshold')
        
        if not city_id or not alert_type or not threshold:
            return JsonResponse({
                'success': False,
                'error': 'Missing fields'
            }, status=400)
        
        try:
            city = City.objects.get(id=city_id)
        except City.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'City not found'
            }, status=404)
        
        alert = WeatherAlert.objects.create(
            user=request.user,
            city=city,
            alert_type=alert_type,
            threshold=threshold
        )
        
        return JsonResponse({
            'success': True,
            'alert_id': alert.id,
            'alert_type': alert.get_alert_type_display(),
            'city': city.name,
            'threshold': alert.threshold
        }, status=201)
    
    return JsonResponse({
        'success': False,
        'error': 'Use POST'
    }, status=405)

@login_required
@csrf_exempt
def get_alerts(request):
    # get all alerts for logged-in user
    if request.method == 'GET':
        alerts = WeatherAlert.objects.filter(user=request.user, is_active=True).select_related('city')
        
        data = []
        for alert in alerts:
            data.append({
                'id': alert.id,
                'city_id': alert.city.id,
                'city_name': alert.city.name,
                'country': alert.city.country,
                'alert_type': alert.alert_type,
                'alert_type_display': alert.get_alert_type_display(),
                'threshold': alert.threshold,
                'is_active': alert.is_active,
                'created_at': alert.created_at
            })
        
        return JsonResponse({
            'success': True,
            'alerts': data
        })
    
    return JsonResponse({
        'success': False,
        'error': 'Use GET'
    }, status=405)

@login_required
@csrf_exempt
def delete_alert(request, alert_id):
    # delete an alert
    if request.method == 'DELETE':
        try:
            alert = WeatherAlert.objects.get(id=alert_id, user=request.user)
            alert.delete()
            return JsonResponse({
                'success': True,
                'message': 'Alert deleted'
            })
        except WeatherAlert.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Alert not found'
            }, status=404)
    
    return JsonResponse({
        'success': False,
        'error': 'Use DELETE'
    }, status=405)

@login_required
@csrf_exempt
def toggle_alert(request, alert_id):
    # turn alert on or off
    if request.method == 'PUT':
        try:
            alert = WeatherAlert.objects.get(id=alert_id, user=request.user)
            alert.is_active = not alert.is_active
            alert.save()
            return JsonResponse({
                'success': True,
                'is_active': alert.is_active,
                'message': f"Alert {'activated' if alert.is_active else 'deactivated'}"
            })
        except WeatherAlert.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Alert not found'
            }, status=404)
    
    return JsonResponse({
        'success': False,
        'error': 'Use PUT'
    }, status=405)

@login_required
@csrf_exempt
def check_alerts(request, city_id):
    # check if any alerts are triggered for a city
    if request.method == 'GET':
        try:
            city = City.objects.get(id=city_id)
        except City.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'City not found'
            }, status=404)
        
        weather_service = OpenWeatherService()
        weather_result = weather_service.get_current_weather(city.lat, city.lon)
        
        if not weather_result['success']:
            return JsonResponse({
                'success': False,
                'error': 'Could not get weather data'
            }, status=500)
        
        current_temp = weather_result['data']['temperature']
        
        # get all active alerts for this city and user
        alerts = WeatherAlert.objects.filter(
            user=request.user,
            city=city,
            is_active=True
        )
        
        triggered = []
        for alert in alerts:
            if alert.check_alert(current_temp):
                triggered.append({
                    'id': alert.id,
                    'type': alert.get_alert_type_display(),
                    'threshold': alert.threshold,
                    'current': current_temp
                })
        
        return JsonResponse({
            'success': True,
            'city': city.name,
            'current_temp': current_temp,
            'alerts_triggered': triggered,
            'total_alerts': len(triggered)
        })
    
    return JsonResponse({
        'success': False,
        'error': 'Use GET'
    }, status=405)
    
@login_required
@csrf_exempt
def get_city_from_favorite(request, favorite_id):
    # get city details from a favorite
    if request.method == 'GET':
        try:
            fav = FavoriteLocation.objects.get(id=favorite_id, user=request.user)
            return JsonResponse({
                'success': True,
                'city_id': fav.city.id,
                'name': fav.city.name,
                'country': fav.city.country,
                'lat': fav.city.lat,
                'lon': fav.city.lon
            })
        except FavoriteLocation.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Favorite not found'
            }, status=404)
    
    return JsonResponse({
        'success': False,
        'error': 'Use GET'
    }, status=405)

@login_required
@csrf_exempt
def daily_summary(request):
    # analytics summary over user's favourites
    if request.method != 'GET':
        return JsonResponse({
            'success': False,
            'error': 'Use GET'
        }, status=405)

    favorites = FavoriteLocation.objects.filter(user=request.user).select_related('city')

    if not favorites.exists():
        return JsonResponse({
            'success': True,
            'summary': {
                'favorite_count': 0,
                'average_temperature': None,
                'coldest': None,
                'hottest': None,
            },
            'details': [],
            'message': 'No favorites found for user'
        })

    details = []
    temps = []

    for fav in favorites:
        result = weather.get_current_weather(fav.city.lat, fav.city.lon)
        if not result.get('success'):
            continue

        data = result['data']
        temp = data.get('temperature')
        if temp is None:
            continue

        entry = {
            'favorite_id': fav.id,
            'city': data.get('city'),
            'country': data.get('country'),
            'lat': data.get('lat'),
            'lon': data.get('lon'),
            'temperature': temp,
            'weather': data.get('weather'),
        }
        details.append(entry)
        temps.append((temp, entry))

    if not temps:
        return JsonResponse({
            'success': False,
            'error': 'Could not fetch weather data for any favorites'
        }, status=502)

    avg_temp = sum(t[0] for t in temps) / len(temps)
    coldest = min(temps, key=lambda t: t[0])[1]
    hottest = max(temps, key=lambda t: t[0])[1]

    return JsonResponse({
        'success': True,
        'summary': {
            'favorite_count': len(details),
            'average_temperature': avg_temp,
            'coldest': coldest,
            'hottest': hottest,
        },
        'details': details
    })