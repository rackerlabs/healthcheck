from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()


def create_app(config_name=None):
    if config_name is None:
        config_name = 'default'
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    app.config['CELERY_BROKER_URL'] = 'redis://192.168.99.100:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://192.168.99.100:6379/0'

    config[config_name].init_app(app)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
