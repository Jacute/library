from flask import Flask, request
import logging


app = Flask(__name__)


@app.route('/', methods=['POST'])
def main():
    logging.info(request.json)


if __name__ == '__main__':
    # db_session.global_init("db/data.sqlite")
    app.run(debug=False, port=5000)
