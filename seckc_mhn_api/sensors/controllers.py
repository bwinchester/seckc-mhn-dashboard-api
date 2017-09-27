'''sensors_module
'''
import os
import json
from flask import Blueprint, request
import requests
from seckc_mhn_api.config import SETTINGS
import certifi
from seckc_mhn_api.geocode.controllers import geocodeinternal

# Define the blueprint: 'geocode', set its url prefix: app.url/geocode
SENSORS_MODULE = Blueprint('sensors', __name__, url_prefix='/sensors')

@SENSORS_MODULE.route("/locations", methods=['GET'])
def sensors():
    sensorurl =  "https://mhn.h-i-r.net/api/sensor/?api_key=" + SETTINGS["mhn"]["apikey"]
    sensor_request = requests.get(sensorurl, verify=certifi.where())
    sensorjson = []
    print sensor_request
    if sensor_request.status_code == 200:
        responsejson = sensor_request.json()
        for sensor in responsejson:
            sensorlookup = geocodeinternal(sensor["ip"])
            if sensorlookup["traits"] is not None:
                del sensorlookup["traits"]
            sensorjson.append(sensorlookup)
        return sensorjson

    # If no Cookie header, return active false
    return {"active": False}
