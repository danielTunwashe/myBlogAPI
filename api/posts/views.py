from flask_restx import Namespace,Resource,fields
#Importing posts from models to query our database
from ..models.posts import Post
#Importing HTTP status class
from http import HTTPStatus
#Importing jwt_required to protect our endpoints and importing get_jwt_identity to know current user that created the post
from flask_jwt_extended import jwt_required,get_jwt_identity
#Importing User from users table to get query our database and get our current user username
from ..models.users import User
#Importing sql alchemy instance
from ..utils import db


post_namespace = Namespace("posts",description="a post namespace")

#Createing a module for serialization (import fields from flask_restx)
post_model=post_namespace.model(
    'Post',{
        'id':fields.Integer(description="An ID"),
        'title':fields.String(description="title of post",required=True),
        'content':fields.String(description="content of post(ie Main body of post)",required=True),
        'slug':fields.String(description="Slug for post",required=True)
    }
)

#Module for creating posts by users
@post_namespace.route('/add-post')
class CreatePost(Resource):
    #First specify the data we are expecting or payload since we have created our serilization
    @post_namespace.expect(post_model)
    #Protect our end point with jwt_required
    #Return our object as json by marshaling it with our post_model
    @post_namespace.marshal_with(post_model)
    @jwt_required()
    def post(self):
        """
            Create a new post
        """
        #Getting current user who posted username
        username=get_jwt_identity()
        #Querying the user table to get the user username
        current_user=User.query.filter_by(username=username).first()
        
        #Access the data from our client through our post_namespace.payload (similar to request.getjson from flask)
        data = post_namespace.payload
        
        #Using the payload data which is a dictionary to create our post
        new_post=Post(
            title=data['title'],
            content=data['content'],
            slug=data['slug']
        )
        #specify the user which created the post (via the relationship between the users and the posts table using the backref in our users table) import get_jwt_identity
        new_post.blogger=current_user
        
        #save our post to the database
        new_post.save()
        
        return new_post, HTTPStatus.CREATED
    

#module for getting all posts (This is for Admins and Users)
@post_namespace.route('/all-posts')
class GetAllPosts(Resource):
    #Want the object returned to be returned as json
    @post_namespace.marshal_with(post_model)
    #Protect our end point with jwt_required
    @jwt_required()
    def get(self):
        #First create a module that helps us serilaize the data we pass to our API as well as help us marshal our responses and then, our responses will be return as json 
        """
           Get all posts 
        """
        #Query all posts from our database (import our post from models)
        posts=Post.query.all()
        #Return all posts (return post returns all orders as objects which is not json serializable) - (Import our HTTP status class from http)
        return posts , HTTPStatus.OK
        


#module for getting specific post
@post_namespace.route('/post/<int:post_id>')
class GetSpecificPost(Resource):
    #Make the object returned json serializable
    @post_namespace.marshal_with(post_model)
    #Protect our end point via jwt_required
    @jwt_required()
    def get(self,post_id):
        """
           Get a specific post by id
        """
        #Query for the post by its ID in the database
        post=Post.get_by_id(post_id)
        
        #Return our post and HTTP status
        return post,HTTPStatus.OK


#module for updating a post by ID
@post_namespace.route('/post/edit/<int:post_id>')
class UpdatePostById(Resource):
    #First specify the data we are expecting or payload since we have created our serilization
    @post_namespace.expect(post_model)
    #Make the object returned json serializable
    @post_namespace.marshal_with(post_model)
    #Protect our end point
    @jwt_required()
    def put(self,post_id):
        """
           Update a post by id
        """
        #Query for the post 
        post_to_update = Post.get_by_id(post_id)
        
        #Gets the data that comes as our payload
        data = post_namespace.payload
        
        #Update our post due to different data that has come to our end point
        post_to_update.title=data['title']
        post_to_update.content=data['content']
        post_to_update.slug=data['slug']
        
        #Save to our database (import our sqlAlchemy instance from utils)
        db.session.commit()
        
        #Return the updated post
        return post_to_update, HTTPStatus.OK


#module for deleting a post by ID (This is for Admins)
@post_namespace.route('/post/delete/<int:post_id>')
class DeletePostById(Resource):
    #protect our end point
    @jwt_required()
    #Make the object returned json serilizable
    @post_namespace.marshal_with(post_model)
    def delete(self,post_id):
        """
           Delete a post by id
        """
        #Query for the post to delete
        post_to_delete = Post.get_by_id(post_id)
        
        #Use the simple method in the post model to delete easily
        post_to_delete.delete()
        
        #return a response
        return post_to_delete, HTTPStatus.NO_CONTENT
    
#module for getting a specific user posts
@post_namespace.route('/user/<int:user_id>/post/<int:post_id>/')
class GetSpecificPostByUser(Resource):
    #How to return our object as json serializable
    @post_namespace.marshal_with(post_model)
    #Protect our endpoint
    @jwt_required()
    def get(self,user_id,post_id):
        """
            Get a User's specific post
            """
        #First get user who made the post
        user=User.get_by_id(user_id)
        #Second get posts made by the current user and filter by the user queryed for above via the backref in the user's table
        post=Post.query.filter_by(id=post_id).filter_by(blogger=user).first()
        
        #Return post and HTTPStatus
        return post, HTTPStatus.OK
    
    
#module for getting all post by a specific user
@post_namespace.route('/user/<int:user_id>/posts')
class UserPosts(Resource):
    #Return as a list of posts therefore we use marshal_list_with
    @post_namespace.marshal_list_with(post_model)
    #protect this end point via jwt_required
    @jwt_required()
    def get(self,user_id):
        """
            Get all posts by a specific user
        """
        #Make a query with the specific user id (import our User model from ..models.user)
        user=User.get_by_id(user_id)
        
        #Get posts attached or made by this specific user
        posts=user.posts
        
        #Return our posts and HTTPStatus
        return posts,HTTPStatus.OK