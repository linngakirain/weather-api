from django.contrib import admin
from django.urls import path
from weatherapp.views import search, current, forecast, pollution, HandleRegisterRequest

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/search/', search),
    path('api/weather/', current),
    path('api/forecast/', forecast),
    path('api/pollution/', pollution),
    path('api/register/', HandleRegisterRequest),
]
