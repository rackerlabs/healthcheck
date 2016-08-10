import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    db_string = 'postgresql://aded0190:helloworld@localhost:5432/canaryDB'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or db_string
    # 'postgresql://aded0190:helloworld@localhost:5432/canaryDB'
    #  sqlite:///' + os.path.join(basedir, 'data-dev.sqlite)


class TestingConfig(Config):
    TESTING = True
    db_string = "postgresql://localhost/testdb"
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or db_string

    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    db_string = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or db_string

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'unix': UnixConfig,
    'default': DevelopmentConfig
}
