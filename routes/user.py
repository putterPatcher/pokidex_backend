from utils.connect import flask
from paths import User
from controllers.user import *
from middlewares.auth import verifyUser
from services.get_response import get_response

user_blueprint = flask.Blueprint('user_blueprint', __name__)

@user_blueprint.route(User.details, methods=['GET'])
def get_details():return get_response(flask.request, getDetails, verifyUser)

@user_blueprint.route(User.collection, methods=['GET'])
def get_collection():return get_response(flask.request, getPokimons, verifyUser)

@user_blueprint.route(User.edit_pokimon, methods=['PATCH'])
def edit_pokimon():return get_response(flask.request, editPokimon, verifyUser)

@user_blueprint.route(User.delete_pokimon, methods=['DELETE'])
def delete_pokimon():return get_response(flask.request, deletePokimon, verifyUser)
