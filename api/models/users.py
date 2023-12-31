#To Create our user table we first import our db instance from utils
from ..utils import db 
from datetime import datetime

#Then, we create our databse table via classes

class User(db.Model):
#first define the table name
    __tablename__='users'
    id=db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(45),nullable=False,unique=True)
    fullname=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(50),nullable=False,unique=True)
    about_author=db.Column(db.String(100),nullable=False)
    date_added = db.Column(db.DateTime(), default=datetime.utcnow)
    password_hash=db.Column(db.Text(),nullable=False)
    is_staff=db.Column(db.Boolean(),default=False)
    posts=db.relationship('Post',backref='blogger',lazy=True)
    
#Special function to return a string representation of these objects
    def __repr__(self):
        return f"<User {self.username}>"
    
#Special function to help us save our new user
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    #Special function to allow us query a specific user by its ID
    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)
    
    #special function that allows one to delete a post
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    