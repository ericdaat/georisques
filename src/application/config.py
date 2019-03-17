class DefaultConfig(object):
    DEBUG = True
    TESTING = True
    SECRET_KEY = "dev"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/georisques.db"
    REDIS_URL = "redis://localhost:6379"
