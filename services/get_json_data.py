import json
from datetime import datetime
from typing import Any

from bson import ObjectId

class MongoJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)

def get_data(data):
    return json.loads(MongoJSONEncoder().encode(list(data)))

def get_dic(data):
    return json.loads(MongoJSONEncoder().encode(data))

def get_objid(id):return ObjectId(id)

