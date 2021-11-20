from flask import redirect, render_template, request, url_for, session, abort
from flask.helpers import flash
from app.helpers.configuration import get_configuration
from app.helpers.permission import has_permission as check_permission
from app.helpers.email import check as check_email
from app.helpers.auth import authenticated
from sqlalchemy.exc import OperationalError
from app.models.categories import Categoria
from app.models.denuncias import Denuncia
from app.models.seguimiento import Seguimiento
from app.forms.denuncias import CreateDenunciaForm, EditDenunciaForm
from app.models.user import User


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
        flash("No hay denuncias aún.")
        denuncias = None
    return render_template("denuncias/index.html", denuncias=denuncias)


def index_assigned(page):
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
    user_id = User.get_id_from_email(user_email)
    denuncias = Denuncia.get_index_denuncias_assigned(page, config, user_id)
    if not denuncias.items:
        abort(401)
    return render_template("denuncias/tracking.html", denuncias=denuncias)


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
    form = CreateDenunciaForm(request.form)
    if form.validate():
        if Denuncia.unique_field(form.title.data):
            flash("Ya se encuentra cargada una denuncia con dicho titulo en el sistema")
            return render_template("denuncias/new.html", form=form)
        denuncia = Denuncia(
            title=form.title.data,
            description=form.description.data,
            lat=form.lat.data,
            long=form.long.data,
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            tel=form.tel.data,
            email=form.email.data,
        )
        if form.user.data != 0:
            user = User.get_user_by_id(form.user.data)
            user.assign_complaints(denuncia)
        category = Categoria.get_category_by_id(form.category.data)
        category.assign_complaints(denuncia)
        denuncia.add_denuncia()
        flash("La denuncia ha sido creada correctamente.")
        return redirect(url_for("denuncia_index"))
    return render_template("denuncias/new.html", form=form)


def delete(id):
    """Elimina la denuncia con el id recibido por parametro"""
    if not authenticated(session):
        abort(401)
    if not check_permission("denuncias_destroy", session):
        abort(401)
    denuncia = Denuncia.get_by_id(id)
    if not denuncia:
        abort(400)
    denuncia.delete_tracking()
    denuncia.delete_denuncia()
    return redirect(url_for("denuncia_index"))


def edit(id):
    """Retorna y renderiza el formulario para la edicion de una nueva denuncia"""
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("denuncias_update", session):
        abort(401)
    denuncia = Denuncia.get_by_id(id)
    if not denuncia:
        abort(400)
    if denuncia.is_closed():
        abort(400)
    if denuncia.is_resolved():
        abort(400)
    form = EditDenunciaForm(
        title=denuncia.title,
        category=denuncia.category_id,
        description=denuncia.description,
        lat=denuncia.lat,
        long=denuncia.long,
        firstname=denuncia.firstname,
        lastname=denuncia.lastname,
        tel=denuncia.tel,
        email=denuncia.email,
        user=denuncia.assigned_to,
    )
    form.state.data = denuncia.state
    return render_template("denuncias/edit.html", denuncia=denuncia, form=form)


def update(id):
    """ " Contiene la logica para la actualizacion de una denuncia"""
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("denuncias_update", session):
        abort(401)
    denuncia = Denuncia.get_by_id(id)
    if not denuncia:
        abort(400)
    if denuncia.is_closed():
        abort(400)
    if denuncia.is_resolved():
        abort(400)
    form = EditDenunciaForm(
        title=request.form["title"],
        category=request.form["category"],
        description=request.form["description"],
        lat=request.form["lat"],
        long=request.form["long"],
        firstname=request.form["firstname"],
        lastname=request.form["lastname"],
        tel=request.form["tel"],
        email=request.form["email"],
        user=request.form["user"],
        state=request.form["state"],
    )
    if form.validate():
        query = Denuncia.get_by_title(form.title.data)
        if query and denuncia.id != query.id:
            flash("Ya se encuentra una denuncia con dicho titulo en el sistema")
            return render_template("denuncias/edit.html", denuncia=denuncia, form=form)
        denuncia.edit(
            title=form.title.data,
            description=form.description.data,
            lat=form.lat.data,
            long=form.long.data,
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            tel=form.tel.data,
            email=form.email.data,
            state=form.state.data,
        )
        if form.user.data != 0:
            user = User.get_user_by_id(form.user.data)
            user.assign_complaints(denuncia)
        else:
            denuncia.disassign_user()
        if form.category.data != 0:
            category = Categoria.get_category_by_id(form.category.data)
            category.assign_complaints(denuncia)
        else:
            denuncia.disassign_category()
        flash("La denuncia ha sido editado correctamente.")
        return redirect(url_for("denuncia_index"))
    return render_template("denuncias/edit.html", denuncia=denuncia, form=form)


def show(id, page):
    """
        Renderiza el detalle con los datos de una denuncia dada

    Args:
        id: Int que representa el id de la denuncia
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("denuncias_show", session):
        abort(401)
    denuncia = Denuncia.get_by_id(id)
    if denuncia.deleted:
        abort(400)
    config = get_configuration(session)
    seguimientos = Seguimiento.get_tracking(page, config, id)
    usuario = User.get_user_by_id(denuncia.assigned_to)
    categoria = Categoria.get_category_by_id(denuncia.category_id)
    return render_template(
        "denuncias/show.html",
        denuncia=denuncia,
        usuario=usuario,
        categoria=categoria,
        seguimientos=seguimientos,
    )


def search(page):
    """Retorna el listado de denuncias filtrados con las opciones de búsqueda."""
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("denuncia_index", session):
        abort(401)
    config = get_configuration(session)
    denuncias = Denuncia.search_by_title(request.args["title"])
    title = request.args["title"]
    state = ""
    if request.args["state"] != "":
        denuncias = Denuncia.search_by_state(denuncias, request.args["state"])
        state = request.args["state"]
    previous = ""
    if "previous" in request.args.keys() and request.args["previous"] != "":
        denuncias = Denuncia.search_previous_date(denuncias, request.args["previous"])
        previous = request.args["previous"]
    later = ""
    if "later" in request.args.keys() and request.args["later"] != "":
        denuncias = Denuncia.search_later_date(denuncias, request.args["later"])
        later = request.args["later"]
    denuncias = Denuncia.get_denuncias_paginated(denuncias, page, config)
    return render_template(
        "denuncias/index.html",
        denuncias=denuncias,
        filter=1,
        title=title,
        state=state,
        previous=previous,
        later=later,
    )
