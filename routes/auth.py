from utils.connect import flask
from paths import Auth
from controllers.auth import *
from middlewares.auth import authUser, verifyUser
from services.get_response import get_response

auth_blueprint = flask.Blueprint('auth_blueprint', __name__)

@auth_blueprint.route(Auth.signup, methods=['POST'])
def signup():return authSignup(flask.request)

@auth_blueprint.route(Auth.login, methods=['POST'])
def login():return get_response(flask.request, authLogin, authUser)

@auth_blueprint.route(Auth.logout, methods=['POST'])
def logout():return get_response(flask.request, authLogout, verifyUser)
