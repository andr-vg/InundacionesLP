import uuid

from sqlalchemy.orm import relationship
from app.db import db
from sqlalchemy import Table, ForeignKey, Column, Integer, String, DateTime, Boolean, text, select, and_,or_
from app.models.coordenadas import Coordenadas

class ZonaInundable(db.model):
    """
    
    """
    __tablename__ = 'zonasInundables'
    id = Column(Integer, primary_key=True)
    code = Column(String(255), unique=True)
    name = Column(String(255), unique=True)
    state = Column(Boolean, default=False)
    color = Column(String(255))
    coords = relationship('Coordenadas', secondary='zona_tiene_coords', backref='zonasInundables')

    def __init__(self,name):
        self.code = self.generate_code()
        self.name = name


    def add_zona_inundable(self):
        db.session.add(self)


    def update_zona_inundable(self):
        db.session.commit()


    def generate_code(self):
        self.code = uuid.uuid1()


