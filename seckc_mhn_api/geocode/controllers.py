'''auth_module
'''
import os
import json
from flask import Blueprint, request
import requests
from seckc_mhn_api.config import SETTINGS
import geoip2.database

script_dir = os.path.dirname(__file__)
abs_file_path = os.path.dirname(os.path.realpath(__file__))
abs_file_path = os.path.join(abs_file_path, "../../geodatabase/GeoLite2-City.mmdb")

# Define the blueprint: 'geocode', set its url prefix: app.url/geocode
GEOCODE_MODULE = Blueprint('geocode', __name__, url_prefix='/geocode')

reader = geoip2.database.Reader(abs_file_path)

@GEOCODE_MODULE.route("/<ip>", methods=['GET'])
def geocode(ip):
    #print reader.city("136.32.181.16")
    response = reader.city(ip)
    return response.raw

def geocodeinternal(ip):
    #print reader.city("136.32.181.16")
    response = reader.city(ip)
    return response.raw
