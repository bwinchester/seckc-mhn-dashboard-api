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

NOTES = {
    0: 'do the shopping',
    1: 'build the codez',
    2: 'paint the door',
}

def note_repr(key):
    return {
        'url': request.host_url.rstrip('/') + url_for('notes_detail', key=key),
        'text': NOTES[key]
    }

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


@APP.route("/", methods=['GET', 'POST'])
@user_status
def notes_list():
    """
    List or create notes.
    """
    print("test")
    print(request.user_active)

    if request.method == 'POST':
        note = str(request.data.get('text', ''))
        idx = max(NOTES.keys()) + 1
        NOTES[idx] = note
        return note_repr(idx), status.HTTP_201_CREATED

    # request.method == 'GET'
    return [note_repr(idx) for idx in sorted(NOTES.keys())]


@APP.route("/<int:key>/", methods=['GET', 'PUT', 'DELETE'])
def notes_detail(key):
    """
    Retrieve, update or delete note instances.
    """
    if request.method == 'PUT':
        note = str(request.data.get('text', ''))
        NOTES[key] = note
        return note_repr(key)

    elif request.method == 'DELETE':
        NOTES.pop(key, None)
        return '', status.HTTP_204_NO_CONTENT

    # request.method == 'GET'
    if key not in NOTES:
        raise exceptions.NotFound()
    return note_repr(key)

if __name__ == "__main__":
    SOCKET_IO_APP.run(APP)