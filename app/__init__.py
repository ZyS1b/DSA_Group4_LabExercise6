from flask import Flask
import os

from .routes import main_blueprint
from .sorting_routes import sorting_blueprint
from .state import SITE_NAME


def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret")
    app.config["SITE_NAME"] = SITE_NAME
    app.register_blueprint(main_blueprint)
    app.register_blueprint(sorting_blueprint)
    return app
