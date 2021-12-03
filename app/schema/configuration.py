class ConfiguracionSchema(object):
    """ " Clase para serializar los objetos del modelo Configuracion"""

    @classmethod
    def dump(cls, obj):
        """Serializa un unico objeto"""
        return {
            "elements_per_page": obj.elements_per_page,
            "ordered_by": obj.ordered_by,
            "css_private": obj.css_private,
            "css_public": obj.css_public,
        }
