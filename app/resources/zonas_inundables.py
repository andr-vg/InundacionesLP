import csv
from pathlib import Path
from flask import redirect, render_template, request, url_for, session, abort, flash
import json
from app.helpers.csv_check import check
from flask.templating import render_template
import io

from app.models.coordenadas import Coordenadas
from app.models.zonas_inundables import ZonaInundable

def index(page):
    return render_template("zonas_inundables/index.html",page=1)

def upload():
    """
    Recibe el archivo subido por el usuario, y se asegura que sea .csv para procesarlo
    """
    file = request.files["inputFile"]
    file_content = io.TextIOWrapper(file.stream._file, "UTF8", newline=None)
    if check(file.filename):
        __process_csv(file_content)
    return file.filename

def __process_csv(file):
    """
    Procesa el archivo csv, crea las zonas_inundables, y las coordenadas.
    Luego relaciona zonas y coordenadas, para luego guardarlas en la base de datos.

    Args:
        file: Archivo csv, previamente verificado.
    """
    d_reader = csv.DictReader(file)
    for index,row in enumerate(d_reader):
        zones_list = json.loads(row['area'])
        zona_inundable = ZonaInundable(row['name'])
        for lat, long in zones_list:
            coordenadas = Coordenadas(lat,long)
            coordenadas.assign_zonas_inundables(zona_inundable,coordenadas)

