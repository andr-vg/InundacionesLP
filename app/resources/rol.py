from flask import redirect, render_template, request, url_for, session, abort
from app.models.rol import Rol
from app.models.user import User
from app.helpers.auth import authenticated
from app.db import db

# Protected resources
def index():    
    roles = Rol.get_all_roles()
    return render_template("rol/index.html", roles=roles)


def rol_assign(id):
    #roles = Rol.query.all()
    roles = Rol.get_all_roles()
    #user=User.query.filter(User.id==id).first()
    user=User.get_user_by_id(id)
    return render_template("rol/rol_assign.html", user=user, roles=roles)    


def rol_user_assign():
    if not authenticated(session):
        abort(401)
    roles = request.form.getlist("rol")
    user = User.get_user_by_id(request.form['id'])
    for name in roles:
        #rol = Rol.query.filter(Rol.name==name).first()
        rol = Rol.get_rol_by_name(name)
        user.roles.append(rol)
    db.session.commit()
    return redirect(url_for("user_index"))