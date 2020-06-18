import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    FLASK_ENV = os.getenv("FLASK_ENV")

class Development(Config):
    DEBUG = True
    

class Production(Config):
    DEBUG = False