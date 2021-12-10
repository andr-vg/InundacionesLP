from app.models.user import User
from app.models.denuncias import Denuncia


def has_tracking(session):
    "Retorna si el usuario actual tiene seguimietos"
    user = User.get_user_by_email(session.get("user"))
    denuncias_asignadas = Denuncia.get_assigned(user.id)
    if denuncias_asignadas:
        return True
    return False
