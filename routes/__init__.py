from flask import Flask
from .home import home_bp
from .about import about_bp
from .contact import contact_bp
from .signup import signup_bp
from .verifyOTP import verifyOTP_bp
from .login import login_bp
from flask_mysqldb import MySQL

def create_app():

    app = Flask(__name__)
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'sumit'

    app.register_blueprint(home_bp)
    app.register_blueprint(about_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(signup_bp)
    app.register_blueprint(verifyOTP_bp)
    app.register_blueprint(login_bp)

    return app