class DenunciaSchema(object):
    """" Clase para serializar los objetos del modelo Denuncia """


    @classmethod
    def dump(cls,obj,many=False):
        """" Recibe el objeto y un booleano que indica si es una coleccion  y devuelve el objeto serializado"""
        if many:
            return cls._serialize_collection(obj)
        else:
            return cls._serialize(obj)

    @classmethod
    def _serialize_collection(cls,pagination):
        """ Serializa una coleccion de objetos recibido como un objeto Paginacion """
        return {
            "page":pagination.page,
            "per_page":pagination.per_page,
            "total":pagination.total,
            "denuncias":[cls._serialize(item) for item in pagination.items],
        }

    @classmethod
    def _serialize(cls,obj):
        """ Serializa un unico objeto """
        return {
            "categoria_id":obj.category_id,
            "coordenadas":str(obj.lat) +","+str(obj.long),
            "apellido_denunciante":obj.lastname,
            "nombre_denunciante":obj.firstname,
            "telcel_denunciante":obj.tel ,
            "email_denunciante": obj.email,
            "titulo": obj.title,
            "descripcion":obj.description,
        }