import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import true
from app.db import db
from sqlalchemy import ForeignKey, Column, Integer, String, DateTime

class Seguimiento(db.Model):
    """
    
    """
    __tablename__ = 'seguimientos'
    id = Column(Integer,primary_key=True)
    description = Column(String(255))
    author = Column(Integer,ForeignKey('usuarios.id'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)