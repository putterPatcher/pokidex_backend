from utils.connect import flask, app

def serverError(error):
    return app.response_class(
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
