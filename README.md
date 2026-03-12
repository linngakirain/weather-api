# Weather API - COMP3011 Coursework

A RESTful weather API with user authentication, favorites, and weather alerts.

## Features
- User registration/login/logout
- City search
- Current weather, 5-day forecast, air pollution
- Save favorite locations
- Weather alerts with threshold triggers

## Tech Stack
- Django 6.0
- OpenWeatherMap API

## Setup
#### Clone the repository
```
git clone https://github.com/linngakirain/weather.git
cd weather
```

#### Set up environment variables
Create a `.env` file in the project root:
```
cp .env.sample .env
```

#### Run database migrations
```
python manage.py migrate
```

#### Create a superuser
```
python manage.py createsuperuser
```

#### Start the development server
```
python manage.py runserver
```

#### Access the application
- API Base URL: http://127.0.0.1:8000/api/
- Admin Interface: http://127.0.0.1:8000/admin/

## API Endpoints

### Authentication
- **POST** ` /api/register/` - Register new user
- **POST** ` /api/login/` - Login user
- **POST** ` /api/logout/` - Logout user
- **GET** ` /api/check-auth/` - Check login status

### Weather Data
- **GET** ` /api/search/?q=London` - Search cities
- **GET** ` /api/weather/?lat=48.85&lon=2.35` - Current weather
- **GET** ` /api/forecast/?lat=48.85&lon=2.35` - 5-day forecast
- **GET** ` /api/pollution/?lat=48.85&lon=2.35` - Air pollution

### Favorites (Requires Login)
- **GET** ` /api/favorites/` - Get all favorites
- **POST** ` /api/favorites/add/` - Add favorite
- **DELETE** ` /api/favorites/delete/1/` - Delete favorite

### Weather Alerts (Requires Login)
- **GET** ` /api/alerts/` - Get all alerts
- **POST** ` /api/alerts/create/` - Create alert
- **PUT** ` /api/alerts/toggle/1/` - Toggle alert on/off
- **DELETE** ` /api/alerts/delete/1/` - Delete alert
- **GET** ` /api/alerts/check/1/` - Check triggered alerts

## Testing
```
python weatherapp/tests.py
```