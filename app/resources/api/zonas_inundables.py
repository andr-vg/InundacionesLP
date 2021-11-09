from flask import jsonify, Blueprint, request, make_response
from app.models.configuration import Configuration
from app.models.zonas_inundables import ZonaInundable
from app.schema.zonas_inundables import ZonasInundablesSchema

zonas_inundables_api = Blueprint("zonas_inundables", __name__, url_prefix="/zonas_inundables")


@zonas_inundables_api.get("/")
def index():
    config = Configuration.get_configuration()
    if not request.args:
        print("no hay params")
        zonas_page = ZonaInundable.get_all()
        zonas = ZonasInundablesSchema.dump(zonas_page, all=True)
        return jsonify(zonas)
    else:
        try:
            page = int(request.args.get("page", 1))
            per_page = int(request.args.get("per_page", config.elements_per_page))
            zonas_page = ZonaInundable.get_zonas_paginated(page, per_page)
            zonas = ZonasInundablesSchema.dump(zonas_page, many=True)
            return jsonify(zonas)
        except:
            return make_response(jsonify("Error 404 Not Found"), 404)

@zonas_inundables_api.get("/<id>")
def get(id):
    response = ZonaInundable.get_zona_by_id(id)
    if not response:
        return make_response(jsonify("Error 404 Not Found"), 404)
    zona = ZonasInundablesSchema.dump(response)
    return jsonify(zona)