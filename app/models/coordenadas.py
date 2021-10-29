
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null
from app.db import db
from sqlalchemy import cast, Column, Integer, String, DateTime, Boolean, text, select, and_,or_, Float


class Coordenadas(db.Model):
    """
    
    """
    @classmethod
    def add_coords(cls,coords):
        db.session.add(coords)


    @classmethod
    def update_coords(cls):
        db.session.commit()

    
    @classmethod
    def get_or_create(cls,lat,long):
        coords = Coordenadas.query.filter((Coordenadas.lat==lat[:8])&(Coordenadas.long==long[:8])).first()
        print(coords)
        if not coords:
            coords = Coordenadas(lat=lat,long=long)
            Coordenadas.add_coords(coords=coords)
        return coords

    __tablename__ = 'coordenadas'
    id = Column(Integer, primary_key=True)
    constraint =  relationship("Denuncia",back_populates="coords")
    lat = Column(String(255))
    long = Column(String(255))

    def __init__(self,lat,long):
        self.lat = lat[:8]
        self.long = long[:8]


    def assign_constraint(self,constraint):
        self.constraint.append(constraint)
    

