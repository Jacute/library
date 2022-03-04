import json
import sqlite3
from flask import Flask, request
from db_func import add_in_db, delete_from_db
import logging
import re


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
    req = request.json['request']['original_utterance']
    if request.json['session']['new']:
        response['response']['text'] = 'Привет! Отправь мне ключевое слово,' \
                                       ' по которому ты хочешь найти книги,' \
                                       ' а я выведу список всех доступных произведений из библиотеки.'
    elif req == 'Помощь' or \
            req == 'Что ты умеешь?':
        response['response']['text'] = 'Я ищу книги из библиотеки по ключевым словам. Отправь мне его,' \
                                       ' а я выведу список всех доступных произведений из библиотеки.\n' \
                                       'Также я могу:\n' \
                                       '- Добавлять новые книги в библиотеку. Отправь мне данную команду:\n' \
                                       '    + "Название произведения;Автор;Номер;Ключевые слова"\n' \
                                       'Пример: + "Тарас Бульба;Н.В.Гоголь;10059;товарищество,братство,повесть"\n\n' \
                                       '- Удалять книги из библиотеки. Отправь мне данную команду:\n' \
                                       '    - "Номер книги"\n' \
                                       'Пример: - "10059"\n\n' \
                                       'Приятного пользования! ;)'
    elif re.match(r'\+ "[^;]+;[^;]+;\d+;[^;]+"', req):
        a = re.findall('[^;]+', req)
        name, author, number, keywords = a[0][3:], a[1], int(a[2]), a[3][:-1]
        try:
            f_code = add_in_db(name, author, number, keywords)
            if f_code:
                response['response']['text'] = 'Ваша запись была успешно добавлена в библиотеку!'
            else:
                response['response']['text'] = 'Запись с таким же номером уже существует'
        except Exception:
            response['response']['text'] = 'Что-то пошло не так! Попробуйте ещё раз...'
    elif re.match(r'- "\d+"', req):
        a = re.findall('\d+', req)
        number = int(a[0])
        try:
            f_code = delete_from_db(number)
            if f_code:
                response['response']['text'] = 'Ваша запись была успешно удалена из библиотеки!'
            else:
                response['response']['text'] = 'Запись с таким же номером отсутствует'
        except Exception:
            response['response']['text'] = 'Что-то пошло не так! Попробуйте ещё раз...'
    else:
        if req.isnumeric():
            req = str(req)
        conn = sqlite3.connect('db.db')
        cur = conn.cursor()
        cur.execute("""SELECT * from library""")
        records = cur.fetchall()
        result = []
        for i in records:
            if req.lower() in i[1].lower() or req.lower() in i[2].lower() or\
                    req.lower() in i[4].lower() or req == str(i[3]):
                result.append([i[1], i[2], str(i[3])])
        if result and len(req) >= 3:
            res = '\n'.join([' '.join(i) for i in result])
            response['response']['text'] = res if len(res) <= 1024 else res[:1021] + '...'
        else:
            response['response']['text'] = 'Извините, по данному запросу произведения не найдены.' \
                                           ' Попробуйте ещё раз.'
        cur.close()
        conn.close()
    return json.dumps(response)


if __name__ == '__main__':
    # db_session.global_init("db/data.sqlite")
    app.run(debug=False)
