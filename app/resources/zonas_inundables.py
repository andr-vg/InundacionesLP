import csv
from pathlib import Path
from flask import redirect, render_template, request, url_for, session, abort, flash
import json
from app.forms.zonas_inundables import EditZonaInundableForm
from app.helpers.csv_check import check
from app.helpers.auth import authenticated
from app.helpers.permission import has_permission as check_permission
from app.helpers.configuration import get_configuration
from sqlalchemy.exc import OperationalError
from app.models.user import User

from flask.templating import render_template
import io

from app.models.coordenadas import Coordenadas
from app.models.zonas_inundables import ZonaInundable


def index(page):
    """Retorna y renderiza el listado de zonas
    Args:
        page(int):Numero de pagina para el paginado del listado de zonas
    raises:
        OperationalError
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("zonas_inundables_index", session):
        abort(401)
    config = get_configuration(session)
    try:
        zonas = ZonaInundable.get_index_zonas(page, config)
    except OperationalError:
        flash("No hay zonas inundables aún.")
        zonas = None
    return render_template("zonas_inundables/index.html", zonas=zonas)


def upload():
    """
    Recibe el archivo subido por el usuario, y se asegura que sea .csv para procesarlo
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("zonas_inundables_new", session):
        abort(401)
    file = request.files["inputFile"]
    file_content = io.TextIOWrapper(file.stream._file, "UTF8", newline=None)
    if check(file.filename):
        __process_csv(file_content)
        return render_template("zonas_inundables/new.html", file_name=file.filename)
    else:
        abort(400)


def __process_csv(file):
    """
    Procesa el archivo csv, crea las zonas_inundables, y las coordenadas.
    Luego relaciona zonas y coordenadas, para luego guardarlas en la base de datos.

    Args:
        file: Archivo csv, previamente verificado.
    """
    def add_coordenadas(lista_zonas,zona):
        """
        Agregara coordenadas segun la zona que corresponda
        """
        for lat, long in lista_zonas:
            coordenadas = Coordenadas(lat, long)
            coordenadas.assign_zonas_inundables(zona, coordenadas)  

    d_reader = csv.DictReader(file)
    for row in d_reader:
        try:
            zona = ZonaInundable.exists_zona_inundable(row["name"])
            zones_list = json.loads(row["area"])
            if not zona:
                zona_inundable = ZonaInundable(row["name"])
                add_coordenadas(zones_list,zona_inundable)
            else:
                for coord in zona.coords:
                    coord.delete()
                add_coordenadas(zones_list,zona)
        except:
            abort(400)


def edit():
    """
    Renderizado de la pagina de ediciones de Zonas inundables
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("punto_encuentro_update", session):
        abort(401)
    zona = ZonaInundable.get_zona_by_id(request.form["id"])
    form = EditZonaInundableForm(
        id=zona.id,
        name=zona.name,
        state="Publicado" if zona.state else "Despublicado",
        color=zona.color,
    )
    return render_template("zonas_inundables/edit.html", form=form, zona=zona, coords=zona.get_coords_as_list())


def delete():
    """
    Lógica a realizar al momento de eliminar
    de manera fisica una zona
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("zonas_inundables_destroy", session):
        abort(401)
    zona = ZonaInundable.get_zona_by_id(request.form["id"])
    zona.delete()
    flash("Zona eliminada correctamente.")
    return redirect(url_for("zonas_inundables_index"))


def update():
    """
    Lógica a realizar al momento de confirmar
    la edición de la zona inundable actual.
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("punto_encuentro_update", session):
        abort(401)
    form = EditZonaInundableForm(
        id=request.form["id"],
        name=request.form["name"],
        state=request.form["state"],
        color=request.form["color"],
    )
    if form.validate():
        zona = ZonaInundable.get_zona_by_id(form.id.data)
        query = ZonaInundable.get_zona_by_name(form.name.data)
        if query and zona.id != query.id:
            flash("Ya se encuentra una Zona con dicho nombre en el sistema")
            return render_template("zonas_inundables/edit.html", form=form)
        zona.edit(
            name=form.name.data,
            color=form.color.data,
            state=1 if form.state.data == "Publicado" else 0,
        )
        flash("La zona ha sido editada correctamente.")
        return redirect(url_for("zonas_inundables_index"))
    else:
        zona = ZonaInundable.get_zona_by_id(request.form["id"])
        return render_template("zonas_inundables/edit.html", form=form, zona=zona, coords=zona.get_coords_as_list())


def show(name):
    """
    Renderiza el detalle con los datos de una zona inundable

    Args:
        name(string): nombre de la zona inundable
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("zonas_inundables_index", session):
        abort(401)
    zona = ZonaInundable.get_zona_by_name(name)
    return render_template(
        "zonas_inundables/show.html", zona=zona, coords=zona.get_coords_as_list()
    )


def search(page):
    """
    Lógica a realizar al momento de renderizar
    un listado de búsqueda de zonas_inundables paginado.

    Args:
        page(int): número de página
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("zonas_inundables_index", session):
        abort(401)
    config = get_configuration(session)
    zonas = ZonaInundable.search_by_name(request.args["name"])
    name = request.args["name"]
    active = ""
    if "active" in request.args.keys() and request.args["active"] != "":
        active = request.args["active"]
        if request.args["active"] == "activo":
            zonas = ZonaInundable.get_with_state(zonas, True)
        elif request.args["active"] == "inactivo":
            zonas = ZonaInundable.get_with_state(zonas, False)
    zonas = ZonaInundable.search_paginate(zonas, page, config)

    return render_template(
        "zonas_inundables/index.html", zonas=zonas, filter=1, name=name, active=active
    )


def soft_delete():
    """ " Elimina una zona logicamente mantenido con la variable state."""
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("zonas_inundables_update", session):
        abort(401)
    zona = ZonaInundable.get_zona_by_id(request.form["id"])
    zona.change_state()
    state = "Publicado" if zona.state else "Despublicado"
    flash("La zona ha sido {} correctamente".format(state))
    return redirect(url_for("zonas_inundables_index"))
