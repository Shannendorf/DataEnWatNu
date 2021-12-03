import secrets
import os
import logging
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
rootdir = os.path.abspath(os.path.join(basedir, ".."))
load_dotenv(os.path.join(rootdir, '.env'))

APP_NAME = os.environ.get('APP_NAME') or 'APP_NAME'
SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_urlsafe()
TESTING = os.environ.get('TESTING') or False
DEV = os.environ.get('DEVELOPMENT') or False

## DB Settings
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'postgresql+psycopg2://postgres:mysecretpassword@127.0.0.1:5432/DataEnWatNu_db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

## Auth Settings
EXPIRATION_TIME = os.environ.get('EXPIRATION_TIME') or 2629800

## Logging Settings
logging_level = os.environ.get("LOGGING_LEVEL")
if logging_level == 'DEBUG':
    LOGGING_LEVEL = logging.DEBUG       # pragma: no cover 
elif logging_level == 'INFO':
    LOGGING_LEVEL = logging.INFO        # pragma: no cover
elif logging_level == 'WARNING':
    LOGGING_LEVEL = logging.WARNING     # pragma: no cover
elif logging_level == 'ERROR':  
    LOGGING_LEVEL =  logging.ERROR      # pragma: no cover
elif logging_level == 'CRITICAL':
    LOGGING_LEVEL = logging.CRITICAL    # pragma: no cover
else:
    LOGGING_LEVEL = logging.WARNING     # pragma: no cover
LOGGING_BACKUP_COUNT = os.environ.get('LOGGING_BACKUP_COUNT') or 10
LOGGING_SIZE = os.environ.get('LOGGING_SIZE') or 10240
LOGGING_EMAIL = os.environ.get("LOGGING_EMAIL")

## Email Settings
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = 1
MAIL_USERNAME = '639datatest@gmail.com'
MAIL_PASSWORD = 'Ditiseenaardappelwell!569659#%'
ADMINS = ['639datatest@gmail.com']