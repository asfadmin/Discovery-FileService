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
    def generate_data(file_size=1000, slow=0):
        generated = 0
        block_size = 1000
        letters = string.ascii_letters
        while generated < file_size:
            generated += block_size
            yield ''.join(random.choice(letters) for i in range(block_size))
            if slow > 0:
                time.sleep(slow / 100000)

    file_size = min(int(request.values.get('bytes', 1000)), int(1e10))  # 10GB max
    slow = int(request.values.get('slow', 0))  # microseconds between file chunks
    return application.response_class(stream_with_context(generate_data(
        file_size=file_size,
        slow=slow
    ), mimetype='text/plain',
    headers={
        'content-length': 1000 * ceil(file_size / 1000)
    }))


# Run a dev server
if __name__ == '__main__':
    sys.dont_write_bytecode = True  # prevent clutter
    application.debug = True  # enable debugging mode
    FORMAT = "[%(filename)18s:%(lineno)-4s - %(funcName)18s() ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)  # enable debugging output
    application.run(threaded=True)  # run threaded to prevent a broken pipe error
