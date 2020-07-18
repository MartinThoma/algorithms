#!/usr/bin/env python

# Core Library modules
import os


class Config:
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = "2c084ae6f1b340a7af8880400b83cb49"
    FLASK_SECRET = SECRET_KEY
    DB_HOST = os.environ["DB_HOST"]
    DB_PORT = os.environ.get("DB_PORT", 3306)
    DB_DATABASE = os.environ["DB_DATABASE"]
    DB_USER = os.environ["DB_USER"]
    DB_PASSWORD = os.environ["DB_PASSWORD"]
    sqlalchemy_connection_string = (
        "mysql+pymysql://{user}:{password}@{host}:{port}/{db}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = sqlalchemy_connection_string.format(
        port=DB_PORT, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, db=DB_DATABASE,
    )
