from flask import Blueprint
from . import projects, errors, canary, results

api = Blueprint('api', __name__)
