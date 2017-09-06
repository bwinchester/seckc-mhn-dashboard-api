'''create an hpfeeds relay
'''
import sys
import logging
import traceback
import json
import threading
import hpfeeds
from seckc_mhn_api.config import SETTINGS
from socketIO_client import SocketIO, LoggingNamespace

logging.basicConfig(level=logging.WARNING)

HOST = SETTINGS["hpfeeds"]["host"]
PORT = SETTINGS["hpfeeds"]["port"]
CHANNELS = SETTINGS["hpfeeds"]["channels"]
IDENT = SETTINGS["hpfeeds"]["user"]
SECRET = SETTINGS["hpfeeds"]["token"]

print HOST, PORT, CHANNELS, IDENT, SECRET

def main():
    hpc = hpfeeds.new(HOST, PORT, IDENT, SECRET)
    print >>sys.stderr, 'connected to', hpc.brokername

    myconnection = SocketIO('localhost', 5000, LoggingNamespace)
    def on_message(ident, channel, payload):
        try:
            dec = json.loads(str(payload))
            #del dec['daddr']
            dec['identifier'] = ident
            enc = json.dumps(dec)

            myconnection.emit('hpfeedevent', enc)

        except:
            traceback.print_exc()
            print >>sys.stderr, 'forward error for message from {0}.'.format(ident)
            return

        #hpc.publish(RELAYCHAN, enc)

    def on_error(payload):
        print >>sys.stderr, ' -> errormessage from server: {0}'.format(payload)
        hpc.stop()

    hpc.subscribe(CHANNELS)
    hpc.run(on_message, on_error)
    hpc.close()
    return 0

def start():
    mythread = threading.Thread(target=main)
    mythread.daemon = True
    mythread.start()

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(0)
