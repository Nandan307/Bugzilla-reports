from flask import Flask

app = Flask(__name__, template_folder="templates/reports")

from app_dir import routes
