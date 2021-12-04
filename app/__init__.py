from os import path, environ, urandom
from flask import Flask, render_template, g, Blueprint, redirect, url_for, request
from flask_session import Session
from app import resources
from config import config
from app import db
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from app.resources import (
    configuration,
    puntos_encuentro,
    seguimiento,
    user,
    auth,
    rol,
    denuncias,
    zonas_inundables,
    recorridos_evacuacion,
)
from app.resources.api.denuncias import denuncia_api
from app.resources.api.zonas_inundables import zonas_inundables_api
from app.resources.api.puntos_encuentro import puntos_encuentro_api
from app.resources.api.categorias import categoria_api
from app.resources.api.recorridos_evacuacion import recorridos_evacuacion_api
from app.resources.api.configuration import configuracion_api
from app.helpers import handler
from app.helpers import puntos_encuentro as puntos

# from app.helpers import auth as helper_auth
# from app.helpers import permission as helper_permission
from flask_wtf.csrf import CSRFProtect
import logging

csrf = CSRFProtect()

from oauthlib.oauth2 import WebApplicationClient
from flask_login import (LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
    )


def create_app(environment="development"):
    # Configuración inicial de la app
    app = Flask(__name__)
    CORS(app)


    # CSRF Setup
    # csrf = CSRFProtect(app)
    csrf.init_app(app)
    app.config["WTF_CSRF_CHECK_DEFAULT"] = False
    app.config["WTF_CSRF_ENABLED"] = False
    
    app.secret_key = environ.get("SECRET_KEY") or urandom(24)    

    # Carga de la configuración
    env = environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])

    # Configuration para Oauth2
    GOOGLE_CLIENT_ID = app.config['GOOGLE_CLIENT_ID']
    GOOGLE_CLIENT_SECRET = app.config['GOOGLE_CLIENT_SECRET']
    GOOGLE_DISCOVERY_URL = app.config['GOOGLE_DISCOVERY_URL']


    # OAuth 2 client setup
    client = WebApplicationClient(GOOGLE_CLIENT_ID)
    
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Server Side session
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Configure db
    db.init_app(app)

    # Logs de la BD
    # logging.basicConfig()
    # logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

    # Funciones que se exportan al contexto de Jinja2
    app.jinja_env.globals.update(is_authenticated=auth.authenticated)
    app.jinja_env.globals.update(has_permission=auth.has_permission)
    app.jinja_env.globals.update(
        get_configuration=configuration.get_session_configuration
    )
    app.jinja_env.globals.update(tojson=puntos.tojson)
    # app.jinja_env.globals.update(get_rol_actual=rol.get_session_rol_actual)
    # app.jinja_env.globals.update(get_roles=rol.get_session_roles)
    app.jinja_env.globals.update(get_username=user.get_session_username)
    app.jinja_env.globals.update(is_pending=auth.is_pending)

    # Autenticación
    app.add_url_rule("/iniciar_sesion", "auth_login", auth.login)
    app.add_url_rule("/cerrar_sesion", "auth_logout", auth.logout)
    app.add_url_rule(
        "/autenticacion", "auth_authenticate", auth.authenticate, methods=["POST"]
    )

    # Rutas de Usuarios
    app.add_url_rule(
        "/usuarios", "user_index", user.index, defaults={"page": 1}, methods=["GET"]
    )
    app.add_url_rule("/usuarios/<int:page>", "user_index", user.index, methods=["GET"])
    app.add_url_rule("/usuarios", "user_create", user.create, methods=["POST"])
    app.add_url_rule("/usuarios/nuevo", "user_new", user.new)
    app.add_url_rule("/usuarios/editar", "user_edit", user.edit, methods=["POST"])
    app.add_url_rule(
        "/usuarios/actualizar", "user_update", user.update, methods=["POST"]
    )
    app.add_url_rule(
        "/usuarios/eliminar", "user_soft_delete", user.soft_delete, methods=["POST"]
    )
    app.add_url_rule(
        "/usuarios/estado/<int:id>", "user_change_state", user.change_state
    )
    app.add_url_rule(
        "/usuarios/search/",
        "user_search",
        user.search,
        defaults={"page": 1},
        methods=["GET"],
    )
    app.add_url_rule(
        "/usuarios/search/<int:page>", "user_search", user.search, methods=["GET"]
    )
    # app.add_url_rule("/usuarios/cambiar_rol", "user_change_rol", user.change_rol, methods=["POST"])
    app.add_url_rule("/usuarios/<username>", "user_show", user.show, methods=["GET"])
    app.add_url_rule("/usuarios/pendientes", "user_show_pendientes", user.show_pendientes, defaults={"page": 1}, methods=["GET"])
    app.add_url_rule("/usuarios/pendientes/<int:page>", "user_show_pendientes", user.show_pendientes, methods=["GET"])
    app.add_url_rule("/usuarios/pendientes/aceptar", "user_accept_pendientes", user.accept_pendientes, methods=["POST"])
    app.add_url_rule(
        "/usuarios/pendientes/actualizar", "user_pendientes_update", user.update_pendientes, methods=["POST"]
    )
    # Rutas de perfil propio
    app.add_url_rule("/perfil", "user_edit_profile", user.edit_profile)
    app.add_url_rule(
        "/actualizar_perfil",
        "user_update_profile",
        user.update_profile,
        methods=["POST"],
    )

    # Rutas de Roles

    # Rutas de Puntos de encuentro
    app.add_url_rule(
        "/puntos_encuentro",
        "punto_encuentro_index",
        puntos_encuentro.index,
        defaults={"page": 1},
        methods=["GET"],
    )
    app.add_url_rule(
        "/puntos_encuentro/<int:page>",
        "punto_encuentro_index",
        puntos_encuentro.index,
        methods=["GET"],
    )
    app.add_url_rule(
        "/puntos_encuentro/search/",
        "punto_encuentro_search",
        puntos_encuentro.search,
        defaults={"page": 1},
        methods=["GET"],
    )
    app.add_url_rule(
        "/puntos_encuentro/search/<int:page>",
        "punto_encuentro_search",
        puntos_encuentro.search,
        methods=["GET"],
    )
    app.add_url_rule(
        "/puntos_encuentro",
        "punto_encuentro_create",
        puntos_encuentro.create,
        methods=["POST"],
    )
    app.add_url_rule(
        "/puntos_encuentro/nuevo", "punto_encuentro_new", puntos_encuentro.new
    )
    app.add_url_rule(
        "/puntos_encuentro/editar",
        "punto_encuentro_edit",
        puntos_encuentro.edit,
        methods=["POST"],
    )
    app.add_url_rule(
        "/puntos_encuentro/actualizar",
        "punto_encuentro_update",
        puntos_encuentro.update,
        methods=["POST"],
    )
    app.add_url_rule(
        "/puntos_encuentro/eliminar",
        "punto_encuentro_soft_delete",
        puntos_encuentro.soft_delete,
        methods=["POST"],
    )
    app.add_url_rule(
        "/puntos_encuentro/baja",
        "punto_encuentro_delete",
        puntos_encuentro.delete,
        methods=["POST"],
    )
    app.add_url_rule(
        "/puntos_encuentro/<name>",
        "punto_encuentro_show",
        puntos_encuentro.show,
        methods=["GET"],
    )

    # Rutas de Denuncias

    app.add_url_rule(
        "/denuncias",
        "denuncia_index",
        denuncias.index,
        defaults={"page": 1},
        methods=["GET"],
    )
    app.add_url_rule(
        "/denuncias/<int:page>", "denuncia_index", denuncias.index, methods=["GET"]
    )
    app.add_url_rule(
        "/denuncias/search/",
        "denuncia_search",
        denuncias.search,
        defaults={"page": 1},
        methods=["GET"],
    )
    app.add_url_rule(
        "/denuncias/search/<int:page>",
        "denuncia_search",
        denuncias.search,
        methods=["GET"],
    )
    app.add_url_rule(
        "/denuncias/seguimiento",
        "denuncia_tracking",
        denuncias.index_assigned,
        defaults={"page": 1},
        methods=["GET"],
    )
    app.add_url_rule(
        "/denuncias/seguimiento/<int:page>",
        "denuncia_tracking",
        denuncias.index_assigned,
        methods=["GET"],
    )
    app.add_url_rule("/denuncias/nuevo", "denuncia_new", denuncias.new)
    app.add_url_rule(
        "/denuncias/baja/<int:id>", "denuncia_delete", denuncias.delete, methods=["GET"]
    )
    app.add_url_rule(
        "/denuncias/actualizar/<int:id>",
        "denuncia_edit",
        denuncias.edit,
        methods=["GET"],
    )
    app.add_url_rule(
        "/denuncias/editar/<int:id>",
        "denuncia_update",
        denuncias.update,
        methods=["POST"],
    )
    app.add_url_rule(
        "/denuncias", "denuncia_create", denuncias.create, methods=["POST"]
    )
    app.add_url_rule(
        "/denuncias/detalle/<int:id>",
        "denuncia_show",
        denuncias.show,
        defaults={"page": 1},
        methods=["GET"],
    )
    app.add_url_rule(
        "/denuncias/detalle/<int:id>/<int:page>",
        "denuncia_show",
        denuncias.show,
        methods=["GET"],
    )

    # Rutas de Seguimientos

    app.add_url_rule("/seguimiento/nuevo/<int:id>", "seguimiento_new", seguimiento.new)
    app.add_url_rule(
        "/seguimiento/<int:id>",
        "seguimiento_create",
        seguimiento.create,
        methods=["POST"],
    )
    app.add_url_rule(
        "/seguimiento/baja/<int:id>/<int:page>",
        "seguimiento_delete",
        seguimiento.delete,
        methods=["GET"],
    )

    # Rutas de Configuracion
    app.add_url_rule("/configuracion", "configuration_update", configuration.update)
    app.add_url_rule(
        "/config",
        "configuration_confirm_update",
        configuration.confirm_update,
        methods=["POST"],
    )

    # Rutas para Zonas_inundables
    app.add_url_rule(
        "/zonas_inundables",
        "zonas_inundables_index",
        zonas_inundables.index,
        defaults={"page": 1},
        methods=["GET"],
    )
    app.add_url_rule(
        "/zonas_inundables/<int:page>",
        "zonas_inundables_index",
        zonas_inundables.index,
        methods=["GET"],
    )
    app.add_url_rule(
        "/zonas_inundables/subir",
        "zonas_inundables_upload",
        zonas_inundables.upload,
        methods=["POST"],
    )
    app.add_url_rule(
        "/zonas_inundables/eliminar",
        "zonas_inundables_delete",
        zonas_inundables.delete,
        methods=["POST"],
    )
    app.add_url_rule(
        "/zonas_inundables/actualizar",
        "zonas_inundables_update",
        zonas_inundables.update,
        methods=["POST"],
    )
    app.add_url_rule(
        "/zonas_inundables/editar/",
        "zonas_inundables_edit",
        zonas_inundables.edit,
        methods=["POST"],
    )
    app.add_url_rule(
        "/zonas_inundables/<name>",
        "zonas_inundables_show",
        zonas_inundables.show,
        methods=["GET"],
    )
    app.add_url_rule(
        "/zonas_inundables/search/",
        "zonas_inundables_search",
        zonas_inundables.search,
        defaults={"page": 1},
        methods=["GET"],
    )
    app.add_url_rule(
        "/zonas_inundables/search/<int:page>",
        "zonas_inundables_search",
        zonas_inundables.search,
        methods=["GET"],
    )
    app.add_url_rule(
        "/zonas_inundables/publicar",
        "zonas_inundables_soft_delete",
        zonas_inundables.soft_delete,
        methods=["POST"],
    )

    # Rutas para recorridos de evacuacion
    app.add_url_rule(
        "/recorridos_evacuacion",
        "recorridos_index",
        recorridos_evacuacion.index,
        defaults={"page": 1},
        methods=["GET"],
    )
    app.add_url_rule(
        "/recorridos_evacuacion/<int:page>",
        "recorridos_index",
        recorridos_evacuacion.index,
        methods=["GET"],
    )
    app.add_url_rule(
        "/recorridos_evacuacion",
        "recorridos_create",
        recorridos_evacuacion.create,
        methods=["POST"],
    )
    app.add_url_rule(
        "/recorridos_evacuacion/nuevo", "recorridos_new", recorridos_evacuacion.new
    )
    app.add_url_rule(
        "/recorridos_evacuacion/editar",
        "recorridos_edit",
        recorridos_evacuacion.edit,
        methods=["POST"],
    )
    app.add_url_rule(
        "/recorridos_evacuacion/actualizar",
        "recorridos_update",
        recorridos_evacuacion.update,
        methods=["POST"],
    )
    app.add_url_rule(
        "/recorridos_evacuacion/eliminar",
        "recorridos_delete",
        recorridos_evacuacion.delete,
        methods=["POST"],
    )
    app.add_url_rule(
        "/recorridos_evacuacion/estado/<int:id>",
        "recorridos_publicate",
        recorridos_evacuacion.change_state,
    )
    app.add_url_rule(
        "/recorridos_evacuacion/search/",
        "recorridos_search",
        recorridos_evacuacion.search,
        defaults={"page": 1},
        methods=["GET"],
    )
    app.add_url_rule(
        "/recorridos_evacuacion/search/<int:page>",
        "recorridos_search",
        recorridos_evacuacion.search,
        methods=["GET"],
    )
    app.add_url_rule(
        "/recorridos_evacuacion/<name>",
        "recorridos_show",
        recorridos_evacuacion.show,
        methods=["GET"],
    )

