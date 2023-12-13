from flask import Flask
from .home import home_bp
from .about import about_bp
from .contact import contact_bp
from .signup import signup_bp
from .verifyOTP import verifyOTP_bp
from .login import login_bp
from .refreshToken import refreshToken_bp
from flask_mysqldb import MySQL

def create_app():

    app = Flask(__name__)
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'sumit'
    app.config['secretKey'] = "b4e328a84a0f4d9484444b2708847078"
    app.config["email"] = "sumit401sinha@gmail.com"
    app.config["password"] = "uere uwdk fcnz tuon"

    app.register_blueprint(home_bp)
    app.register_blueprint(about_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(signup_bp)
    app.register_blueprint(verifyOTP_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(refreshToken_bp)

    return app