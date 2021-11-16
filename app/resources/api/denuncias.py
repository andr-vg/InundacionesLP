from flask import jsonify,Blueprint,request,session
from werkzeug.wrappers import response
from app.models.categories import Categoria
from app.models.configuration import Configuration
from app.models.denuncias import Denuncia
from app.schema.denuncias import DenunciaSchema
from app.forms.denuncias import CreateDenunciaForm




denuncia_api = Blueprint("denuncias",__name__,url_prefix="/denuncias")


@denuncia_api.get("/")
def index():
    denuncias_iter= Denuncia.get_all()
    denuncias = [DenunciaSchema.dump(denuncia) for denuncia in denuncias_iter]
    return jsonify(denuncias)


@denuncia_api.get("/<int:page>")
def paginated(page):
    config = Configuration.get_configuration()
    per_page = int(request.args.get("per_page",config.elements_per_page))
    denuncias_page = Denuncia.get_paginated(page=int(page),config=config,elements_per_page=per_page)
    denuncias = DenunciaSchema.dump(denuncias_page,many=True)
    return jsonify(denuncias)


@denuncia_api.post("/")
def create():
    response = {}
    form = CreateDenunciaForm(**request.get_json())
    if form.validate_on_submit():
        if Denuncia.unique_field(form.title.data):
            return jsonify(response),400
        response = Denuncia(title=form.title.data,description=form.description.data,
        lat=form.lat.data,long=form.long.data,firstname=form.firstname.data,lastname=form.lastname.data,
        tel=form.tel.data,email=form.email.data)
        category = Categoria.get_category_by_id(form.category.data)
        if not category:
            return jsonify(response),400
        category.assign_complaints(response)
        response.add_denuncia()
        response.update_denuncia()
        response = DenunciaSchema.dump(response)
        return jsonify(response),201
    return jsonify(response),400