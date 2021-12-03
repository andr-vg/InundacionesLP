from flask import jsonify, Blueprint, request, session
from app.models.configuration import Configuration
from app.schema.configuration import ConfiguracionSchema


configuracion_api = Blueprint("configuracion", __name__, url_prefix="/configuracion")


@configuracion_api.get("/")
def index():
    config = Configuration.get_configuration()
    if config:
        response = ConfiguracionSchema.dump(config)
    else:
        response = {
            "error_name": "400 Bad Request",
            "error_description": "No se pudo obtener la configuracion",
        }
    return jsonify(response)
