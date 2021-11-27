from flask import jsonify, Blueprint, request, session
from app.models.categories import Categoria
from app.schema.categorias import CategoriaSchema


categoria_api = Blueprint("categorias", __name__, url_prefix="/categorias")


@categoria_api.get("/")
def index():
    categoria_iter = Categoria.get_all()
    if categoria_iter:
        response = CategoriaSchema.dump(categoria_iter, many=True)
    else:
        response = {
            "error_name": "400 Bad Request",
            "error_description": "No se pudieron obtener las categorias",
        }
    return jsonify(response)
