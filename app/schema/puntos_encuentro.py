class PuntoEncuentroSchema(object):
    """ Clase para serializar los Puntos de encuentro """


    @classmethod
    def dump(cls,punto_encuentro):
        """ Serializa un punto de encuentro recibido por parametro y retorna un dict con las claves name, lat y long."""
        return {
            "name":punto_encuentro.name,
            "lat":punto_encuentro.lat,
            "long":punto_encuentro.long,
        }