from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from healthcheck.config import get_config

db = SQLAlchemy()


def create_app(config_name=None):
    app = Flask(__name__)
    config = get_config(config_name=config_name)
    app.config.from_object(config)

    config.init_app(app)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    from healthcheck.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
