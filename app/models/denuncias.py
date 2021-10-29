import datetime
from sqlalchemy.orm import relationship
from app.db import db
from app.models.coordenadas import Coordenadas
from sqlalchemy import Table, ForeignKey, Column, Integer, String, DateTime, Boolean, text, select, and_,or_, Float



class Denuncia(db.Model):
    """
    
    """
    @classmethod
    def unique_field(cls, title):
        """
        Verifica si ya existe una denuncia con el titulo recibido por parametro

        Args:
            title: String
        Returns:
            El resultado de la consulta con la denuncia existente caso contrario None
        """
        denuncia = Denuncia.query.filter(Denuncia.title == title).first()
        return denuncia




    __tablename__ = 'denuncias'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), unique=True)
    category = Column(String(255))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    closed_at = Column(DateTime, default=None)
    description = Column(String(255), unique=True)
    state = Column(String(255))
    firstname = Column(String(255))
    lastname = Column(String(255))
    tel = Column(String(255))
    email = Column(String(255))
    assigned_to = Column(Integer, ForeignKey('usuarios.id'))
    user_assign = relationship("User", back_populates="complaints")
    id_coords = Column(Integer,ForeignKey("coordenadas.id"))
    coords = relationship("Coordenadas",back_populates="constraint")


    
    def add_denuncia(self):
        db.session.add(self)


    def update_denuncia(self):
        db.session.commit()

    
    def assign_coords(self,coords):
        self.coords.append(coords)


    def get_index_denuncias(page, config):
        """" Retorna el listado de denuncias ordenado con la configuracion del sistema y paginado con
        la cantidad de elementos por pagina definidos en la configuracion del sistema.
        :param page:Numero entero que representa la pagina.
        :param config: Representa la configuracion del sistema. """
        if config.ordered_by == "Ascendente":
            return Denuncia.query.order_by(Denuncia.title.asc()).paginate(page, per_page=config.elements_per_page)
        return Denuncia.query.order_by(Denuncia.title.desc()).paginate(page, per_page=config.elements_per_page)