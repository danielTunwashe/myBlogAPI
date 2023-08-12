from flask_restx import Namespace, Resource, fields
#Importing user from models to query our database
from ..models.users import User
#Importing HTTP status class
from http import HTTPStatus
#Importing jwt_required to protect our endpoints and importing get_jwt_identity to know current user that signed up
from flask_jwt_extended import jwt_required,get_jwt_identity
#importing request from flask to access our data from the client
from flask import request
#importing sql-alchemy instance from utils
from ..utils import db
#Importing enquiries from models to query our database
from ..models.enquiries import Enquiry



admin_namespace=Namespace("admin",description="a complain Namespace")


#Createing a module for serialization (import fields from flask_restx)
enquiries_model=admin_namespace.model(
    'Enquiry',{
        'id':fields.Integer(description="An ID"),
        'firstname':fields.String(description="Your firstname",required=True),
        'lastname':fields.String(description="Your lastname",required=True),
        'enquiry':fields.String(description="Your enquiry",required=True)
    }
)


#Another module that helps us get our users details after registration in a json format
user_model=admin_namespace.model(
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

#Display list of all users
@admin_namespace.route('/all-users')
class GetAllEnquires(Resource):
    #Want the object returned to be returned as json
    @admin_namespace.marshal_with(user_model)
    #Protect our end point with jwt_required
    @jwt_required()
    def get(self):
        '''
            Display list of all users
        
        '''
        #First create a module that helps us serilaize the data we pass to our API as well as help us marshal our responses and then, our responses will be return as json 
        #Query all users from our database (import our user from models)
        user=User.query.all()
        #Return all users (return user returns all user as objects which is not json serializable) - (Import our HTTP status class from http)
        return user , HTTPStatus.OK
        
    

#Update User's profile by ID
@admin_namespace.route('/update/<int:user_id>')
class UpdateUserProfile(Resource):
    #Make the object returned json serializable
    @admin_namespace.marshal_with(user_model)
    #Protect our endpoint
    @jwt_required()
    def put(self,user_id):
        '''
           Update user's profile by ID
        
        '''
        user_to_update=User.get_by_id(user_id)
        
        #Gets the data that comes from user as json
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

#Delete User's profile by ID  
@admin_namespace.route('/delete/<int:user_id>')
class DeleteUserProfile(Resource):
    #Make the object returned json serilizable
    @admin_namespace.marshal_with(user_model)
    #protect our end point
    @jwt_required()
    def delete(self,user_id):
        '''
            Delete user's profile by ID
        
        '''
         #query for user to delete
        user_to_delete=User.get_by_id(user_id)
        
        #Use the simple method in the user model to delete easily
        user_to_delete.delete()
        
        #return a response
        return user_to_delete, HTTPStatus.NO_CONTENT

#Display list of all enquires made by a user
@admin_namespace.route('/all-enquires')
class GetAllUserEnquires(Resource):
    #Want the object returned to be returned as json
    @admin_namespace.marshal_with(enquiries_model)
    #Protect our end point with jwt_required
    @jwt_required()
    def get(self):
        '''
            Display list of all enquiries made by users
        
        '''
        #First create a module that helps us serilaize the data we pass to our API as well as help us marshal our responses and then, our responses will be return as json 
        #Query all  from our database (import our enquiry from models)
        enquiry=Enquiry.query.all()
        #Return all enquiries (return user returns all user as objects which is not json serializable) - (Import our HTTP status class from http)
        return enquiry , HTTPStatus.OK
  

#Delete a user enquiry by ID  
@admin_namespace.route('/enquiries/delete/<int:enquiry_id>')
class DeleteUserEnquiry(Resource):
    def delete(self,enquiry_id):
        '''
            Delete users's enquiry by ID
        
        '''
        #query for enquiry to delete
        enquiry_to_delete=Enquiry.get_by_id(enquiry_id)
        
        #Use the simple method in the enquiry model to delete easily
        enquiry_to_delete.delete()
        
        #return a response
        return enquiry_to_delete, HTTPStatus.NO_CONTENT
    
    
    
