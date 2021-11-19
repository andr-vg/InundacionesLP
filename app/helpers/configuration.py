def get_configuration(session):
    """
    Retorna la configuracion actual del sistema
    """
    return session.get("config")