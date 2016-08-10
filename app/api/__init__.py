from flask import Blueprint

api = Blueprint('api', __name__)
from . import projects, errors, canary, results
