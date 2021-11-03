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
    file = request.files["inputFile"]
    file_content = io.TextIOWrapper(file.stream._file, "UTF8", newline=None)
    print(check(file.filename))
    if check(file.filename):
        _process_csv(file_content)
    return file.filename

def _process_csv(file):
    #Path de zonas.csv
    zonas_folder = Path.cwd().parent /'grupo22' /'app' / 'data'
    json_file_path = zonas_folder / 'zonas.json'
    #Lectura de zonas.csv
    values = {}
    d_reader = csv.DictReader(file)
    for index,row in enumerate(d_reader):
        zones_list = json.loads(row['area'])
        zona_inundable = ZonaInundable(row['name'])
        for lat, long in zones_list:
            coordenadas = Coordenadas(lat,long)
            coordenadas.assign_zonas_inundables(zona_inundable,coordenadas)


"""        values[index] = row
        values[index]["area"]= zones_list
    with open(json_file_path,'w') as json_file:
        json_file.write(json.dumps(values, indent=4))"""
