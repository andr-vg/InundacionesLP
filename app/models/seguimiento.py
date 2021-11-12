import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import true
from app.db import db
from sqlalchemy import ForeignKey, Column, Integer, String, DateTime


class Seguimiento(db.Model):
    """
    Modelo que representa el seguimiento de una denuncia

    Args:
    id (int): Id del seguimiento
    description(string): descripcion del seguimiento
    created_at (date): fecha de creacion del seguimiento
    complaint_id (int): id de la denuncia a la cual pertenece el seguimiento
    complaints (denuncia): denuncia a la cual pertenece el seguimiento
    assigned_to (int): id del usuario autor del seguimiento
    user_assign (user): usuario autor del seguimiento
    """
    __tablename__ = 'seguimientos'
    id = Column(Integer,primary_key=True)
    description = Column(String(255))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    complaint_id = Column(Integer, ForeignKey('denuncias.id'))
    complaints = relationship("Denuncia", back_populates="tracking")
    assigned_to = Column(Integer, ForeignKey('usuarios.id'))
    user_assign = relationship("User", back_populates="tracking")


    def get_tracking(page, config,denuncia_id):
        """" Retorna el listado de seguimientos asignados a la denuncia recibida por parametro
        ordenado con la configuracion del sistema y paginado con
        la cantidad de elementos por pagina definidos en la configuracion del sistema.
        :param page:Numero entero que representa la pagina.
        :param config: Representa la configuracion del sistema.
        :param denuncia_id: Numero entero que representa la denuncia """
        if config.ordered_by == "Ascendente":
            return Seguimiento.query.filter(Seguimiento.complaint_id==denuncia_id).order_by(Seguimiento.created_at.asc()).paginate(page, per_page=config.elements_per_page)
        return Seguimiento.query.filter(Seguimiento.complaint_id==denuncia_id).order_by(Seguimiento.created_at.desc()).paginate(page, per_page=config.elements_per_page)


    def update_seguimiento(self):
        db.session.commit()