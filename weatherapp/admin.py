from django.contrib import admin
from .models import City, FavoriteLocation, WeatherAlert

admin.site.register(City)
admin.site.register(FavoriteLocation)
admin.site.register(WeatherAlert)