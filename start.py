from routes.auth import auth_blueprint
from routes.pokidex import pokidex_blueprint
from routes.user import user_blueprint
from paths import Paths
import flask
import utils.config as conf
from flask_cors import CORS
import pymongo

client = database = users = pokidex = None
def create_app():
    global client, database, users, pokidex
    app = flask.Flask(__name__)
    app.config.from_object(conf.Config())
    CORS(app)

    client = pymongo.MongoClient(
    app.config["MONGO_DB_URI"]
    )

    try:
        client.server_info()
        print("Connected to MongoDB.")
    except Exception as e:
        print("MongoDB connection error:", e)

    database = client.pokidex
    app.config["USERS"] = database.users
    app.config["POKEDEX"] = database.pokidex

    app.register_blueprint(auth_blueprint, url_prefix=Paths.auth)
    app.register_blueprint(pokidex_blueprint, url_prefix=Paths.pokidex)
    app.register_blueprint(user_blueprint, url_prefix=Paths.user)
    return app

if __name__=='__main__':
    from waitress import serve
    import os

    port = int(os.environ.get("PORT", 10000))
    print(port)
    serve(create_app(), host="0.0.0.0", port=port)
