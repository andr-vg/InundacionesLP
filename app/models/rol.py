

from app.db import db
from sqlalchemy import Table,ForeignKey,Column,Integer,String
from sqlalchemy.orm import relationship
from app.models.permission import Permission


rol_permissions = Table('rol_tiene_permiso',db.Model.metadata,
    Column('roles_id',ForeignKey('roles.id'),primary_key=True),
    Column('permisos_id',ForeignKey('permisos.id'),primary_key=True)
)


class Rol(db.Model):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key = True)
    name = Column(String(30), unique = True)
    users=relationship("User",secondary='usuario_tiene_rol',back_populates='roles')  
    permissions=relationship("Permission",secondary=rol_permissions,back_populates='roles')

    def __init__(self, name):
        self.name = name

    def get_all_roles():
        return Rol.query.all()

    def get_rol_by_id(id):
        return Rol.query.filter(Rol.id==id).first()

    def get_rol_by_name(name):
        return Rol.query.filter(Rol.name==name).first()