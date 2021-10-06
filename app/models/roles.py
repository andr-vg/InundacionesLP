from app.db import db
from sqlalchemy.orm import relationship
from sqlalchemy import Column,Integer,String


class Rol(db.Model):
    __tablename__ = "roles"
    id = Column(Integer, primary_key = True)
    name = Column(String(30), unique = True)
 
    def __init__(self, name):
        self.name = name
