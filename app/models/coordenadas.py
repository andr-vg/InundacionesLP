from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import foreign
from app.db import db
from sqlalchemy import Table, ForeignKey, Column, Integer, String, DateTime, Boolean, text, select, and_,or_, Float

class Coordenadas(db.model):
    """
    
    """
    __tablename__ = 'coordenadas'
    id = Column(Integer, primary_key=True)
    id_zona = Column(Integer, ForeignKey('zonasInundables.id'))
    lat = Column(Float)
    long = Column(Float)
    
    