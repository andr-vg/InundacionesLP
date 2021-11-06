class ZonasInundablesSchema(object):

    @classmethod
    def dump(cls, obj, many=False):
        if many:
            return cls._serialize_collection(obj)
        else:
            return {"atributos": cls._serialize(obj)}

    @classmethod
    def _serialize_collection(cls, pagination):
        return {
            "zonas": [cls._serialize(item) for item in pagination.items],
            "total": pagination.total,
            "pagina": pagination.page
        }

    @classmethod
    def _serialize(cls, obj):
        return {
            "id": obj.id,
            "nombre": obj.name,
            "coordenadas": [
                {"lat": coord.lat, "long": coord.long} for coord in obj.coords
            ],
            "color": obj.color,
        }