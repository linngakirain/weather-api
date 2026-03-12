from django.db import models
from django.contrib.auth.models import User

class City(models.Model):
    name = models.CharField(max_length=163)
    country = models.CharField(max_length=2) # ISO country code e.g. GB
    lat = models.FloatField()
    lon = models.FloatField()
    
    def __str__(self):
        return f"{self.name}, {self.country}, ({self.lat}, {self.lon})"

class FavoriteLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'city']
    
    def __str__(self):
        return f"{self.user.username}'s {self.city.name}"

class WeatherAlert(models.Model):
    ALERT_TYPES = [
        ('RAIN', 'Rain Alert'),
        ('SNOW', 'Snow Alert'),
        ('TEMP_HIGH', 'High Temperature'),
        ('TEMP_LOW', 'Low Temperature'),
        ('WIND', 'Strong Wind'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    threshold = models.FloatField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_alert_type_display()} for {self.city.name}"
    
    def check_alert(self, current_temp):
        # check if the alert condition is met based on current weather data
        if self.alert_type == 'TEMP_LOW' and current_temp < self.threshold:
            return True
        elif self.alert_type == 'TEMP_HIGH' and current_temp > self.threshold:
            return True
        return False