def check(filename):
    """
    Verifica que el archivo recibido tenga extension .csv
    Args:
        filename: Nombre del archivo a verificar
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() == "csv"
