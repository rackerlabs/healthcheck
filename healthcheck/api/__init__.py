from flask import Blueprint

api = Blueprint('api', __name__)
from healthcheck.api import projects, errors, canary, results
