#importing the package for testing
import unittest
#importing our create app function within from our main init.py
from .. import create_app
#import our config to use our confi_dict and set it to test case 
from ..config.config import config_dict
#Importing our db to access our database
from ..utils import db
#importing generate_password_hash from werkzeug 
from werkzeug.security import generate_password_hash
from ..models.users import User
from flask_jwt_extended import create_access_token, create_refresh_token


#creating test case class that comes from unittest
class AdminTestCaseClass(unittest.TestCase):
    #write a tear down and set up functions
    def setUp(self):
        #set up our app
        self.app=create_app(config=config_dict['test'])
        #create an app context and this app to our application context
        #create an app context
        self.appctx = self.app.app_context()
        #push current app to our app context
        self.appctx.push()
        
        #Create a test client which gives us the ability to test our API
        self.client=self.app.test_client()
        #create our database using the configuration, we defined in our config (import our db from the utils folder)
        db.create_all()
        
        
    
    #this destroy our database tables after it has been tested
    def tearDown(self):
        #destroy all our database
        db.drop_all()
        
        #pop the app context
        self.appctx.pop()
        #set our app to none
        self.app=None
        #Alsp, we set our client to none
        self.client=None



    
    def test_api_get_all_(self):
        access_token = create_access_token(identity='test@gmail.com')
        headers={
            "Authorization":f"Bearer {access_token}"
        }
        response = self.client.post('/user/add', json={
            "username":"test-firstname",
            "fullname":"test-lastname",
            "email":"test@gmail.com",
            "password_hash": "password",
            "about_author":"I love youtube post"
        },headers=headers)
        assert response.status_code == 201
        
        response = self.client.get('/admin/get-all')
        assert response.status_code == 200

        # make sure the user is in the database
        user=User.query.all()
        assert user is not None
        assert user.email == 'test@gmail.com'
        
        #install pytest in order to run the test(pip install pytest)