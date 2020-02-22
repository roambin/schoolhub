from flask import Blueprint

bp = Blueprint('bp', __name__)

from app.controller import controller
