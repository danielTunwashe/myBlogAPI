#seting up our flask server
from flask import Flask
#importing our namespaces to our server
from .posts.views import post_namespace
from .auth.views import auth_namespace
from .admin.views import admin_namespace
from flask_restx import Api
#importing our configuration dictionary from config folder
from .config.config import config_dict
#Import our db instance and database model to set up our tables created
from .utils import db
from .models.posts import Post
from .models.users import User
from .models.enquiries import Enquiry
from flask_migrate import Migrate
#Setting up JWT_Extended to work with our application
from flask_jwt_extended import JWTManager
#Importing some of the classes that will be used for creating custom errors from werkzeug
from werkzeug.exceptions import NotFound, MethodNotAllowed



#Setting up our flask server
#Give our application factory an argument after importing our config_dict
def create_app(config=config_dict['dev']):
    app=Flask(__name__)
    
    #Hook our configuration to our app instace, make sure it just after our main server
    app.config.from_object(config)
    
    
    
    
    
    #impoerting our namespaces to our server
    api = Api(app)
    
    api.add_namespace(post_namespace)
    api.add_namespace(auth_namespace)
    api.add_namespace(admin_namespace)
    
    #Hooking our database model to our application
    db.init_app(app)
    
    migrate = Migrate(app,db)
    
    #Setting up our jwt_extended to our main application
    jwt=JWTManager(app)
    
    #Creating custom error handler to handle most of our errors by using werkzeug exception classes, we therefore import some of the classes
    @api.errorhandler(NotFound)
    #creating a function to handle our not_found error
    def not_found(error):
        return {"error":"Not Found"},404
      
    #Creating custom error handler to handle most of our errors by using werkzeug exception classes, we therefore import some of the classes
    @api.errorhandler(MethodNotAllowed)
    #creating a function to handle our not_found error
    def method_not_allowed(error):
        return {"error":"Method not allowed"},405
    
    
    #creating a context within a shell to access our modules and db instance
    @app.shell_context_processor
    def make_shell_context():
        return{
            'db':db,
            'User':User,
            'Post':Post,
            'Enquiry':Enquiry
        }
    
    return app