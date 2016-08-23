import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'postgresql://postgres@localhost:5432/canaryDB'
    CELERY_BROKER_URL = 'redis://192.168.99.101:6379/0'
    CELERY_RESULT_BACKEND = 'redis://192.168.99.101:6379/0'
    API_URL = 'http://localhost:5000'


class LocalhostDevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'postgresql://postgres@localhost:5432/postgres'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    API_URL = 'http://localhost:5000'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'postgresql://localhost/testdb'


class DockerConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:password@db:5432/postgres'
    CELERY_BROKER_URL = 'redis://queue:6379/0'
    CELERY_RESULT_BACKEND = 'redis://queue:6379/0'
    API_URL = 'http://api:5000'

config = {
    'development': DevelopmentConfig,
    'localhost': LocalhostDevelopmentConfig,
    'testing': TestingConfig,
    'docker': DockerConfig,
    'default': DevelopmentConfig
}


def get_config(config_name=None):
    return config.get(config_name or os.getenv('FLASK_CONFIG') or 'default')
