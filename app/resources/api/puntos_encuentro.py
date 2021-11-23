from flask import jsonify, Blueprint, request, session
from werkzeug.wrappers import response
from app.models.configuration import Configuration
from app.models.puntos_encuentro import PuntosDeEncuentro
from app.schema.puntos_encuentro import PuntoEncuentroSchema


puntos_encuentro_api = Blueprint("puntos", __name__, url_prefix="/puntos_encuentro")


@puntos_encuentro_api.get("/")
def index():
    config = Configuration.get_configuration()
    if not request.args:
        puntos_iter = PuntosDeEncuentro.get_all(config)
        response = [PuntoEncuentroSchema.dump(punto) for punto in puntos_iter]
    else:
        try:
            page = request.args.get("page")
            puntos_iter = PuntosDeEncuentro.get_index_puntos_encuentro(
                int(page), config
            )
            response = PuntoEncuentroSchema.dump(puntos_iter, many=True)
        except:
            response = {
                "error_name": "400 Bad Request",
                "error_description": "Numero de pagina invalido",
            }
    response = jsonify(response)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@puntos_encuentro_api.get("/<int:id>")
def paginated(id):
    response = PuntosDeEncuentro.get_punto_by_id(id)
    if not response:
        response = {
            "error_name": "400 Bad Request",
            "error_description": "No existe un punto con dicho id",
        }
        return jsonify(response)
    response = PuntoEncuentroSchema.dump(response)
    return jsonify(response)
