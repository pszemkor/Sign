from flask import Flask, jsonify

from backend.recognition_service import RecognitionService

app = Flask(__name__)

LETTER_TO_BE_SHOWN = "A"
rs = RecognitionService()


@app.route('/check', methods=['GET'])
def check():
    last_letter = rs.last_letter()
    if LETTER_TO_BE_SHOWN == last_letter:
        return jsonify({"success": True, "last_letter": last_letter})
    else:
        return jsonify({"success": False, "last_letter": last_letter})


@app.route('/letter', methods=['GET'])
def get_letter():
    return LETTER_TO_BE_SHOWN


@app.route('/skip', methods=['POST'])
def skip():
    pass


if __name__ == '__main__':
    # run camera service
    rs.run()
    app.run()
