# from flask import Blueprint, render_template, jsonify
# import requests

# weather = Blueprint('weather', __name__)

# # Configuration de l'API OpenWeatherMap
# OPENWEATHER_API_KEY = 'b1fd6e14799699504191b6bdbcadfc35'
# BASE_WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather'

# @weather.route('/get_weather', methods=['GET'])
# def get_weather():
#     # Exemple avec des coordonnées statiques, vous pouvez les rendre dynamiques
#     lat, lon = 48.8566, 2.3522  # Coordonnées de Paris, France
#     weather_url = f'{BASE_WEATHER_URL}?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric'
#     response = requests.get(weather_url)
#     if response.ok:
#         return jsonify(response.json())
#     else:
#         return jsonify({'error': 'Failed to fetch weather data'}), response.status_code

# @weather.route('/weather_map')
# def weather_map():
#     return render_template('weather.html')

# Autres routes et fonctions pour la météo si nécessaire

from flask import Blueprint, request, jsonify, render_template ,session, redirect, url_for
from models import User
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required

import requests


weather = Blueprint('weather', __name__)

BASE_WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'
OPENWEATHER_API_KEY = 'b1fd6e14799699504191b6bdbcadfc35'
@weather.route('/get_weather_by_coords', methods=['GET'])
def get_weather_by_coords():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    if not lat or not lon:
        return jsonify({'error': 'Missing latitude or longitude parameters'}), 400

    weather_url = f'{BASE_WEATHER_URL}?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric'
    response = requests.get(weather_url)
    if response.ok:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Failed to fetch weather data'}), response.status_code

@weather.route('/get_regional_weather', methods=['GET'])
def get_regional_weather():
    # Exemple : Utiliser des coordonnées pour identifier une région
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    # (Vous pouvez ajouter une logique pour choisir différents points de la région)
    response = requests.get(f"{BASE_WEATHER_URL}?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric")
    if response.ok:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Failed to fetch regional weather data'}), response.status_code


@weather.route('/get_city_weather', methods=['GET'])
def get_city_weather():
    # Recevoir les coordonnées ou l'identifiant de la ville en paramètre
    city_id = request.args.get('city_id')  # ou lat, lon
    # Faire une requête à OpenWeatherMap pour la ville
    response = requests.get(f"{BASE_WEATHER_URL}?id={city_id}&appid={OPENWEATHER_API_KEY}&units=metric")
    if response.ok:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Failed to fetch city weather data'}), response.status_code

@weather.route('/logout')
def logout():
    # Clear session or any user-specific data here
    session.clear()
    logout_user()
    # Redirect to login page or home page after logout
    return redirect(url_for('auth.login'))

@weather.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response

@weather.route('/weather_map')
def weather_map():
    return render_template('weather.html')
