#To Create our user table we first import our db instance from utils
from ..utils import db 
from datetime import datetime



#Create our table in form of classes
class Enquiry(db.Model):
    __tablename__='enquiries'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(200), nullable=False)
    enquiry = db.Column(db.Text(500), nullable=False)
    date_of_complain = db.Column(db.DateTime, default=datetime.utcnow)
    
    
    
    #Create a string representation
    def __repr__(self):
        return f"<Enquiry {self.id}>"
    
    
    #special function that allows one to delete a post
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    #Special function to allow us query for a post by its ID
    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)