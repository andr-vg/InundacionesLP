class PuntoEncuentroSchema(object):

    @classmethod
    def dump(cls,punto_encuentro):
        return {
            "name":punto_encuentro.name,
            "lat":punto_encuentro.lat,
            "long":punto_encuentro.long,
        }