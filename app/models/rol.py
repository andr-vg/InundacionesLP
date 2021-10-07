

from app.db import db
from sqlalchemy import Table,ForeignKey,Column,Integer,String
from sqlalchemy.orm import relationship

rol_permissions = Table('rol_tiene_permiso',db.Model.metadata,
    Column('roles',Integer,ForeignKey('roles.id'),primary_key=True),
    Column('permisos',Integer,ForeignKey('permisos.id'),primary_key=True)
)


class Rol(db.Model):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key = True)
    name = Column(String(30), unique = True)
    users=relationship('User',secondary='usurio_tiene_rol')  
    permissions=relationship('Permission',secondary='rol_tiene_permiso')

    def __init__(self, name):
        self.name = name
