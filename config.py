import os

DB_URL = os.environ.get('DB_CONNECTION_STRING',
                        default='postgresql+psycopg2://user2:Rootmode2@localhost:6433/test_for_course')


class Config:
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    JSON_SORT_KEYS = os.getenv("JSON_SORT_KEYS", False)
    JSON_AS_ASCII = os.getenv("JSON_AS_ASCII", False)
    DEBUG = os.getenv("DEBUG", True)
    SQLALCHEMY_RECORD_QUERIES = True


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = DB_URL
    TESTING = True
