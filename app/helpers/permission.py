from app.models.user import User

# def check(user_id, permission):
#    return User.has_permission(user_id, permission)


def has_permission(permission, session):
    """
    Funcion que retorna si un dado permiso se encuentra en el listado
    de permisos de la sesión actual
    """
    return permission in session.get("permissions")
