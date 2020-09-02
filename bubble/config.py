"""Default configuration

Use env var to override
"""

from environs import Env

env = Env()

env.read_env(".flaskenv", recurse=False)

ENV = env("FLASK_ENV", "production")
DEBUG = ENV == "development"
SECRET_KEY = env("SECRET_KEY")

DATABASE_URI = env("DATABASE_URI")

JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND_URL")
DEFAULT_LOG_DIR = env("DEFAULT_LOG_DIR", "./logs")
DEFAULT_LOG_FILE = env("DEFAULT_LOG_FILE", "default.log")
ELASTICSEARCH_URL = env("ELASTICSEARCH_URL")
USER_CENTER_URL = env("USER_CENTER_URL")
