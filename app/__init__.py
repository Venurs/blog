from flask import Flask
from app.config import config
from app.extensions import config_extensions
from app.views import *
from uploads import photos
from flask_uploads import configure_uploads


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config_extensions(app)
    config_blueprint(app)
    configure_uploads(app, photos)
    return app