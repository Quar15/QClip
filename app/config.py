import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['APP_SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['APP_DATABASE_URL']
    if os.environ['APP_UPLOAD_DIRECTORY'].startswith('/'):
        UPLOAD_DIRECTORY = os.environ['APP_UPLOAD_DIRECTORY']
    else:
        UPLOAD_DIRECTORY = os.path.join(os.getcwd(), 'app/static', os.environ['APP_UPLOAD_DIRECTORY'])
    MAX_CONTENT_LENGTH = int(os.environ['APP_UPLOAD_MAX_CONTENT_LENGTH']) * 1024 * 1024  # Calculate MB
    ALLOWED_EXTENSIONS = [
            'mp4',
            'mkv',
            'avi',
            'mpeg',
            'ogg',
            'webm',
    ]


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    WTF_CSRF_ENABLED = False
