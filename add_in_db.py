import sqlite3


def add_in_db(name, author, number, keywords):
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    cur.execute("SELECT COUNT (*) FROM library")
    rowcount = cur.fetchone()[0]
    print(rowcount)
    cur.execute(f"""INSERT INTO library (id, name, author, number, keywords) 
    VALUES ({rowcount + 1}, '{name}', '{author}', {number}, '{keywords}');""")
    conn.commit()
    cur.close()
    conn.close()
