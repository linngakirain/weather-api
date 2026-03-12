from django.contrib import admin
from django.urls import path
from weatherapp.views import (
    register, login, logout_view, check_auth,
    search, current, forecast, pollution,
    add_favorite, get_favorites, delete_favorite, get_city_from_favorite,
    create_alert, get_alerts, delete_alert, toggle_alert, check_alerts,
    daily_summary,
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
    path('api/favorites/city/<int:favorite_id>/', get_city_from_favorite),
    
    path('api/alerts/', get_alerts),
    path('api/alerts/create/', create_alert),
    path('api/alerts/delete/<int:alert_id>/', delete_alert),
    path('api/alerts/toggle/<int:alert_id>/', toggle_alert),
    path('api/alerts/check/<int:city_id>/', check_alerts),

    path('api/analytics/daily-summary/', daily_summary),

]