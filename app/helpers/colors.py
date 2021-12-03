def get_translated_color(color):
    """
    Metodo que convierte el color obtenido en español de la BD
    a Ingles para ser utilizado en el mapa
    """
    colores = {"red": "Red", "blue": "Blue", "green": "Green", "yellow": "Yellow"}
    return colores[color]
