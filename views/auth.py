from flask import  render_template, request,  redirect, url_for, flash, session, abort

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db
from forms import LoginForm, RegisterForm
import pyotp, pyqrcode, base64
from io import BytesIO

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('weather.weather_map'))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash('Username already exists.')
            return redirect(url_for('auth.register'))

        # Generate a random TOTP secret
        totp_secret = pyotp.random_base32()

        # Create new user with hashed password and TOTP secret
        user = User(username=form.username.data, 
                    password_hash=generate_password_hash(form.password.data),
                    totp_secret=totp_secret)

        db.session.add(user)
        db.session.commit()

        # Redirect to the two-factor setup page
        flash('User registered successfully. Please set up two-factor authentication.')
        return redirect(url_for('auth.two_factor_setup', username=user.username))

    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('weather.weather_map'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.password_hash, form.password.data):
            # Verify 2FA token
            totp = pyotp.TOTP(user.totp_secret)
            if totp.verify(form.token.data):
                login_user(user)
                flash('Logged in successfully.')
                return redirect(url_for('weather.weather_map'))
            else:
                flash('Invalid 2FA token.')
        else:
            flash('Invalid username or password.')

    return render_template('login.html', form=form)


@auth.route('/two_factor_verify', methods=['POST'])
def two_factor_verify():
    username = session.get('username')
    if not username:
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(username=username).first()
    if not user:
        flash('User not found.')
        return redirect(url_for('login'))

    token = request.form.get('token')
    totp = pyotp.TOTP(user.totp_secret)
    if totp.verify(token):
        login_user(user)
        session.pop('username', None)  # Clear session variable
        return redirect(url_for('weather.weather_map'))
    else:
        flash('Invalid 2FA token.')
        return redirect(url_for('auth.two_factor_setup', username=username))

@auth.route('/two_factor_setup')
def two_factor_setup():
    username = request.args.get('username')
    if not username:
        return redirect(url_for('login'))

    user = User.query.filter_by(username=username).first()
    if not user:
        return redirect(url_for('login'))

    session['username'] = username
    url = pyotp.totp.TOTP(user.totp_secret).provisioning_uri(username, issuer_name="YourAppName")
    qr = pyqrcode.create(url)
    stream = BytesIO()
    qr.svg(stream, scale=4)
    stream.seek(0)
    data = base64.b64encode(stream.getvalue()).decode()

    return render_template('two_factor_setup.html', qr_code=data)



@auth.route('/qrcode')
def qrcode():
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()

    if user is None:
        abort(404)

    # Generate QR code
    url = pyotp.totp.TOTP(user.totp_secret).provisioning_uri(user.username, issuer_name="YourAppName")
    qr = pyqrcode.create(url)
    stream = BytesIO()
    qr.svg(stream, scale=4)
    return stream.getvalue(), 200, {
        'Content-Type': 'image/svg+xml'
    }


"""""
@auth.route('/two_factor_setup')
def two_factor_setup():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    
    user = User.query.filter_by(username=session['username']).first()
    if not user:
        flash('User not found.')
        return redirect(url_for('auth.login'))
    
    # Generate the TOTP URI for QR Code
    totp_uri = user.get_totp_uri()
    qr = pyqrcode.create(totp_uri)
    stream = BytesIO()
    qr.svg(stream, scale=4)
    stream.seek(0)
    qr_code = base64.b64encode(stream.getvalue()).decode('utf-8')

    return render_template('two_factor_setup.html', qr_code=qr_code)


@auth.route('/two_factor_verify', methods=['POST'])
def two_factor_verify():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    user = User.query.filter_by(username=session['username']).first()
    if not user:
        flash('User not found.')
        return redirect(url_for('auth.login'))

    token = request.form.get('token')
    if user.verify_totp(token):
        login_user(user)
        session.pop('username', None)  # Clear session variable
        return redirect(url_for('main.index'))
    else:
        flash('Invalid 2FA token.')
        return redirect(url_for('auth.two_factor_setup'))
"""
"""""
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.verify_password(form.password.data):
            session['username'] = user.username
            return redirect(url_for('auth.two_factor_setup'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)
"""
""""
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login.')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)
"""""