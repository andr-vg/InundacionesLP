class ZonasInundablesSchema(object):
    """
    Clase utilizada para la serialización de los objetos
    del modelo de zonas inundables
    """

    @classmethod
    def dump(cls, obj, per_page=False, many=False, all=False):
        if all:
            return cls._serialize_collection_all(obj)
        elif many and per_page:
            return cls._serialize_collection(obj, per_page)
        else:
            return {"atributos": cls._serialize(obj)}

    @classmethod
    def _serialize_collection_all(cls, zones):
        return {
            "zonas": [cls._serialize(item) for item in zones],
            "total": [len(zones)],
        }

    @classmethod
    def _serialize_collection(cls, pagination, per_page):
        return {
            "zonas": [cls._serialize(item) for item in pagination.items],
            "total": pagination.total,
            "pagina": pagination.page,
            "por_pagina": per_page,
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
            "codigo": obj.code,
        }
