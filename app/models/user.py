import datetime

from sqlalchemy.sql.expression import null

from app.db import db
from sqlalchemy import Table,ForeignKey,Column,Integer,String,DateTime,Boolean
from sqlalchemy.orm import relationship


user_roles = Table('usuario_tiene_rol',db.Model.metadata,
    Column('usuarios',Integer,ForeignKey('usuarios.id'),primary_key=True),
    Column('roles',Integer,ForeignKey('roles.id'),primary_key=True)
)

class User(db.Model):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    firstname = Column(String(30))
    lastname = Column(String(30))
    username = Column(String(30), unique=True)
    email = Column(String(30), unique=True)
    password = Column(String(30))
    roles = relationship('Rol',secondary='usuario_tiene_rol')
    active = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=None)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, email, password, username ,roles=None, firstname=None, lastname=None):
        self.email = email
        self.password = password
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
