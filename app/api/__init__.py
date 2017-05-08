from flask import Blueprint

api = Blueprint('api','name')

from . import authentication,errors
