from django.test import TestCase
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

session = requests.Session()

# register user
print("\nregistering user")
data = {"username": "dummy", "email": "dummy@example.com", "password": "dummydummy"}
r = session.post(f"{BASE_URL}/register/", json=data)
print(r.json())

# login
print("\nlogging in")
data = {"username": "dummy", "password": "dummydummy"}
r = session.post(f"{BASE_URL}/login/", json=data)
print(r.json())

# search city
print("\nsearching London")
r = session.get(f"{BASE_URL}/search/?q=London")
print(r.json())

# get weather for London
print("\ngetting weather for London")
r = session.get(f"{BASE_URL}/weather/?lat=51.5074&lon=-0.1278")
print(r.json())

# add favorite
print("\nadding London to favorites")
data = {"name": "London", "country": "GB", "lat": 51.5074, "lon": -0.1278}
r = session.post(f"{BASE_URL}/favorites/add/", json=data)
print(r.json())

# getting favorites
print("\ngetting favorites")
r = session.get(f"{BASE_URL}/favorites/")
print(r.json())

# logout
print("\nlogging out")
r = session.post(f"{BASE_URL}/logout/")
print(r.json())