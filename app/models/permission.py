from app.db import db
from sqlalchemy import Column,Integer,String





class Permission(db.Model):
    __tablename__ = "Permisos"
    id = Column(Integer, primary_key = True)
    name = Column(String(30), unique = True)

    def __init__(self, name):
        self.name = name
