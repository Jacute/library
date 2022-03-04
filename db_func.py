import sqlite3


def add_in_db(name, author, number, keywords):
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    cur.execute("SELECT COUNT (*) FROM library;")
    rowcount = cur.fetchone()[0]
    cur.execute(f"""SELECT * from library WHERE number = {number};""")
    if cur.fetchone():
        cur.close()
        conn.close()
        return 0
    cur.execute(f"""INSERT INTO library (id, name, author, number, keywords) 
    VALUES ({rowcount + 1}, '{name}', '{author}', {number}, '{keywords}');""")
    conn.commit()
    cur.close()
    conn.close()
    return 1


def delete_from_db(number):
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    cur.execute(f"""SELECT * from library WHERE number = {number};""")
    if not cur.fetchone():
        cur.close()
        conn.close()
        return 0
    cur.execute(f"""DELETE FROM library WHERE number = {number};""")
    conn.commit()
    cur.close()
    conn.close()
    return 1
