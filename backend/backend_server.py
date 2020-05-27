from flask import Flask, jsonify

from database.database import insert_progress
from datetime import datetime
from backend.recognition_service import RecognitionService

app = Flask(__name__)

ATTEMPTS_COUNT = 0
LETTER_TO_BE_SHOWN = "A"
rs = RecognitionService()


@app.route('/check', methods=['GET'])
def check():
    global ATTEMPTS_COUNT
    last_letter = rs.last_letter()
    if LETTER_TO_BE_SHOWN == last_letter:
        insert_progress([datetime.today(), LETTER_TO_BE_SHOWN, ATTEMPTS_COUNT, 1])
        ATTEMPTS_COUNT = 0
        return jsonify({"success": True, "last_letter": last_letter})
    else:
        ATTEMPTS_COUNT += 1
        return jsonify({"success": False, "last_letter": last_letter})


@app.route('/currentletter', methods=['GET'])
def get_letter():
    return LETTER_TO_BE_SHOWN


@app.route('/skip', methods=['POST'])
def skip():
    pass


if __name__ == '__main__':
    rs.run()
    app.run()
