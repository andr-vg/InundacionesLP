
from app.schema.puntos_encuentro import PuntoEncuentroSchema
from flask import json

def tojson(puntos_encuentro):
    puntos = [PuntoEncuentroSchema.dump(punto) for punto in puntos_encuentro]
    return json.dumps(puntos)