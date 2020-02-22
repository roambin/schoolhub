from flask import Flask
from flask_cors import CORS
from app.controller import bp

folder = "../../dist"
# folder = "../../vue-admin-template/dist"


def create_app():
    app = Flask(__name__, static_folder=folder + "/static", template_folder=folder)
    CORS(app)
    app.jinja_env.variable_start_string = '[['
    app.jinja_env.variable_end_string = ']]'
    app.register_blueprint(bp)
    return app
