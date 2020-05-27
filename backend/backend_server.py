from flask import Flask, jsonify

app = Flask(__name__)

LETTER_TO_BE_SHOWN = "A"


@app.route('/check', methods=['GET'])
def check():
    pass
    # check if success, return JSON


@app.route('/letter', methods=['GET'])
def get_letter():
    return LETTER_TO_BE_SHOWN


@app.route('/skip', methods=['POST'])
def skip():
    pass


if __name__ == '__main__':
    # run camera service
    app.run()
