from flask import Flask
from flask_cors import CORS
from app.routes.home_routes import *

def create_app():
    app = Flask(__name__)
    CORS(app)  # permite requisições do Angular

    app.register_blueprint(home_routes)

    return app