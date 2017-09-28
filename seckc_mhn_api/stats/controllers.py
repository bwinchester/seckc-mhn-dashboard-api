'''stats_module
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

@STATS_MODULE.route("/attacks", methods=['GET'])
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

@STATS_MODULE.route("/attackers", methods=['GET'])
def getattackers():
    attackerurl =  "https://mhn.h-i-r.net/api/top_attackers/?hours_ago=24&api_key=" + SETTINGS["mhn"]["apikey"]
    top_attacker_request = requests.get(attackerurl, verify=certifi.where())
    if top_attacker_request.status_code == 200:
        return top_attacker_request.json()
    return {}

@STATS_MODULE.route("/attacker/<ip>", methods=['GET'])
def getattackerstats(ip):
    attackerstaturl =  "https://mhn.h-i-r.net/api/attacker_stats/" + ip + "/?api_key=" + SETTINGS["mhn"]["apikey"]
    attacker_request = requests.get(attackerstaturl, verify=certifi.where())
    if attacker_request.status_code == 200:
        return attacker_request.json()
    return {}