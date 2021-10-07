

from app.db import db
from sqlalchemy import Table,ForeignKey,Column,Integer,String
from sqlalchemy.orm import relationship
from app.models.permission import Permission


rol_permissions = Table('rol_tiene_permiso',db.Model.metadata,
    Column('roles_id',Integer,ForeignKey('roles.id'),primary_key=True),
    Column('permisos_id',Integer,ForeignKey('permisos.id'),primary_key=True)
)


class Rol(db.Model):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key = True)
    name = Column(String(30), unique = True)
    users=relationship("User",secondary='usuario_tiene_rol',back_populates='roles')  
    permissions=relationship("Permission",secondary=rol_permissions,back_populates='roles')

    def __init__(self, name):
        self.name = name
