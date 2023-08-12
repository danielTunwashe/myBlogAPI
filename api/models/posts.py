#Import our db instance
from ..utils import db
from datetime import datetime


#Create our table in form of classes
class Post(db.Model):
    __tablename__='posts'
    id=db.Column(db.Integer(),primary_key=True)
    title = db.Column(db.String(255),nullable=False)
    content = db.Column(db.Text(500),nullable=False)
    date_posted = db.Column(db.DateTime(), default = datetime.utcnow)
    slug = db.Column(db.String(255),nullable=False)
    user=db.Column(db.Integer(),db.ForeignKey('users.id'))
    
    
    #Create a string representation
    def __repr__(self):
        return f"<Post {self.id}>"
    
    #Special function to help us save our posts to the database
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    #Special function to allow us query for a post by its ID
    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)
    
    
    #special function that allows one to delete a post
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        