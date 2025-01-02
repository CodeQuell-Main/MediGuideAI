from flask import Flask 

def create_app():

    app = Flask(__name__)

    from .routes import chatbot_routes
    app.register_blueprint(chatbot_routes)

    return app