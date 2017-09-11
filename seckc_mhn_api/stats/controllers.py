'''auth_module
'''
import os
import json
import datetime
from pymongo import MongoClient
from flask import Blueprint, request, abort
import requests
from seckc_mhn_api.config import SETTINGS
from seckc_mhn_api.auth.controllers import user_status
import certifi

# Define the blueprint: 'stats', set its url prefix: app.url/stats
STATS_MODULE = Blueprint('stats', __name__, url_prefix='/stats')

database = "mnemosyne"
dbconn = MongoClient()
db = dbconn[database]

MNEMOSYNE_COOKIE = None
AUTH_PAYLOAD = {
    "username": SETTINGS["mnemosyne"]["username"],
    "password": SETTINGS["mnemosyne"]["password"]
}

@STATS_MODULE.route("/", methods=['GET'])
@user_status
def getstats():
    if request.args.get('date', default=None, type=None) is not None and request.args.get('channel', default=None, type=None) is not None:
        query = {'date': request.args.get('date', default=None, type=None), 'channel': request.args.get('channel', default=None, type=None)}
    elif request.args.get('date', default=None, type=None) is not None:
        query = {'date': request.args.get('date', default=None, type=None)}
    elif request.args.get('channel', default=None, type=None) is not None:
        query = {'channel': request.args.get('channel', default=None, type=None)}
    else:
        abort(404, 'Bad Request')

    results = list(db['daily_stats'].find(query))

    for result in results:
        del result['_id']

    return results

#     if request.user_active == False:
#         print request.user_active
#         abort(401)
#     else:
#         logoutMnemo()
#         jar = setMnemosyneCookie()
#         rheaders = {'Connection': 'close', 'Accept': 'application/json'}
#         date = datetime.date.today()
#         print date.strftime("%Y%m%d")
#         print jar["beaker.session.id"]
#         rheaders["Cookie"] = "beaker.session.id=" + jar["beaker.session.id"]
#         print rheaders
#         auth_request = requests.get("https://mhn.h-i-r.net:8181/api/v1/hpfeeds/stats?date=" + date.strftime("%Y%m%d"), headers=rheaders, verify=False)
#         return json.loads(auth_request.text)

# def setMnemosyneCookie():
#     global MNEMOSYNE_COOKIE
#     rheaders = {'Connection': 'close', 'Accept': 'application/json'}
#     auth_request = requests.post("https://mhn.h-i-r.net:8181/login", data=AUTH_PAYLOAD, headers=rheaders, verify=False)
#     print auth_request
#     MNEMOSYNE_COOKIE = auth_request.cookies
#     return auth_request.cookies

# def logoutMnemo():
#     rheaders = {'Connection': 'close', 'Accept': 'application/json'}
#     auth_request = requests.get("https://mhn.h-i-r.net:8181/logout", headers=rheaders, verify=False)