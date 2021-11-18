from flask import jsonify,Blueprint,request,session
from werkzeug.wrappers import response
from app.models.configuration import Configuration
from app.models.puntos_encuentro import PuntosDeEncuentro
from app.schema.puntos_encuentro import PuntoEncuentroSchema





puntos_encuentro_api = Blueprint("puntos",__name__,url_prefix="/puntos_encuentro")


@puntos_encuentro_api.get("/")
def index():
    puntos_iter= PuntosDeEncuentro.get_all()
    puntos = [PuntoEncuentroSchema.dump(punto) for punto in puntos_iter]
    return jsonify(puntos)


@puntos_encuentro_api.get("/<int:page>")
def paginated(page):
    config = Configuration.get_configuration()
    puntos_page = PuntosDeEncuentro.get_index_puntos_encuentro(page=int(page),config=config)
    puntos = PuntoEncuentroSchema.dump(puntos_page,many=True)
    return jsonify(puntos)
