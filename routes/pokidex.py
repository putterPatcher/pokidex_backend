from utils.connect import flask
from paths import Pokidex
from controllers.pokidex import *
from services.get_response import get_response
from middlewares.auth import verifyUser

pokidex_blueprint = flask.Blueprint('pokidex_blueprint', __name__)

@pokidex_blueprint.route(Pokidex.pokidex, methods=["GET"])
def get_pokidex():return getPokidex(flask.request)

@pokidex_blueprint.route(Pokidex.pokimon, methods=['GET'])
def get_pokimon(id):return getPokimon(flask.request, id=id)

@pokidex_blueprint.route(Pokidex.add_pokimon, methods=['POST'])
def add_pokimonn():return get_response(flask.request, addPokimon, verifyUser)

@pokidex_blueprint.route(Pokidex.filter_pokimon, methods=['GET'])
def filter_pokimon():return filterPokimon(flask.request)
