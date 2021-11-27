from flask import jsonify, Blueprint, request, make_response
from app.models.configuration import Configuration
from app.models.recorridos_evacuacion import Recorridos
from app.schema.recorridos_evacuacion import RecorridosSchema

recorridos_evacuacion_api = Blueprint(
    "recorridos_evacuacion", __name__, url_prefix="/recorridos_evacuacion"
)


@recorridos_evacuacion_api.get("/")
def index():
    config = Configuration.get_configuration()
    if not request.args:
        recorridos_page = Recorridos.get_all_publicated(config)
        print("RESULTADO", recorridos_page)
        print("AAAA")
        recorridos = RecorridosSchema.dump(recorridos_page, all_=True)
        return jsonify(recorridos)
    else:
        try:
            page = int(request.args.get("page", 1))
            per_page = int(config.elements_per_page)
            # al traer paginado tengo que traer solo los que esten publicados
            recorridos_page = Recorridos.get_recorridos_paginated(
                page=page, config=config
            )
            recorridos = RecorridosSchema.dump(recorridos_page, many=True)
            return jsonify(recorridos)
        except:
            return make_response(jsonify("Error 404 Not Found"), 404)


@recorridos_evacuacion_api.get("/cercanos")
def nearest():
    config = Configuration.get_configuration()
    if request.args:
        recorridos_iter = Recorridos.get_all_publicated(config)
        try:
            lat = float(request.args.get("lat"))
            lon = float(request.args.get("lon"))
            nearest_points = sorted(
                recorridos_iter, key=lambda recorrido: recorrido.haversine(lat, lon)
            )[:5]
            response = [
                RecorridosSchema.dump(recorrido) for recorrido in nearest_points
            ]
        except:
            response = {
                "error_name": "400 Bad Request",
                "error_description": "Parametros invalidos",
            }
    else:
        response = {
            "error_name": "400 Bad Request",
            "error_description": "Requiere los parametros lat y lon",
        }
    return jsonify(response)


@recorridos_evacuacion_api.get("/<id>")
def get(id):
    response = Recorridos.get_recorrido_by_id(id)
    # si no devuelve nada o el estado es no publicado
    if not response or not response.state:
        return make_response(jsonify("Error 404 Not Found"), 404)
    recorrido = RecorridosSchema.dump(response)
    return jsonify(recorrido)
