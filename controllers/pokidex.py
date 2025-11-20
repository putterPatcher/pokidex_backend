import flask
# from utils.connect import users, pokidex
from services.error import serverError
from services.get_json_data import get_data, get_objid, get_dic
from services.headers import json_header
from services.get_json_data import get_objid

def getPokidex(request: flask.Request):
    try:
        pokidex = flask.current_app.config["POKEDEX"]
        data = pokidex.find({})
        response = flask.Response(
            response = flask.json.dumps({
                "message": "Got pokimons successfully",
                "success":True,
                "data":get_data(data)
            }),
            status=200,
            headers=json_header
        )
    except Exception as e:
        response = serverError(e)
    return response

def getPokimon(request: flask.Request, id):
    try:
        pokidex = flask.current_app.config["POKEDEX"]
        pokimon = pokidex.find_one({"_id": get_objid(id)})
        if pokimon:
            response = flask.Response(
                response = flask.json.dumps({
                    "message": "Pokimon found",
                    "success":True,
                    "data": get_dic(pokimon)
                }),
                status=200,
                headers=json_header
            )
        else:
            response = flask.Response(
                response=flask.json.dumps({
                    "message": "No pokimon found",
                    "success":False
                }),
                status=400,
                headers=json_header
            )
    except Exception as e:
        response = serverError(e)
    return response

def addPokimon(request: flask.Request):
    try:
        users = flask.current_app.config["USERS"]
        pokidex = flask.current_app.config["POKEDEX"]
        data = request.get_json()
        id = request.user["_id"]
        data['user_id'] = get_objid(id)
        del data['jwt']
        fields = ['user_id', 'name', 'img', 'type', 'height', 'weight', 'candy', 'candy_count', 'egg', 'spawn_chance', 'avg_spawns', 'spawn_time', 'multipliers', 'weaknesses', 'next_evolution']
        for i in fields:
            if i not in data.keys():
                return flask.Response(
                    headers=json_header,
                    status=400,
                    response=flask.json.dumps({
                        "success": False,
                        "message": f"{i} is not included"
                    })
                )
        pokimon = pokidex.insert_one(data)
        users.find_one_and_update({"_id": data["user_id"]}, { "$push": { "pokimons": pokimon.inserted_id}})
        response=flask.Response(
            headers=json_header,
            status=201,
            response=flask.json.dumps({
                "success": True,
                "message": "Added pokimon successfully"
            })
        )
    except Exception as e:
        response = serverError(e)
    return response

def filterPokimon(request:flask.Request):
    try:
        pokidex = flask.current_app.config["POKEDEX"]
        queries = request.args.to_dict(flat=False)
        find_query = {}
        for i in queries.keys():
            if i == 'name':
                find_query["name"] = {"$regex": queries[i][0], "$options": "i"}
            elif i == 'candy_counts':
                find_query["candy_counts"] = {"$gte": float(queries[i][0]), "$lte": float(queries[i][1])}
            elif i == 'spawn_chance':
                find_query["spawn_chance"] = {"$gte": float(queries[i][0]), "$lte": float(queries[i][1])}
            elif i == 'avg_spawns':
                find_query["avg_spawns"] = {"$gte": float(queries[i][0]), "$lte": float(queries[i][1])}
            elif i == 'height':
                find_query["height"] = {"$gte": float(queries[i][0]), "$lte": float(queries[i][1])}
            elif i == 'weight':
                find_query["weight"] = {"$gte": float(queries[i][0]), "$lte": float(queries[i][1])}
            else:
                return flask.Response(
                    headers=json_header,
                    status=400,
                    response=flask.json.dumps({
                        "success": False,
                        "message": f"Queries are incorrect ({i})"
                    })
                )
        data = pokidex.find(find_query)
        response = flask.Response(
            headers=json_header,
            status=200,
            response=flask.json.dumps({
                "success": True,
                "message": "Got pokemons successfully",
                "data": get_data(data)
            })
        )
    except Exception as e:
        response = serverError(e)
    return response
