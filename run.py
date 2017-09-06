'''RUN seckc hpfeeds api
'''
from seckc_mhn_api.api_base import APP, SOCKET_IO_APP

SOCKET_IO_APP.run(APP)

# APP.config["host"] = '0.0.0.0'
# APP.config["port"] = 5000
# APP.config["debug"] = True
#SOCKET_IO_APP.run(APP,host='0.0.0.0', port=5000, debug=True)
