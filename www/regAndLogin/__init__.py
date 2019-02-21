from flask import Blueprint

login = Blueprint('login',__name__)

register = Blueprint('register',__name__)

forget = Blueprint('forget',__name__)

from . import login,register,forget