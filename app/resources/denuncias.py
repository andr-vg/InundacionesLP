from flask import redirect, render_template, request, url_for, session, abort
from flask.helpers import flash
from app.helpers.configuration import get_configuration
from app.helpers.permission import has_permission as check_permission
from app.helpers.email import check as check_email
from app.helpers.auth import authenticated
from sqlalchemy.exc import OperationalError
from app.models.denuncias import Denuncia
from app.models.coordenadas import Coordenadas
from app.forms.denuncias import CreateDenunciaForm

def index(page):
    """Retorna y renderiza el listado de denuncias
    :param page:Numero de pagina para el paginado del listado
    :type page: int
    :raises: OperationalError
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("denuncias_index", session):
        abort(401)
    config = get_configuration(session) 
    try:
        denuncias = Denuncia.get_index_denuncias(page, config)
    except OperationalError:
        flash("No hay puntos de encuentro aún.")
        denuncias = None
    return render_template("denuncias/index.html", denuncias=denuncias)


def new():
    """Retorna y renderiza el formulario para la creacion de una nueva denuncia"""
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("denuncias_new", session):
        abort(401)
    form = CreateDenunciaForm()
    return render_template("denuncias/new.html", form=form)


def create():
    """Contiene la logica para la creacion de una nueva denuncia, 
    si el formulario es valido se carga en la base de datos."""
    if not authenticated(session):
        abort(401)
    if not check_permission("denuncias_new", session):
        abort(401)
    form = CreateDenunciaForm(title=request.form["title"],category=request.form["category"],
    description=request.form["description"],lat=request.form["lat"],long=request.form["long"],
    firstname=request.form["firstname"],lastname=request.form["lastname"],tel=request.form["tel"],
    email=request.form["email"])
    if form.validate():
        if Denuncia.unique_field(form.title.data):
            flash("Ya se encuentra cargada una denuncia con dicho titulo en el sistema")
            return render_template("denuncias/new.html", form=form)
        denuncia = Denuncia(title=form.title.data,category=form.category.data,description=form.description.data,
        firstname=form.firstname.data,lastname=form.lastname.data,tel=form.tel.data,email=form.email.data)
        coords = Coordenadas.get_or_create(form.lat.data,form.long.data)
        coords.assign_constraint(denuncia)
        denuncia.add_denuncia()
        denuncia.update_denuncia()
        flash("La denuncia ha sido creado correctamente.")
        return redirect(url_for("denuncia_index"))
    return render_template("denuncias/new.html",form=form)