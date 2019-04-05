import json
from bson.json_util import dumps


def bson_to_json(bson_data):
    return json.loads(dumps(bson_data))
