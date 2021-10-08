import datetime

from app.db import db
from sqlalchemy import Column,Integer,String

class Configuration(db.Model):
    __tablename__ = 'configuracion'
    id = Column(Integer, primary_key=True)
    number_pages = Column(Integer)
    elements_per_page = Column(Integer)
    ordered_by = Column(String(30))
    css_private = Column(String(30))
    css_public = Column(String(30))

    def __init__(self, number_pages, elements_per_page, ordered_by, css_private, css_public):
        self.number_pages = number_pages
        self.elements_per_page = elements_per_page
        self.ordered_by = ordered_by
        self.css_private = css_private
        self.css_public = css_public