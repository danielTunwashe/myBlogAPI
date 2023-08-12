#setting up our configurations
import os
#After importing our secret key
from decouple import config
#Import timedelta to configure our JWT expiration period
from datetime import timedelta


#Setting up our coonection string to specify the path of our database
BASE_DIR=os.path.dirname(os.path.realpath(__file__))


class Config:
    SECRET_KEY=config('SECRET_KEY','secret')
    #Specifying some configuration specific to sqlite
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    #setting up jwt access token life span (import time delta from date time)
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=30)
    #setting up jwt refresh token life span
    JWT_REFRESH_TOKEN_EXPIRES=timedelta(minutes=30)
    #Configure our JWT secret key (also add to our .env file)
    JWT_SECRET_KEY=config('JWT_SECRET_KEY')
    


class DevConfig(Config):
    DEBUG=config('DEBUG',cast=bool)
    #Specifying some configuration specific to sqlite
    SQLALCHEMY_ECHO=True
    #Create our connection string
    SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(BASE_DIR,'db.sqlite3')
    
    
class TestConfig(Config):
    pass


class ProdConfig(Config):
    pass


#Simple dictionary that helps us assist our classes 
config_dict={
    'dev':DevConfig,
    'prod':ProdConfig,
    'test':TestConfig
}