import uuid

from sqlalchemy.orm import relationship
from app.db import db
from sqlalchemy import Table, ForeignKey, Column, Integer, String, DateTime, Boolean, text, select, and_,or_


class ZonaInundable(db.Model):
    """
    
    """
    zona_tiene_coords = Table('zona_tiene_coords', db.Model.metadata,
    Column('zonasInundables_id', ForeignKey('zonasInundables.id'), primary_key=True),
    Column('coordenadas_id', ForeignKey('coordenadas.id'), primary_key=True)
)

    __tablename__ = 'zonasInundables'
    id = Column(Integer, primary_key=True)
    code = Column(String(255), unique=True)
    name = Column(String(255), unique=True)
    state = Column(Boolean, default=False)
    color = Column(String(255), nullable=True)
    coords = relationship('Coordenadas', secondary='zona_tiene_coords', backref='zonasInundables')

    def __init__(self,name,state=True):
        self.code = self.generate_code()
        self.name = name
        self.state = state


    def add_zona_inundable(self):
        db.session.add(self)


    def update_zona_inundable(self):
        db.session.commit()


    def generate_code(self):
        return uuid.uuid4()



