import uuid
from flask import (
    redirect,
    render_template,
    request,
    url_for,
    abort,
    session,
    flash,
    current_app,
)
from app.models.user import User, Rol
from app.models.configuration import Configuration
from sqlalchemy import and_
from app.helpers.auth import authenticated as auth
from app.helpers.auth import get_pending_state as pend
from app.helpers.permission import has_permission as perm
from app.helpers.denuncia import has_tracking as track
from app.resources import rol
from oauthlib.oauth2 import WebApplicationClient
import requests
from os import environ
import json


def login():
    return render_template("auth/login.html")


def google_login(google_client_id, google_discovery_url):
    def get_google_provider_cfg():
        return requests.get(google_discovery_url).json()

    client = WebApplicationClient(google_client_id)
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=current_app.config["REDIRECT_URI"],
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


def callback(google_client_id, google_client_secret, google_discovery_url):
    def get_google_provider_cfg():
        return requests.get(google_discovery_url).json()

    client = WebApplicationClient(google_client_id)
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(google_client_id, google_client_secret),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    if userinfo_response.json().get("email_verified"):
        users_email = userinfo_response.json()["email"]
    else:
        return "User email not available or not verified by Google.", 400
    users_name = uuid.uuid1()
    # Crear usuario
    user = User(username=users_name, email=users_email, pending=True)

    # Verificar si existe
    if not User.get_user_by_email(users_email):
        user.add_user()
        session["pending"] = user.pending
    else:
        user = User.get_user_by_email(users_email)
        if user.active and not user.deleted and not user.pending:
            # Iniciar sesion
            session["user"] = user.email
            session["username"] = user.username
            session["config"] = Configuration.get_configuration()
            session["permissions"] = User.get_permissions(user_id=user.id)
            session["pending"] = user.pending
    return redirect(url_for("home"))


def authenticate():
    params = request.form
    user = User.login(params=params)
    if not user:
        flash("Usuario o clave incorrecto.")
        return redirect(url_for("auth_login"))
    session["user"] = user.email
    session["username"] = user.username
    session["config"] = Configuration.get_configuration()
    session["permissions"] = User.get_permissions(user_id=user.id)
    session["pending"] = user.pending
    flash("La sesión se inició correctamente.")

    return render_template("home.html")


def is_pending():
    return pend(session)


def authenticated():
    return auth(session)


def has_permission(permission):
    return perm(permission, session)


def has_tracking():
    return track(session)


def logout():
    del session["user"]
    session.clear()
    flash("La sesión se cerró correctamente.")

    return redirect(url_for("auth_login"))
