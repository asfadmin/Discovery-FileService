from flask import Flask
from flask import request
from flask import stream_with_context
from flask_cors import CORS
from flask_talisman import Talisman
from math import ceil
import sys
import logging
import string
import random
import time

application = Flask(__name__)
CORS(application, send_wildcard=True)
talisman = Talisman(application)


# Add a default endpoint for health checks
@application.route('/')
def health_report():
    return 'I feel fine'


# Just send a file
@application.route('/generate', methods = ['GET', 'POST'])
def generate_file():
    block_size = 1000

    def generate_data(file_size=block_size, slow=0):
        generated = 0
        with open('/dev/random', 'rb') as devrand:
            while generated < file_size:
                generated += block_size
                yield devrand.read(block_size)
                if slow > 0:
                    time.sleep(slow / 100000)

    file_size = min(float(request.values.get('bytes', block_size)), int(1e10))  # 10GB max
    slow = int(request.values.get('slow', 0))  # microseconds between file chunks
    return application.response_class(stream_with_context(generate_data(
        file_size=file_size,
        slow=slow
    )), mimetype='application/octet-stream',
        headers={
            'content-length': block_size * ceil(file_size / block_size)
    })


# Run a dev server
if __name__ == '__main__':
    sys.dont_write_bytecode = True  # prevent clutter
    application.debug = True  # enable debugging mode
    FORMAT = "[%(filename)18s:%(lineno)-4s - %(funcName)18s() ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)  # enable debugging output
    application.run(threaded=True)  # run threaded to prevent a broken pipe error
