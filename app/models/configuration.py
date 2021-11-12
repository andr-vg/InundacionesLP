import datetime

from app.db import db
from sqlalchemy import Column,Integer,String

class Configuration(db.Model):
    """" Modelo que representa la configuracion del sistema """
    @classmethod
    def get_configuration(cls):
        """ Retorna la configuracion del sistema """
        return Configuration.query.first()

    __tablename__ = 'configuracion'
    id = Column(Integer, primary_key=True)
    elements_per_page = Column(Integer,default=15)
    ordered_by = Column(String(30),default="Ascendente")
    css_private = Column(String(30),default="app/static/style.css")
    css_public = Column(String(30),default="app/static/style.css")

    def __init__(self, elements_per_page, ordered_by, css_private, css_public):
        self.elements_per_page = elements_per_page
        self.ordered_by = ordered_by
        self.css_private = css_private
        self.css_public = css_public

    def edit(self,elements_per_page,ordered_by,css_private,css_public):
        """ Asigna los parametros recibidos a la configuracion """
        self.elements_per_page = elements_per_page
        self.ordered_by = ordered_by
        self.css_private = css_private
        self.css_public = css_public

    
    def update(self):
        db.session.commit()