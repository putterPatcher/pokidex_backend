import flask

def serverError(error):
    return flask.Response(
        response=flask.json.dumps({
            "message": "Internal Server Error",
            "error": str(error),
            "success":False
            },
        ),
        status=500,
        headers={
            "Content-Type": "application/json"
        }
    )
