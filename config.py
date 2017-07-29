import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = '0707eb3a-38c9-497e-9d6c-3069bce2e603'
    SQLALCHEMY_DATABASE_URI = \
        'sqlite:///' + os.path.join(basedir,'data.sqlite')
    SQLALCHEMY_COMMIT_IN_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = \
        'sqlite:///' + os.path.join(basedir,'data-dev.sqlite')
    @classmethod
    def init_app(cls,app):
        Config.init_app(app)
        import logging
        handler = logging.FileHandler('app.log', encoding='UTF-8')
        handler.setLevel(logging.DEBUG)
        logging_format = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
        handler.setFormatter(logging_format)
        app.logger.addHandler(handler)

    
      
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = \
        'sqlite:///' + os.path.join(basedir,'data-test.sqlite')

class ProductionConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = \
        'sqlite:///' + os.path.join(basedir,'data.sqlite')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
