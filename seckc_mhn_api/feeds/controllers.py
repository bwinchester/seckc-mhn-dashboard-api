'''register sockets
'''
import json
from seckc_mhn_api.api_base import SOCKET_IO_APP
from seckc_mhn_api.auth.controllers import socket_user_status
from flask import request
from flask_socketio import join_room, emit

def sanitize_data(d):
    if not isinstance(d, (dict, list)):
        return d
    if isinstance(d, list):
        return [sanitize_data(v) for v in d]
    return {k: sanitize_data(v) for k, v in d.items()
            if k not in {'hostIP', 'local_host', 'victimIP'}}

@SOCKET_IO_APP.on('hpfeedevent')
def handle_my_custom_event(data):
    #print('received json: ' + str(json))
    emit('hpfeedevent', json.loads(data), room='activeUsers')
    sanitized = sanitize_data(json.loads(data))
    sanitized_json = None
    try:
        sanitized_json = sanitized
        #print sanitized_json
    except:
        print 'didntwork'

    emit('hpfeedevent', sanitized_json, room='anonUsers')

@SOCKET_IO_APP.on('connect')
@socket_user_status
def see_user_maybe_join():
    useragent = unicode.encode(request.headers["User-Agent"])
    if request.user_active is True:
        print "auth user connected"
        join_room("activeUsers")
    else:
        if useragent.startswith("python-requests") == False:
            print "anon user joined"
            join_room("anonUsers")
