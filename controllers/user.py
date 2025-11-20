import flask
# from utils.connect import users, pokidex
from services.error import serverError
from services.get_json_data import get_objid, get_dic
from services.headers import json_header

def getDetails(request: flask.Request):
    try:
        user = request.user
        del user["jwt"], user["password"]
        response = flask.Response(
            headers=json_header,
            status=200,
            response=flask.json.dumps({
                "success": True,
                "message": "Got details successfully",
                "data": user
            })
       )
    except Exception as e:
        response = serverError(e)
    return response

def getPokimons(request: flask.Request):
    try:
        pokidex = flask.current_app.config["POKEDEX"]
        ids = request.user["pokimons"]
        pokimons = []
        for i in ids:
            pokimons.append(get_dic(pokidex.find_one({"_id": get_objid(i)})))
        response = flask.Response(
            headers=json_header,
            status=200,
            response=flask.json.dumps({
                "success": True,
                "message": "Got pokimons successfully",
                "data": pokimons
            })
        )
    except Exception as e:
        response = serverError(e)
    return response

def editPokimon(request: flask.Request):
    try:
        users = flask.current_app.config["USERS"]
        pokidex = flask.current_app.config["POKEDEX"]
        user_id = get_objid(request.user["_id"])
        id = get_objid(request.get_json()["_id"])
        data = request.get_json()
        del data["_id"], data["jwt"]
        if id in dict(users.find_one({"_id": user_id}))["pokimons"]:
            pokidex.find_one_and_update({"_id": id}, {"$set": data})
            response = flask.Response(
                headers=json_header,
                status=200,
                response=flask.json.dumps({
                    "success": True,
                    "message": "Updated pokimon successfully",
                })
            )
        else:
            return flask.Response(
                headers=json_header,
                status=400,
                response=flask.json.dumps({
                    "success": False,
                    "message": "Pokimon not yours"
                })
            )
    except Exception as e:
        response = serverError(e)
    return response

def deletePokimon(request: flask.Request):
    try:
        users = flask.current_app.config["USERS"]
        pokidex = flask.current_app.config["POKEDEX"]
        id = get_objid(request.get_json()["_id"])
        users.find_one_and_update({"_id": get_objid(request.user["_id"])}, {"$pull": {"pokimons": id}})
        pokidex.find_one_and_delete({"_id": id, "user_id": get_objid(request.user["_id"])})
        response = flask.Response(
            headers=json_header,
            status=200,
            response=flask.json.dumps({
                "success": True,
                "message": "Deleted pokimon successfully"
            })
        )
    except Exception as e:
        response = serverError(e)
    return response
