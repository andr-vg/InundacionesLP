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
    form = EditZonaInundableForm(id=zona.id, name= zona.name, state = zona.state, color = zona.color)
    return(render_template('zonas_inundables/edit.html',form=form))

def delete(id):
    pass

def update():
    pass