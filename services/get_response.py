import flask
from services.error import serverError

def get_response(request: flask.Request, controller, *middlewares, **kwargs):
    try:
        def __run_middlewares(request: flask.Request, *middlewares, **kwargs):
            try:
                for i in middlewares:
                    res = i(request, **kwargs)
                    if type(res) == flask.Response:
                        return res
            except Exception as e:
                return serverError(e)
            
        def __run_controller(request: flask.Request, controller, **kwargs):
            try:
                return controller(request, **kwargs)
            except Exception as e:
                return serverError(e)
        if type(res:=__run_middlewares(request, *middlewares, **kwargs)) == flask.Response:
            return res
        elif res == None:
            return __run_controller(request, controller, **kwargs)
    except Exception as e:
        return serverError(e)