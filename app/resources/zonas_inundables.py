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
    :param page:Numero de pagina para el paginado del listado
    :type page: int
    :raises: OperationalError
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
    return render_template("zonas_inundables/new.html",file_name = file.filename)

def __process_csv(file):
    """
    Procesa el archivo csv, crea las zonas_inundables, y las coordenadas.
    Luego relaciona zonas y coordenadas, para luego guardarlas en la base de datos.

    Args:
        file: Archivo csv, previamente verificado.
    """
    d_reader = csv.DictReader(file)
    for row in (d_reader):
        zona = ZonaInundable.exists_zona_inundable(row['name'])
        print(zona)
        if not zona:
            zones_list = json.loads(row['area'])
            zona_inundable = ZonaInundable(row['name'])
            for lat, long in zones_list:
                coordenadas = Coordenadas(lat,long)
                coordenadas.assign_zonas_inundables(zona_inundable,coordenadas)

def edit():
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("punto_encuentro_update", session):
        abort(401)
    zona = ZonaInundable.get_zona_by_id(request.form['id'])
    
    form = EditZonaInundableForm(id=zona.id, name= zona.name,
    state = "Publicado" if zona.state else "Despublicado", color = zona.color)
    return(render_template('zonas_inundables/edit.html',form=form))

def delete():
    """
    Lógica a realizar al momento de eliminar
    de manera fisica una zona
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission('zonas_inundables_destroy', session):
        abort(401)
    zona = ZonaInundable.get_zona_by_id(request.form["id"])
    zona.delete()
    zona.update_zona_inundable()
    flash("Recorrido eliminado correctamente.")
    return redirect(url_for("zonas_inundables_index"))

def update():
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("punto_encuentro_update", session):
        abort(401)
    form = EditZonaInundableForm(id=request.form['id'],
    name= request.form['name'], state = request.form['state'], color = request.form['color'])
    if form.validate():
        zona = ZonaInundable.get_zona_by_id(form.id.data)
        query = ZonaInundable.get_zona_by_name(form.name.id)
        if query and query.id != zona.id:
            flash("Ya se encuentra una Zona con dicho nombre en el sistema")
            return render_template('zonas_inundables/edit.html',form=form)
        zona.edit(name = form.name.data ,color = form.color.data ,
        state = 1 if form.state.data == "Publicado" else 0)
        zona.update_zona_inundable()
        flash("La zona ha sido editada correctamente.")
        return redirect(url_for("zonas_inundables_index"))
    return render_template("zona_inundable/edit.html", form=form)

def show(name):
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("user_show", session):
        abort(401)    
    zona = ZonaInundable.get_zona_by_name(name)
    return render_template("zonas_inundables/show.html", zona = zona, coords = zona.get_coords_as_list())

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
    if not check_permission("zonas_inundables_index",session):
        abort(401)
    config = get_configuration(session)
    zonas = ZonaInundable.search_by_name(request.args["name"])
    name = request.args["name"]
    active = ""
    if "state" in request.args.keys() and request.args["state"]!="":
        active = request.args["state"]
        if request.args["state"]=="activo":
            zonas = ZonaInundable.get_with_state(zonas, True)
    zonas = ZonaInundable.search_paginate(zonas, page, config)

    return render_template("zonas_inundables/index.html", zonas=zonas, filter=1, name=name, active=active)
