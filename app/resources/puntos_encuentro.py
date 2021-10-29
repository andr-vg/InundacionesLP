from operator import not_
from flask import redirect, render_template, request, url_for, session, abort
from flask.helpers import flash
from app.helpers.configuration import get_configuration
from sqlalchemy.exc import OperationalError
from app.forms.puntos_encuentro import CreatePuntoEncuentro, EditPuntoEncuentro
from app.forms.user import EditUserForm
from app.models.puntos_encuentro import PuntosDeEncuentro
from app.models.user import User
from app.helpers.permission import has_permission as check_permission
from app.helpers.email import check as check_email
from app.helpers.auth import authenticated
from app.db import db


# Protected resources
def index(page):
    """Retorna y renderiza el listado de puntos de encuentro
    :param page:Numero de pagina para el paginado del listado
    :type page: int
    :raises: OperationalError
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("punto_encuentro_index", session):
        abort(401)
    config = get_configuration(session) 
    try:
        puntos_encuentro=PuntosDeEncuentro.get_index_puntos_encuentro(page, config)
    except OperationalError:
        flash("No hay puntos de encuentro aún.")
        puntos_encuentro = None
    return render_template("puntos_encuentro/index.html", puntos_encuentro=puntos_encuentro)


def new():
    """Retorna y renderiza el formulario para la creacion de un nuevo punto de encuentro"""
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("punto_encuentro_new", session):
        abort(401)
    form = CreatePuntoEncuentro()
    return render_template("puntos_encuentro/new.html", form=form)


def create():
    """Contiene la logica para la creacion de un punto de encuentro, 
    si el formulario es valido se carga en la base de datos."""
    if not authenticated(session):
        abort(401)
    if not check_permission("punto_encuentro_new", session):
        abort(401)
    form = CreatePuntoEncuentro(name=request.form["name"],address=request.form["address"],email=request.form["email"],tel=request.form["tel"],lat=request.form["lat"],long=request.form["long"])
    if form.validate():
        if PuntosDeEncuentro.unique_fields(form.name.data,form.address.data):
            flash("Uno o mas campos ya se encuentra cargado en el sistema")
            return render_template("puntos_encuentro/new.html", form=form)
        punto = PuntosDeEncuentro(name=form.name.data.upper(),address=form.address.data.upper(),tel=form.tel.data,email=form.email.data,lat=form.lat.data,long=form.long.data)
        punto.add_punto_encuentro()
        punto.update()
        flash("El nuevo punto de encuentro ha sido creado correctamente.")
        return redirect(url_for("punto_encuentro_index"))
    return render_template("puntos_encuentro/new.html",form=form)


def search():
    """Retorna el listado de puntos de encuentro filtrados con las opciones de búsqueda."""
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("punto_encuentro_index", session):
        abort(401)
    config = get_configuration(session)
    puntos_encuentro = PuntosDeEncuentro.search_by_name(request.args["name"])
    parameters = {
        "name": request.args["name"],
        "active": "",
    }
    if "active" in request.args.keys():
        parameters["active"] == request.args["active"]
    puntos_encuentro = PuntosDeEncuentro.filter_by_state(puntos_encuentro,request.args["active"])
    return render_template("puntos_encuentro/index.html", puntos_encuentro=puntos_encuentro, filter=1, parameters= parameters)


def edit():
    """" Retorna y renderiza el formulario para la edicion de un punto de encuentro. """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("punto_encuentro_update", session):
        abort(401)
    punto = PuntosDeEncuentro.get_punto_by_id(request.form['id'])
    form = EditPuntoEncuentro(id=punto.id,name=punto.name,address=punto.address,tel=punto.tel,email=punto.email,lat=punto.lat,long=punto.long)
    return render_template("puntos_encuentro/edit.html", form=form)


def update():
    """" Contiene la logica para la actualizacion de un punto de encuentro """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("punto_encuentro_update", session):
        abort(401)
    form = EditPuntoEncuentro(id=request.form["id"],name=request.form["name"],address=request.form["address"]
    ,email=request.form["email"],tel=request.form["tel"],lat=request.form["lat"],long=request.form["long"])
    if form.validate():
        punto = PuntosDeEncuentro.get_punto_by_id(form.id.data)
        query = PuntosDeEncuentro.get_punto_by_name(form.name.data)
        if query and punto.id!=query.id:
            flash("Ya se encuentra un punto de encuentro con dicho nombre en el sistema")
            return render_template("puntos_encuentro/new.html", form=form)
        query = PuntosDeEncuentro.get_punto_by_address(form.address.data)
        if query and punto.id!=query.id:
            flash("Ya se encuentra un punto de encuentro con dicha direccion en el sistema")
            return render_template("puntos_encuentro/new.html", form=form)
        punto.edit(name = form.name.data.upper(),address = form.address.data.upper()
        ,tel = form.tel.data,email = form.email.data,lat=form.lat.data,long=form.long.data)
        punto.update()
        flash("El punto de encuentro ha sido editado correctamente.")
        return redirect(url_for("punto_encuentro_index"))
    return render_template("puntos_encuentro/edit.html", form=form)


def soft_delete():
    """" Elimina un punto de encuentro logicamente mantenido con la variable state. """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission('punto_encuentro_edit',session):
        abort(401)
    punto_encuentro = PuntosDeEncuentro.get_punto_by_id(request.form["id"])
    punto_encuentro.change_state()
    punto_encuentro.update()
    state = "Publicado" if punto_encuentro.state else "Despublicado"
    flash("El punto de encuentro ha sido {} correctamente".format(state))
    return redirect(url_for("punto_encuentro_index"))


def show(name):
    """"" Vista detallada de un punto de encuentro """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("punto_encuentro_show", session):
        abort(401)
    punto = PuntosDeEncuentro.get_punto_by_name(name)
    return render_template("puntos_encuentro/show.html", pto=punto)


def delete():
    """" Elimina un punto de encuentro fisicamente """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission('punto_encuentro_destroy',session):
        abort(401)
    punto_encuentro = PuntosDeEncuentro.get_punto_by_id(request.form["id"])
    punto_encuentro.delete()
    punto_encuentro.update()
    flash("El punto de encuentro ha sido eliminado correctamente")
    return redirect(url_for("punto_encuentro_index"))
