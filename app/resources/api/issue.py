from flask import jsonify, Blueprint
from app.db import connection
from app.models.issue import Issue

issue_api = Blueprint("consultas", __name__, url_prefix="/consultas")


@issue_api.get("/")
def index():
    conn = connection()
    issues = Issue.all(conn)

    return jsonify(issues=issues)
