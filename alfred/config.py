import os
class BaseConfig:
    SECRET_KEY = '60808326457a6384f78964761aaa161c'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    # This is to suppress SQLAlchemy warnings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ADMIN_SWATCH = 'flatly'
    MAIL_SERVER = 'smtp.office365.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True

    MAIL_USERNAME =os.environ['MAIL_USERNAME']
    MAIL_PASSWORD =os.environ['MAIL_PASSWORD']


class TestConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

    HASH_ROUNDS = 1
