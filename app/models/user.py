import datetime

from app.db import db
from sqlalchemy import Column,Integer,String,DateTime,Boolean
from sqlalchemy.orm import relationship


class User(db.Model):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key = True)
    firstname = Column(String(30))
    lastname = Column(String(30))
    username = Column(String(30), unique = True)
    email = Column(String(30), unique = True)
    password = Column(String(30))
    active = Column(Boolean, default = True)
    updated_at = Column(DateTime, default = None)
    created_at = Column(DateTime, default = datetime.datetime.utcnow)

    def __init__(self, email, password, username , firstname=None, lastname=None):
        self.email = email
        self.password = password
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
