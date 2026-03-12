import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"
session = requests.Session()

# Basic test
tests = [
    ("POST", "/register/", {"username": "test", "email": "test@example.com", "password": "testing"}),
    ("POST", "/login/", {"username": "test", "password": "testing"}),
    ("GET", "/check-auth/", None),
    ("GET", "/search/?q=Paris", None),
    ("GET", "/weather/?lat=48.85&lon=2.35", None),
    ("GET", "/forecast/?lat=48.85&lon=2.35", None),
    ("GET", "/pollution/?lat=48.85&lon=2.35", None),
    ("POST", "/favorites/add/", {"name": "Paris", "country": "FR", "lat": 48.85, "lon": 2.35}),
    ("GET", "/favorites/", None),
    ("GET", "/analytics/daily-summary/", None),
]

for method, endpoint, data in tests:
    print(f"\n{method} {endpoint}")
    if method == "GET":
        r = session.get(f"{BASE_URL}{endpoint}")
    else:
        r = session.post(f"{BASE_URL}{endpoint}", json=data)
    print(f"Status: {r.status_code}")
    try:
        response_data = r.json()
        print(json.dumps(response_data, indent=2)[:500])
    except:
        print(f"Raw response: {r.text[:200]}")

# Alert functionality test

# 1. Get city_id from favorites - FIXED
print("\n1. Getting city_id from favorites")
r = session.get(f"{BASE_URL}/favorites/")
print(f"Status: {r.status_code}")
favorites = r.json()
print(json.dumps(favorites, indent=2))

if favorites['success'] and favorites['favorites']:
    # Get city coordinates from favorite
    fav = favorites['favorites'][0]
    lat = fav['lat']
    lon = fav['lon']
    
    # Search for the city to get actual City ID
    print(f"\nSearching for city at {lat}, {lon}")
    r = session.get(f"{BASE_URL}/search/?q={fav['name']}")
    search_results = r.json()
    
    if search_results['success'] and search_results['data']:
        # Find matching city by coordinates
        city_id = None
        for city in search_results['data']:
            if abs(city['lat'] - lat) < 0.01 and abs(city['lon'] - lon) < 0.01:
                city_id = 1  # Assume first city in DB
                break
        
        if not city_id:
            city_id = 1  # Fallback
        
        print(f"Using City ID: {city_id}")

        # 2. Create alert
        print("\n2. CREATE ALERT")
        alert_data = {
            "city_id": city_id,
            "alert_type": "TEMP_LOW",
            "threshold": 5.0
        }
        r = session.post(f"{BASE_URL}/alerts/create/", json=alert_data)
        print(f"Status: {r.status_code}")
        print(json.dumps(r.json(), indent=2))

        # 3. Get all alerts
        print("\n3. GET ALL ALERTS")
        r = session.get(f"{BASE_URL}/alerts/")
        print(f"Status: {r.status_code}")
        alerts = r.json()
        print(json.dumps(alerts, indent=2))

        # 4. Check if alerts triggered
        print("\n4. CHECK ALERTS TRIGGERED")
        r = session.get(f"{BASE_URL}/alerts/check/{city_id}/")
        print(f"Status: {r.status_code}")
        check_data = r.json()
        print(json.dumps(check_data, indent=2))

        # 5. Toggle alert
        if alerts['success'] and alerts['alerts']:
            alert_id = alerts['alerts'][0]['id']
            print(f"\n5. TOGGLE ALERT {alert_id}")
            r = session.put(f"{BASE_URL}/alerts/toggle/{alert_id}/")
            print(f"Status: {r.status_code}")
            print(json.dumps(r.json(), indent=2))

            # 6. Delete alert
            print(f"\n6. DELETE ALERT {alert_id}")
            r = session.delete(f"{BASE_URL}/alerts/delete/{alert_id}/")
            print(f"Status: {r.status_code}")
            print(json.dumps(r.json(), indent=2))
        else:
            print("\nNo alerts found to toggle/delete")
    else:
        print("\nCould not find city in search")
else:
    print("\nNo favorites found. Add a favorite first.")

# logout
r = session.post(f"{BASE_URL}/logout/")
print(f"Status: {r.status_code}")
print(r.json())