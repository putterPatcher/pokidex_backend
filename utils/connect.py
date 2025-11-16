import flask
import pymongo
import utils.config as conf

app = flask.Flask(__name__)
app.config.from_object(conf.Config())

client = pymongo.MongoClient(
    app.config["MONGO_DB_URI"]
)

try:
    client.server_info()
    print("Connected to MongoDB.")
except Exception as e:
    print("MongoDB connection error:", e)

database = client.pokidex
users = database.users
pokidex = database.pokidex

# import json
# with open('../pokidex.json', 'r') as file:
#     data = json.load(file)

# for i in data:
#     i["height"]=float(i["height"][:-3])
#     i["weight"]=float(i["weight"][:-4])

# pokidex.insert_many(data)
