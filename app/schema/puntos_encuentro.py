class PuntoEncuentroSchema(object):
    """ " Clase para serializar los objetos del modelo Denuncia"""

    @classmethod
    def dump(cls, obj, many=False):
        """ " Recibe el objeto y un booleano que indica si es una coleccion  y devuelve el objeto serializado"""
        if many:
            return cls._serialize_collection(obj)
        else:
            return cls._serialize(obj)

    @classmethod
    def _serialize_collection(cls, pagination):
        """Serializa una coleccion de objetos recibido como un objeto Paginacion"""
        return {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "Puntos de encuentro": [cls._serialize(item) for item in pagination.items],
        }

    @classmethod
    def _serialize(cls, obj):
        """Serializa un unico objeto"""
        return {
            "name": obj.name,
            "coords": str(obj.lat) + "," + str(obj.long),
            "email": obj.email,
            "address": obj.address,
            "state": obj.state,
            "tel": obj.tel,
            "created_at:": obj.created_at,
            "updated_at": obj.updated_at,
        }
