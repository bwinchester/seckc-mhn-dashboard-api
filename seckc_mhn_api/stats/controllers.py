'''auth_module
'''
import os
import json
from datetime import datetime
from flask import Blueprint, request, abort
import requests
from seckc_mhn_api.config import SETTINGS
from seckc_mhn_api.auth.controllers import user_status
import certifi

# Define the blueprint: 'stats', set its url prefix: app.url/stats
STATS_MODULE = Blueprint('stats', __name__, url_prefix='/stats')

MNEMOSYNE_COOKIE = None
AUTH_PAYLOAD = {
    "username": SETTINGS["mnemosyne"]["username"],
    "password": SETTINGS["mnemosyne"]["password"]
}

@STATS_MODULE.route("/", methods=['GET'])
@user_status
def getstats():
    if request.user_active is False:
        abort(401)
    else:
        rheaders = {'Connection': 'close', 'Accept': 'application/json'}
        if MNEMOSYNE_COOKIE is None: 
            setMnemosyneCookie()
            date = datetime.date
            auth_request = requests.get("https://mhn.h-i-r.net:8181/api/v1/hpfeeds/stats?date=" + "{:%Y%m%d}".format(datetime.now()), cookies=MNEMOSYNE_COOKIE, headers=rheaders, verify=False)
            return json.loads(auth_request.text)
        else:
            date = datetime.date
            auth_request = requests.get("https://mhn.h-i-r.net:8181/api/v1/hpfeeds/stats?date=" + "{:%Y%m%d}".format(datetime.now()), cookies=MNEMOSYNE_COOKIE, headers=rheaders, verify=False)
            return json.loads(auth_request.text)

def setMnemosyneCookie():
    global MNEMOSYNE_COOKIE
    rheaders = {'Connection': 'close', 'Accept': 'application/json'}
    auth_request = requests.post("https://mhn.h-i-r.net:8181/login", data=AUTH_PAYLOAD, headers=rheaders, verify=False)
    print auth_request.cookies
    MNEMOSYNE_COOKIE = auth_request.cookies