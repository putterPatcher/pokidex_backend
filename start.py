from utils.connect import app
from routes.auth import auth_blueprint
from routes.pokidex import pokidex_blueprint
from routes.user import user_blueprint
from paths import Paths

app.register_blueprint(auth_blueprint, url_prefix=Paths.auth)
app.register_blueprint(pokidex_blueprint, url_prefix=Paths.pokidex)
app.register_blueprint(user_blueprint, url_prefix=Paths.user)

if __name__=='__main__':
    app.run(debug=True)

# if __name__=='__main__':
#     from waitress import serve
#     serve(app, host="0.0.0.0", port=8080)
