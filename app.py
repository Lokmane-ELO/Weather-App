from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from models import User
import os 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(16)

#bootstrap = Bootstrap(app)

lm = LoginManager(app)

from extensions import db
db.init_app(app)


login_manager = LoginManager(app)
#login_manager.login_view = 'auth.login'  # Redirige vers la page de connexion

# Import et enregistrement des Blueprints
from views.main import main as main_blueprint
app.register_blueprint(main_blueprint)


from views.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

from views.weather import weather as weather_blueprint
app.register_blueprint(weather_blueprint)


# Autres initialisations...
@app.before_first_request
def create_tables():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    app.run(debug=True)
