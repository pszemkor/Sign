from threading import Thread

from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

import string
import random

from database.database import insert_progress, set_up_database
from datetime import datetime
from backend.recognition_service import RecognitionService

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

ATTEMPTS_COUNT = 0
LETTER_TO_BE_SHOWN = "A"
rs = RecognitionService()


def set_random_letter():
    global LETTER_TO_BE_SHOWN
    random_letter = random.choice(string.ascii_letters.upper())
    while random_letter == LETTER_TO_BE_SHOWN:
        random_letter = random.choice(string.ascii_letters.upper())
    LETTER_TO_BE_SHOWN = random_letter


@app.route('/check', methods=['GET'])
@cross_origin()
def check():
    global ATTEMPTS_COUNT
    last_letter = rs.last_letter()
    if LETTER_TO_BE_SHOWN == last_letter:
        insert_progress([datetime.today(), LETTER_TO_BE_SHOWN, ATTEMPTS_COUNT, 1])
        ATTEMPTS_COUNT = 0
        set_random_letter()
        return jsonify({"success": True, "last_letter": last_letter, "new_letter": LETTER_TO_BE_SHOWN})
    else:
        ATTEMPTS_COUNT += 1
        return jsonify({"success": False, "last_letter": last_letter, "new_letter": None})


@app.route('/currentletter', methods=['GET'])
@cross_origin()
def get_letter():
    return LETTER_TO_BE_SHOWN


@app.route('/skip', methods=['POST'])
@cross_origin()
def skip():
    global ATTEMPTS_COUNT
    last_letter = rs.last_letter()
    insert_progress([datetime.today(), LETTER_TO_BE_SHOWN, ATTEMPTS_COUNT, 0])
    ATTEMPTS_COUNT = 0
    set_random_letter()
    return jsonify({"success": False, "last_letter": last_letter, "new_letter": LETTER_TO_BE_SHOWN})


if __name__ == '__main__':
    set_up_database()
    thread = Thread(target=app.run)
    thread.start()
    rs.run()