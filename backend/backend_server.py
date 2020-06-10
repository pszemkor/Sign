from threading import Thread

from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

import string
import random

from database.database import insert_progress, set_up_database, get_data, get_stats_data
from datetime import datetime
from backend.recognition_service import RecognitionService

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

ATTEMPTS_COUNT = 0

MINIMAL_TOTAL_ATTEMPTS = 10
MINIMAL_RATIO = 0.7

LETTER_TO_BE_SHOWN = "A"
rs = RecognitionService()


def set_random_letter():
    global LETTER_TO_BE_SHOWN

    stats = get_stats_data()
    alphabet_set = set(string.ascii_uppercase)

    for entry in stats:
        entry['total'] = entry['successes'] + entry['failures']
        entry['ratio'] = 0 if entry['total'] == 0 else entry['successes'] / entry['total']
        alphabet_set.remove(entry['sign'])

    for letter in alphabet_set:
        letter_stats = {'sign': letter, 'successes': 0, 'failures': 0, 'total': 0, 'ratio': 0}
        stats.append(letter_stats)

    remaining_letters = []
    for entry in stats:
        if entry['total'] < MINIMAL_TOTAL_ATTEMPTS or entry['ratio'] < MINIMAL_RATIO:
            remaining_letters.append(entry['sign'])

    if not remaining_letters:
        remaining_letters = list(string.ascii_uppercase)

    print('remaining letters', remaining_letters)

    random_letter = random.choice(remaining_letters)
    while random_letter == LETTER_TO_BE_SHOWN:
        random_letter = random.choice(remaining_letters)
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
def get_stats():
    return jsonify({"letter": LETTER_TO_BE_SHOWN})


@app.route('/skip', methods=['POST'])
@cross_origin()
def skip():
    global ATTEMPTS_COUNT
    last_letter = rs.last_letter()
    insert_progress([datetime.today(), LETTER_TO_BE_SHOWN, ATTEMPTS_COUNT, 0])
    ATTEMPTS_COUNT = 0
    set_random_letter()
    return jsonify({"success": False, "last_letter": last_letter, "new_letter": LETTER_TO_BE_SHOWN})


@app.route('/sessions', methods=['GET'])
@cross_origin()
def get_letter():
    data = get_data()
    return jsonify({"data": data})


@app.route('/stats', methods=['GET'])
@cross_origin()
def get_stats_things():
    data = get_stats_data()
    return jsonify({"data": data})


if __name__ == '__main__':
    set_up_database()
    thread = Thread(target=app.run)
    thread.start()
    rs.run()
