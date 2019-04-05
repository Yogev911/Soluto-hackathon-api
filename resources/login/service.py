import json
from db_util import DbClient
from utils import bson_to_json

DB = DbClient()


def login(request):
    try:
        res = json.loads(request.data)
        user = bson_to_json(returned_request(res))
        return (json.dumps(user), 200)

    except:
        return (("failed to login", 401))


def returned_request(res):
    init = False
    user = DB.get_user_by_email(res["email"])
    if user:
        init = True
    return ({"user": user, "Initial": init})
