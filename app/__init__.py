from flask import Flask, session
from flask_dance.contrib.google import make_google_blueprint, google
from dotenv import load_dotenv
import os

def create_app():

    app = Flask(__name__)

    load_dotenv()

    app.secret_key = os.getenv('FLASK_SECRET_KEY')
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SECURE'] = False

    google_bp = make_google_blueprint(
        client_id=os.getenv('OAUTH_CLIENT_ID'),
        client_secret=os.getenv('OAUTH_CLIENT_SECRET'),
        redirect_to='chatbot_routes.callback',
        scope=[
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "openid"
        ]
    )

    app.register_blueprint(google_bp)

    from .routes import chatbot_routes
    app.register_blueprint(chatbot_routes, url_prefix='')

    return app