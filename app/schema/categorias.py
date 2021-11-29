class CategoriaSchema(object):
    """ " Clase para serializar los objetos del modelo Categoria"""

    @classmethod
    def dump(cls, obj, many=False):
        """ " Recibe el objeto y un booleano que indica si es una coleccion  y devuelve el objeto serializado"""
        if many:
            return cls._serialize_collection(obj)
        else:
            return cls._serialize(obj)

    @classmethod
    def _serialize_collection(cls, list):
        """Serializa una coleccion de objetos recibido como una lista"""
        return [cls._serialize(item) for item in list]

    @classmethod
    def _serialize(cls, obj):
        """Serializa un unico objeto"""
        return {
            "id": obj.id,
            "name": obj.name,
        }
