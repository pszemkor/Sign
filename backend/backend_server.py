from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', methods=['GET'])
@app.route('/index.html', methods=['GET'])
def my_form():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
