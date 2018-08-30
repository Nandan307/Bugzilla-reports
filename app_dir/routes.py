# from app_dir import app
import os
import logging

from flask import Flask, request, Blueprint, render_template
from .reports.bugzilla_bzreports import bz_fetch_bugs
from . import Team
from . import BZ


# Application Blueprint to add to the "app" instance
template_folder_path = os.path.abspath("")
routing = Blueprint("routes.py", __name__,
                    template_folder=template_folder_path +
                    "app_dir/templates/report")

# Setting up the Flask application
bzreports_path = os.path.abspath("")
app = Flask(__name__, template_folder=bzreports_path +
            "/app_dir/templates/reports",
            static_url_path=bzreports_path + "/app_dir/static")


def index():
    return "<h1>Welcome to BZreports</h1>"


# Example: localhost:5000/reports/rhel?v=6
def render_html_rhel():
    team_obj = Team.Team("active_team.json")
    bz = BZ.BZ()
    # if key doesn't exist, returns None
    version = request.args.get('v')
    # If version is not specified i.e "localhost:5000/reports/rhel"
    # then version = "7" by default
    if not version:
        version = "7"
    logging.debug("rhel: version is {}\n".format(version))
    bugs = bz_fetch_bugs(bz, team_obj,
                         "Red Hat Enterprise Linux " + version)
    return render_template("rhel.html", bugs=bugs)


# Example: localhost:5000/reports/rhel-stale
def render_html_rhel_stale():
    team_obj = Team.Team("active_team.json")
    bz = BZ.BZ()
    logging.debug("rhel-stale: no version required")
    bugs = bz_fetch_bugs(bz, team_obj)
    return render_template("rhel_stale.html", bugs=bugs)


# Example: localhost:5000/reports/rhel-blockers?v=6
def render_html_rhel_blockers():
    team_obj = Team.Team("active_team.json")
    bz = BZ.BZ()
    # if key doesn't exist, returns None
    version = request.args.get('v')
    # If version is not specified i.e "localhost:5000/reports/rhel-blockers"
    # then version = "7" by default
    if not version:
        version = "7"
    logging.debug("rhel-blockers: version is {}\n".format(version))
    bugs = bz_fetch_bugs(bz, team_obj,
                         "Red Hat Enterprise Linux " + version)
    return render_template("rhel_blockers.html", bugs=bugs)


# -------------Decoupling frontend and backend-----------------

@routing.route("/")
@routing.route("/index")
def decorator_func_index():
    return index()


@routing.route("/reports/rhel")
def decorator_func_rhel():
    return render_html_rhel()


@routing.route("/reports/rhel-stale")
def decorator_func_rhel_stale():
    return render_html_rhel_stale()


@routing.route("/reports/rhel-blockers")
def decorator_func_rhel_blockers():
    return render_html_rhel_blockers()
