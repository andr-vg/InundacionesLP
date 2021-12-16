from app.models.user import User


def authenticated(session):
    """
    Retorna el email del usuario autenticado
    """
    return session.get("user")


def get_pending_state(session):
    """
    Retorna 1 si el usuario esta pendiente, 0 si no lo esta
    """
    user = User.get_user_by_email(session.get("user"))
    return user.pending
