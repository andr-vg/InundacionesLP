from flask import redirect, render_template, request, url_for, session, abort
from app.models.user import User
from app.models.rol import Permission
from app.helpers.auth import authenticated
from app.helpers.permission import check as check_permission
from app.db import db
from app.resources import rol


# Protected resources
def index():
    user_email = authenticated(session)
    id = User.get_id_from_email(user_email)
    if not user_email:
        abort(401)

    if not check_permission(id, "user_index"):
        abort(401)
        
    users=User.query.all()
    return render_template("user/index.html", users=users)


def new():
#    if not authenticated(session):
#        abort(401)
#  
# 
    return render_template("user/new.html")


def create():
#    if not authenticated(session):
#        abort(401)
    new_user = User(**request.form)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("user_index"))
