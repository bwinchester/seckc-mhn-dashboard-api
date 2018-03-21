"""Base API. Import all modules Here. Attach middleware.
"""
from os import environ as environment
from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from seckc_mhn_api.config import SETTINGS
from flask_socketio import SocketIO
from flask_cors import CORS


# print(environment["HOME"])
# print(SETTINGS)

APP = FlaskAPI(__name__)
SOCKET_IO_APP = SocketIO(APP)

#import modules here
from seckc_mhn_api.auth.controllers import AUTH_MODULE, user_status
from seckc_mhn_api.geocode.controllers import GEOCODE_MODULE
from seckc_mhn_api.stats.controllers import STATS_MODULE
from seckc_mhn_api.sensors.controllers import SENSORS_MODULE

import seckc_mhn_api.feeds.hpfeed_relay
seckc_mhn_api.feeds.hpfeed_relay.start()
import seckc_mhn_api.feeds.controllers

# Register blueprint(s)
APP.register_blueprint(AUTH_MODULE)
APP.register_blueprint(GEOCODE_MODULE)
APP.register_blueprint(STATS_MODULE)
APP.register_blueprint(SENSORS_MODULE)

@APP.after_request
def manage_security_headers(response):
    response.headers["Server"] = ""
    return response

if __name__ == "__main__":
    SOCKET_IO_APP.run(APP)
