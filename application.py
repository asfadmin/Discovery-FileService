from flask import Flask
from flask import request
from flask_cors import CORS
from flask_talisman import Talisman
import sys
import logging
import string
import random
import time

app = Flask(__name__)
CORS(app, send_wildcard=True)
talisman = Talisman(app)


# Just send a file
@app.route('/generate', methods = ['GET', 'POST'])
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

    file_size = min(int(request.values.get('bytes', 1000)), 1e10)  # 10GB max
    slow = int(request.values.get('slow', 0))  # microseconds between file chunks
    return app.response_class(generate_data(
        file_size=file_size,
        slow=slow
    ), mimetype='text/plain')


# Run a dev server
if __name__ == '__main__':
    sys.dont_write_bytecode = True  # prevent clutter
    app.debug = True  # enable debugging mode
    FORMAT = "[%(filename)18s:%(lineno)-4s - %(funcName)18s() ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)  # enable debugging output
    app.run(threaded=True)  # run threaded to prevent a broken pipe error
