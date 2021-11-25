class RecorridosSchema(object):
    """
    Clase utilizada para la serialización de los objetos
    del modelo de recorridos de evacuación
    """

    @classmethod
    def dump(cls, obj, many=False, all_=False):
        if all_:
            return cls._serialize_collection_all(obj)
        elif many:
            return cls._serialize_collection(obj)
        else:
            return cls._serialize(obj)

    @classmethod
    def _serialize_collection_all(cls, recorridos):
        return {
            "recorridos": [cls._serialize(item) for item in recorridos],
            "total": [len(recorridos)],
        }

    @classmethod
    def _serialize_collection(cls, pagination):
        return {
            "recorridos": [cls._serialize(item) for item in pagination.items],
            "total": pagination.total,
            "pagina": pagination.page,
        }

    @classmethod
    def _serialize(cls, obj):
        return {
            "id": obj.id,
            "nombre": obj.name,
            "coordenadas": [
                {"lat": coord.lat, "long": coord.long} for coord in obj.coords
            ],
            "descripcion": obj.description,
        }
