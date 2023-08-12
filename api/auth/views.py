from flask_restx import Namespace,Resource, fields
#importing request from flask to access our data from the client
from flask import request
#importing our user class to create a new instance of our user
from ..models.users import User
#Importing pasword hash methods from werkzeug to has our password
from werkzeug.security import generate_password_hash,check_password_hash
#Importing HTTP satus code from HTTP
from http import HTTPStatus
#Importing access token and refresh token to create a JWT Identity
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
#importing sql-alchemy instance from utils
from ..utils import db


#Creating our namespace to seperate our application
auth_namespace=Namespace('user',description="a namespace for auhentication")


#Creating a serilization using flask restx and import (fields) from flask restx
signup_model=auth_namespace.model(
    'SignUp',{
        'id':fields.Integer(),
        'username':fields.String(required=True,description="A username"),
        'fullname':fields.String(required=True,description="A fullname"),
        'email':fields.String(required=True,description="An email"),
        'password':fields.String(required=True,description="A password"),
        'about_author':fields.String(required=True,description="About Author")
    }
)

#Another module that helps us get our users details after registration in a json format
user_model=auth_namespace.model(
    'User',{
        'id':fields.Integer(),
        'username':fields.String(required=True,description="A username"),
        'fullname':fields.String(required=True,description="A fullname"),
        'email':fields.String(required=True,description="An email"),
        'password_hash':fields.String(required=True,description="A password"),
        'about_author':fields.String(required=True,description="About Author"),
        'is_staff':fields.Boolean(description="This show that User is a staff")
    }
)

#Creating serilization using flask restx for login module
login_model=auth_namespace.model(
    'Login',{
        'email':fields.String(required=True,description="An emial"),
        'password':fields.String(required=True,description="A password")
    }
)


#import resource class and create our class that inherits from our resource class
@auth_namespace.route('/add')
class SignUp(Resource):
    #Post because we are going to send request to the server
    #Decorator to help us expect the information in our serilizer in order to send data to our API
    @auth_namespace.expect(signup_model)
    #Return our response via flask restx and the module created
    @auth_namespace.marshal_with(user_model)
    def post(self):
        """
            Sign/Register Up as a new user
        """
        #Access the data from our client (import request from flask)
        data = request.get_json()
        
        
        #Create a new user by going to the user.py file to setup a function to perform that
        #create a new user instance (import our user class from ..models.user)
        new_user=User(
            username=data.get('username'),
            fullname=data.get('fullname'),
            email=data.get('email'),
            #Generate a password hash by importing from werkzeug built in flask
            password_hash= generate_password_hash(data.get('password' )),
            about_author=data.get('about_author')
            
        )
        
        #save new user to our database
        new_user.save()
        
        #return the newly created user via our signup module (after including marshal with at the top) then we just retun our HTTP status request
        #import HTTP status code from HTTP
        return new_user, HTTPStatus.CREATED



#import resource class and create our class that inherits from our resource class
#Update user by ID
@auth_namespace.route('/update/<int:user_id>')
class UpdateUser(Resource):
    #Post because we are going to send request to the server
    # #First specify the data we are expecting or payload since we have created our serilization
    # @auth_namespace.expect(signup_model)
    #Make the object returned json serializable
    @auth_namespace.marshal_with(user_model)
    #Protect our endpoint
    @jwt_required()
    def put(self,user_id):
        
        """
            Update a user profile by ID
        """
        # #Query for the user
        user_to_update=User.get_by_id(user_id)
        
        #Gets the data that comes as our payload
        data = request.get_json()

        
        
        #Update our user due to different data that comes from our payload endpoint
        user_to_update.username=data.get('username')
        user_to_update.fullname=data.get('fullname')
        user_to_update.email=data.get('email')
        user_to_update.password=data.get('password')
        user_to_update.about_author=data.get('about_author')
        
        #Save to our database (import our sqlAlchemy instance from utils)
        db.session.commit()
        
        #return the updated user (we have to marshal with user_model and expect signUp_model) 
        return user_to_update, HTTPStatus.OK
    
        #Note content type must come before Authorization and bearer in insomia before updating 
        

#import resource class and create our class that inherits from our resource class
#Delete user by ID
@auth_namespace.route('/delete/<int:user_id>')
class DeleteUser(Resource):
    #Post because we are going to send request to the server
    #Make the object returned json serilizable
    @auth_namespace.marshal_with(user_model)
    #protect our end point
    @jwt_required()
    def delete(self,user_id):
        """
            Delete a user profile by ID
        """
        #query for user to delete
        user_to_delete=User.get_by_id(user_id)
        
        #Use the simple method in the user model to delete easily
        user_to_delete.delete()
        
        #return a response
        return user_to_delete, HTTPStatus.NO_CONTENT
    
@auth_namespace.route('/login')
class Login(Resource):
    #Post because we are going to send request to the server
    #Decorator to help us expect the login_model information in our serilizer in order to send data to our API
    @auth_namespace.expect(login_model)
    def post(self):
        """
            Login in after signing up and Generate a JWT pair
        """
        #Access the data from our client (import request from flask)
        data = request.get_json()
        
        #To login our user we first query to check if the user exist
        #first get our email and password
        email = data.get('email')
        password = data.get('password')
        #Scan the database and check if the user exist
        user=User.query.filter_by(email=email).first()
        #check if user exist
        if (user is not None) and (check_password_hash(user.password_hash,password)):
            #Generate an access token with the identity of that current user (we need to import access token and refresh token from flask_jwt_extended)
            #create access token
            access_token=create_access_token(identity=user.username)
            #create refresh token
            refresh_token=create_refresh_token(identity=user.username)
            
            #return a dictionary containing an access token and a refresh token
            response={
                'access_token':access_token,
                'refresh_token':refresh_token
            }
            
            # return our response and status code
            return response, HTTPStatus.OK
            
            
#import resource class and create our class that inherits from our resource class
#Acquire a new access token when expired
@auth_namespace.route('/refresh')
class Refresh(Resource):
    #Post because we are going to send request to the server
    #Protect our endpoint and since we want a new refresh token we have to set it to be True
    @jwt_required(refresh=True)
    def post(self):
        """
            Generate a new access token
        """
        #First, we neeed to get the identity of the current logged in user (ie we nrrd to protect these route using JWT_Required and get_jwt_identity which will be imported from flask_jwt_extended)
        #Gets user identity using the token
        username=get_jwt_identity()
        
        #Create a new token based on the identity we have
        access_token=create_access_token(identity=username)
        
        #Return a response containing the new access token
        return {'access_token':access_token},HTTPStatus.OK
        
        # #returns the current user username with the access token
        # return {"username":username}