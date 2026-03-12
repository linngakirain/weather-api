from django.contrib import admin
from django.urls import path
from weatherapp.views import (
    register, login, logout_view, check_auth,
    search, current, forecast, pollution,
    add_favorite, get_favorites, delete_favorite
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/register/', register),
    path('api/login/', login),
    path('api/logout/', logout_view),
    path('api/check-auth/', check_auth),
    
    path('api/search/', search),
    path('api/weather/', current),
    path('api/forecast/', forecast),
    path('api/pollution/', pollution),
    
    path('api/favorites/', get_favorites),
    path('api/favorites/add/', add_favorite),
    path('api/favorites/delete/<int:favorite_id>/', delete_favorite),
]