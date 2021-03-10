from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import BIGINT
from datetime import datetime
db = SQLAlchemy()

class User(db.Model) :

    __tablename__="users"

    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=True)
    dob = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    role = db.Column(db.String, nullable= False)
    voted = db.Column(db.Boolean, nullable = False)

    def __init__(self, name, email, password, dateOfBirth, gender) :

        self.name = name
        self.email = email
        self.password = password
        self.dob = dateOfBirth
        self.gender = gender
        self.timestamp = datetime.now()
        self.role = "user"
        self.voted = False

class Candidate(db.Model):
    __tablename__ = "candidate"
    Id = db.Column(db.Integer, nullable = False, primary_key = True)
    Votes = db.Column(db.Integer, nullable = False)
    Name = db.Column(db.String(100), nullable = False)

    def __init__(self, Id, Votes, Name):
        self.Id = Id
        self.Votes = Votes
        self.Name = Name
