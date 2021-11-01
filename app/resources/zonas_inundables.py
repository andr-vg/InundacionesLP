import csv
from pathlib import Path
from flask import redirect, render_template, request, url_for, session, abort, flash
import json

from flask.templating import render_template

def index(page):
    return render_template("zonas_inundables/index.html",page=1)

def upload():
    file = request.files["inputFile"]
    return file.filename
"""
#Path de zonas.csv
path = Path.cwd() 
zonas_folder = path.parent /'grupo22' /'app' / 'data'
file = zonas_folder / 'zonas.csv'
json_file_path = zonas_folder / 'zonas.json'

#Lectura de zonas.csv
values = {}
with open(file) as csv_file:
    d_reader = csv.DictReader(csv_file)
    for index,row in enumerate(d_reader):
        zones_list = json.loads(row['area'])
        values[index] = row
        values[index]["area"]= zones_list
print(values[0]["area"][1])




#with open(json_file_path,'w') as json_file:
#    json_file.write(json.dumps(values, indent=4))
"""