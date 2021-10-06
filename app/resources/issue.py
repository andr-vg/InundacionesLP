from flask import redirect, render_template, request, url_for
from app.models.issue import Issue

# Public resources
def index():
    issues=Issue.query.all()
    return render_template("issue/index.html", issues=issues)


def new():
    return render_template("issue/new.html")


def create():
    return redirect(url_for("issue_index"))
