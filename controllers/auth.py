import flask
# from utils.connect import users
from services.error import serverError
from services.headers import json_header
from werkzeug.security import generate_password_hash
import re

def authSignup(request: flask.Request):
    try:
        users = flask.current_app.config["USERS"]
        user_details = request.get_json()
        fields = ['name', 'email', 'username', 'password']
        for i in user_details.keys():
            if i not in fields:
                return flask.Response(
                    headers=json_header,
                    status=400,
                    response=flask.json.dumps({
                        "success": False,
                        "message": f"{i} is incorrect field"
                    })
                )
            if len(user_details[i]) == 0:
                return flask.Response(
                    headers=json_header,
                    status=400,
                    response=flask.json.dumps({
                        "success": False,
                        "message": f"{i} is empty"
                    })
                )
            if i == 'email':
                if re.match(r'^[a-z0-9]+[. _]?[a-z0-9]+[@]\w+[.]\ w+$', user_details[i]):
                    return flask.Response(
                    headers=json_header,
                    status=400,
                    response=flask.json.dumps({
                        "success": False,
                        "message": f"{i} is not an email"
                    })
                )
        user_details["password"] = generate_password_hash(user_details["password"])
        user_details["email"] = user_details["email"].lower()
        email_found = users.find_one({"email": user_details["email"]})
        if email_found:
            return flask.Response(
                headers=json_header,
                status=409,
                response=flask.json.dumps({
                    "success": False,
                    "message": "Email already present"
                })
            )
        username_found = users.find_one({"username": user_details["username"]})
        if username_found:
            return flask.Response(
                headers=json_header,
                status=409,
                response=flask.json.dumps({
                    "success": False,
                    "message": "Username already present"
                })
            )
        user_details['jwt'] = None
        user_details["pokimons"] = []
        users.insert_one(user_details)
        response = flask.Response(
            headers=json_header,
            status=201,
            response=flask.json.dumps({
                "success": True,
                "message": "User successfully created",
            })
        )
    except Exception as e:
        response = serverError(e)
    return response

def authLogin(request: flask.Request):
    try:
        return flask.Response(
            headers=json_header,
            status=202,
            response=flask.json.dumps({
                "success": True,
                "message": "Login successful",
                "data": {
                    "jwt": request.user["jwt"]
                }
            })
        )
    except Exception as e:
        return serverError(e)

def authLogout(request: flask.Request):
    try:
        users = flask.current_app.config["USERS"]
        email = request.user["email"]
        users.find_one_and_update({"email": email}, { "$set": {"jwt": None}} )
        response = flask.Response(
            headers=json_header,
            status=200,
            response=flask.json.dumps({
                "success": True,
                "message": "Logged out successfully"
            })
        )
    except Exception as e:
        response = serverError(e)
    return response
