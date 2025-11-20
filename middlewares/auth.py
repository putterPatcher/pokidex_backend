from werkzeug.security import check_password_hash
import jwt
import flask
# from utils.connect import users
from services.error import serverError
from services.headers import json_header
from services.get_json_data import get_dic
from pymongo import ReturnDocument
import datetime
from datetime import timezone

def authUser(request: flask.Request):
    try:
        users = flask.current_app.config["USERS"]
        user_details = request.get_json()
        fields = ['email', 'password']
        for i in user_details.keys():
            if i not in fields:
                return flask.Response(
                    headers=json_header,
                    status=401,
                    response=flask.json.dumps({
                        "success": False,
                        "message": f"{i} field present"
                    })
                )
        user = users.find_one({"email": user_details["email"]})
        if not user:
            return flask.Response(
                headers=json_header,
                status=401,
                response=flask.json.dumps({
                    "success": False,
                    "message": "Email not found"
                })
            )
        check_password = check_password_hash(user["password"], user_details["password"])
        if not check_password:
            return flask.Response(
                headers=json_header,
                status=401,
                response=flask.json.dumps({
                    "success": False,
                    "message": "Password is incorrect"
                })
            )
        issued_at_time = datetime.datetime.now(timezone.utc)
        jwt_token = jwt.encode({ "name": user["name"], "username": user["username"], "email": user["email"], "time": str(issued_at_time)}, flask.current_app.config["SECRET_KEY"], algorithm="HS256")
        user = users.find_one_and_update({"email": user_details["email"]}, { "$set": {"jwt": jwt_token}}, return_document=ReturnDocument.AFTER)
        request.user = get_dic(user)
        return None
    except Exception as e:
        return serverError(e)

def verifyUser(request: flask.Request):
    try:
        users = flask.current_app.config["USERS"]
        jwt = request.get_json()["jwt"]
        user = users.find_one({"jwt": jwt})
        if not user:
            return flask.Response(
                headers=json_header,
                status=401,
                response=flask.json.dumps({
                    "success": False,
                    "message": "jwt is incorrect"
                })
            )
        request.user = get_dic(user)
        return None
    except Exception as e:
        return serverError(e)