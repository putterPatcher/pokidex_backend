from utils.connect import *
from services.error import serverError
from services.headers import json_header
from services.get_json_data import get_data, get_dic, get_objid
from werkzeug.security import generate_password_hash

def authSignup(request: flask.Request):
    try:
        user_details = request.get_json()
        fields = ['name', 'email', 'username', 'password']
        for i in user_details.keys():
            if i not in fields:
                return app.response_class(
                    headers=json_header,
                    status=400,
                    response=flask.json.dumps({
                        "success": False,
                        "message": f"${i} is incorrect field"
                    })
                )
        user_details["password"] = generate_password_hash(user_details["password"])
        user_details["email"] = user_details["email"].lower()
        email_found = users.find_one({"email": user_details["email"]})
        if email_found:
            return app.response_class(
                headers=json_header,
                status=409,
                response=flask.json.dumps({
                    "success": False,
                    "message": "Email already present"
                })
            )
        username_found = users.find_one({"username": user_details["username"]})
        if username_found:
            return app.response_class(
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
        response = app.response_class(
            headers=json_header,
            status=201,
            response=flask.json.dumps({
                "success": True,
                "message": "User successfully created",
            })
        )
    except Exception as e:
        response = serverError
    return response

def authLogin(request: flask.Request):
    try:
        return app.response_class(
            headers=json_header,
            status=202,
            response=flask.json.dumps({
                "success": False,
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
        email = request.user["email"]
        users.find_one_and_update({"email": email}, { "$set": {"jwt": None}} )
        response = app.response_class(
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