##  Autenticacion Google
    app.add_url_rule(
        "/google_autenticacion",
        "google_authenticate",
        auth.google_login,
        defaults={
            "google_client_id": GOOGLE_CLIENT_ID,
            "google_discovery_url": GOOGLE_DISCOVERY_URL,
        },
        methods=["POST"],
    ) 

    app.add_url_rule(
        "/login/callback",
        "auth_callback",
        auth.callback,
            defaults={
                "google_client_id": GOOGLE_CLIENT_ID,
                "google_client_secret": GOOGLE_CLIENT_SECRET,
                "google_discovery_url": GOOGLE_DISCOVERY_URL
            },
        methods=["GET"]
    ) 


    # Ruta para el Home (usando decorator)
    @app.route("/")
    def home():
        return render_template("home.html")

    # Rutas de API-REST (usando Blueprints)
    api = Blueprint("api", __name__, url_prefix="/api")
    api.register_blueprint(zonas_inundables_api)
    api.register_blueprint(denuncia_api)
    api.register_blueprint(puntos_encuentro_api)
    api.register_blueprint(recorridos_evacuacion_api)
    api.register_blueprint(categoria_api)
    api.register_blueprint(configuracion_api)
    csrf.exempt(denuncia_api)
    app.register_blueprint(api)
    app.before_request(disable_csrf)

    # Handlers
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(401, handler.unauthorized_error)
    app.register_error_handler(400, handler.bad_request_error)
    # Implementar lo mismo para el error 500

    # Retornar la instancia de app configurada
    return app


def disable_csrf():
    if request.blueprint != None and not "api." in request.blueprint:
        csrf.protect()
