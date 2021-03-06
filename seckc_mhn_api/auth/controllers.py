'''auth_module
'''
import json
from functools import wraps
from flask import Blueprint, request
import requests
import certifi
from seckc_mhn_api.config import SETTINGS

# Define the blueprint: 'auth', set its url prefix: app.url/auth
AUTH_MODULE = Blueprint('auth', __name__, url_prefix='/auth')

CHUNK_SIZE = 1024

@AUTH_MODULE.route("/me", methods=['GET'])
def auth_me():
    request_headers = dict(request.headers.items())
    if 'Cookie' in request_headers:
        headers = {"Cookie": request_headers["Cookie"],
                   'Connection': 'close', 'Accept': 'application/json'}
        auth_request = requests.get("https://mhn.h-i-r.net/auth/me/", headers=headers, verify=certifi.where())
        try:
            auth_response = auth_request.json()
            return json.loads(auth_request.text)
        except ValueError:
            return {"active": False}

    # If no Cookie header, return active false
    return {"active": False}

def user_status(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        request_headers = dict(request.headers.items())
        if 'Cookie' in request_headers:
            headers = {"Cookie": request_headers["Cookie"],
                       'Connection': 'close', 'Accept': 'application/json'}
            auth_request = requests.get("https://mhn.h-i-r.net/auth/me/", headers=headers, verify=certifi.where())
            try:
                auth_response = auth_request.json()
                request.user_active = auth_response["active"]
                #exit wrapper now
                return f(*args, **kwargs)
            except ValueError:
                request.user_active = False
        # If no Cookie header, return active false
        request.user_active = False
        return f(*args, **kwargs)
    return decorated_function

def socket_user_status(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        request_headers = dict(request.headers.items())
        if 'Accept-Language' in request_headers:
            headers = {"Cookie": unicode.encode(request_headers["Accept-Language"]),
                       'Connection': 'close', 'Accept': 'application/json'}
            try:
                auth_request = requests.get("https://mhn.h-i-r.net/auth/me/",
                                            headers=headers, verify=certifi.where())
                auth_response = auth_request.json()
                request.user_active = auth_response["active"]
                #exit wrapper now
                return f(*args, **kwargs)
            except ValueError:
                request.user_active = False
            except:
                request.user_active = False

        # If no Cookie header, return active false
        request.user_active = False
        return f(*args, **kwargs)
    return decorated_function
