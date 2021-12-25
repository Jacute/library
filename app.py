import json
import sqlite3
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
    else:
        req = request.json['request']['original_utterance']
        conn = sqlite3.connect('db.db')
        cur = conn.cursor()
        cur.execute("""SELECT * from library""")
        records = cur.fetchall()
        result = []
        for i in records:
            if req.lower() in i[1].lower() or req.lower() in i[2].lower() or\
                    req.lower() in i[4].lower():
                result.append([i[1], i[2], str(i[3])])
        if result:
            response['response']['text'] = '\n'.join([' '.join(i) for i in result])
        else:
            response['response']['text'] = 'Извините, по данному запросу произведения не найдены.' \
                                           ' Попробуйте ещё раз.'
        cur.close()
        conn.close()
    return json.dumps(response)


if __name__ == '__main__':
    # db_session.global_init("db/data.sqlite")
    app.run(debug=False)
