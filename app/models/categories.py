from sqlalchemy.orm import relationship
from app.db import db
from app.models.coordenadas import Coordenadas
from sqlalchemy import Enum, ForeignKey, Column, Integer, String, DateTime, Boolean, text, select, and_,or_, Float


class Categoria(db.Model):
    """
    Modelo que representa la categoria de una denuncia
     
    Args:
    id (int): Id de la categoria
    name (string): Nobmre de la categoria
    complaints (list): lista de denuncias asignadas a dicha categoria
    """


    __tablename__ = 'categorias'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    complaints = relationship("Denuncia", back_populates="category")


    def get_all():
        """ Retorna el listado de categorias """
        return Categoria.query.all()


    def get_category_by_id(id):
        """ Retorna la categoria con el id pasado por parametro, si no existe devuelve none"""
        return Categoria.query.filter(Categoria.id==id).first()

    def assign_complaints(self,complaint):
        """Asigna la denuncia a la relacion"""
        self.complaints.append(complaint)
    

