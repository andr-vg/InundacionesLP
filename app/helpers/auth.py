def authenticated(session):
    """
    Retorna el email del usuario autenticado
    """
    return session.get("user")