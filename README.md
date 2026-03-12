# Weather API - COMP3011 Coursework (UoL)

A RESTful weather API with user authentication, favorites, weather alerts, daily summary, and weather history.

## Deployment

The API is deployed on PythonAnywhere:

- Base URL: https://rainl.pythonanywhere.com/api/
- Example: `GET https://rainl.pythonanywhere.com/api/pollution/?lat=48.85&lon=2.35`

## Features
- User registration/login/logout
- City search
- Current weather, 5-day forecast, air pollution
- Save favorite locations
- Weather alerts with threshold triggers
- Daily analytics summary over favourites
- Weather search history per user

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

## API Documentation

Full endpoint, parameter, authentication, and example request/response details:
- **API Documentation PDF**: `API_Documentation.pdf`  

## Testing
```
python weatherapp/tests.py
```
