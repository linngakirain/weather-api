from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import OpenWeatherService

def HandleRegisterRequest(request):
    return HttpResponse('not yet implemented')

weather = OpenWeatherService()

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