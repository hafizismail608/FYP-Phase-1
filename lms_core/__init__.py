from flask import Blueprint

translearn_core_bp = Blueprint('translearn_core', __name__, template_folder='../templates')

from . import views