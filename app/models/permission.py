from app.db import db
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import relationship




class Permission(db.Model):
    """ Modelo que representa los permisos en el sistema """

    __tablename__ = 'permisos'
    id = Column(Integer, primary_key = True)
    name = Column(String(30), unique = True)
    roles = relationship('Rol',secondary='rol_tiene_permiso',back_populates='permissions')
   
   
    def __init__(self, name):
        self.name = name
