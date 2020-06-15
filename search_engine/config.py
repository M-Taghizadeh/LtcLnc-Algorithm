import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

class Development(Config):
    DEBUG = True
    

class Production(Config):
    DEBUG = False