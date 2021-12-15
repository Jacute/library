import json

from flask import Flask, request
import logging


app = Flask(__name__)


@app.route('/', methods=['POST'])
def main():
    logging.info(request.json)

    response = {
        'version': request.json['version'],
        'session': request.json['session'],
        'response': {
            'end_session': False
        }
    }

    if request.json['session']['new']:
        response['response']['text'] = 'Привет! Отправь мне ключевое слово,' \
                                       ' по которому ты хочешь найти книги,' \
                                       ' а я выведу список всех доступных произведений из библиотеки.'

    return json.dumps(response)


if __name__ == '__main__':
    # db_session.global_init("db/data.sqlite")
    app.run(debug=False)
