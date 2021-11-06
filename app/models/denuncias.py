import datetime,enum
from sqlalchemy.orm import relationship
from app.db import db
from app.models.coordenadas import Coordenadas
from sqlalchemy import Enum, ForeignKey, Column, Integer, String, DateTime, Boolean, text, select, and_,or_, Float

class State(enum.Enum):
    sin_confirmar = "Sin confirmar"
    en_curso = "En curso"
    resuelta = "Resuelta"
    cerrada = "Cerrada"

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]


        
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
    category_id = Column(Integer, ForeignKey('categorias.id'))
    category =  relationship("Categoria", back_populates="complaints")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    closed_at = Column(DateTime, default=None)
    description = Column(String(255))
    state = Column(Enum(State), default=State.sin_confirmar)
    lat = Column(Float)
    long = Column(Float)
    firstname = Column(String(255))
    lastname = Column(String(255))
    tel = Column(String(255))
    email = Column(String(255))
    assigned_to = Column(Integer, ForeignKey('usuarios.id'))
    user_assign = relationship("User", back_populates="complaints")
    tracking = relationship("Seguimiento", back_populates="complaints")

    def as_dict(self):
        return {attr.name: getattr(self,attr.name) for attr in self.__table__.columns}


    def edit(self,title,description,lat,long,firstname,lastname,tel,email):
        self.title = title
        self.description = description
        self.lat = lat
        self.long = long
        self.firstname = firstname
        self.lastname = lastname
        self.tel = tel
        self.email = email



    def add_denuncia(self):
        db.session.add(self)


    def update_denuncia(self):
        db.session.commit()
    

    def delete_denuncia(self):
        db.session.delete(self)

    def assign_tracking(self,seguimiento):
        """ Asigna el seguimiento a la relacion """
        self.tracking.append(seguimiento)
    
    def disassign_user(self):
        self.assigned_to=None

    def disassign_category(self):
        self.category_id=None
     
    def change_state(self,state):
        self.state = state
        if state == State.cerrada:
            self.closed_at = datetime.datetime.utcnow()
    
    
    def is_closed(self):
        return self.state==State.cerrada

    def get_index_denuncias(page, config):
        """" Retorna el listado de denuncias ordenado con la configuracion del sistema y paginado con
        la cantidad de elementos por pagina definidos en la configuracion del sistema.
        :param page:Numero entero que representa la pagina.
        :param config: Representa la configuracion del sistema. """
        if config.ordered_by == "Ascendente":
            return Denuncia.query.order_by(Denuncia.created_at.asc()).paginate(page, per_page=config.elements_per_page)
        return Denuncia.query.order_by(Denuncia.created_at.desc()).paginate(page, per_page=config.elements_per_page)


    def get_denuncias_paginated(page,elements_per_page):
        return Denuncia.query.paginate(page, per_page=elements_per_page)


    def get_by_id(id):
        """ Retorna la denuncia con el id recibido por parametro """
        return Denuncia.query.filter(Denuncia.id==id).first()

    
    def get_by_title(title):
        """ Retorna la denuncia con el titulo recibido por parametro """
        return Denuncia.query.filter(Denuncia.title==title).first()

    
    def get_index_denuncias_assigned(page,config,id):
        """" Retorna el listado de denuncias asignadas ordenado con la configuracion del sistema y paginado con
        la cantidad de elementos por pagina definidos en la configuracion del sistema.
        :param page:Numero entero que representa la pagina.
        :param config: Representa la configuracion del sistema. """
        if config.ordered_by == "Ascendente":
            return Denuncia.query.filter(Denuncia.assigned_to==id).order_by(Denuncia.created_at.asc()).paginate(page, per_page=config.elements_per_page)
        return Denuncia.query.filter(Denuncia.assigned_to==id).order_by(Denuncia.created_at.desc()).paginate(page, per_page=config.elements_per_page)