from flask import Blueprint, render_template , redirect, url_for

main = Blueprint('main', __name__)

@main.route('/')
def index():
    #return redirect(url_for('weather.weather_map'))
    return render_template('auth.html')