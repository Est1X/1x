import sqlite3
def open_db():
    try:
        db = sqlite3.connect('user_data.db', check_same_thread=False)
        cursor = db.cursor()
        return cursor,db
    except Exception as e:
        print(e)
def create_db():
    cursor,db = open_db()
    try:
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS creds (login TEXT,password TEXT, user_id INT, username TEXT, user_tg TEXT)''')
        db.commit()
        db.close()
    except Exception as e:
        print(e)
def insert_db(login,password, user_id, username, user_tg):
    cursor, db = open_db()
    try:
        cursor.execute(f'''INSERT INTO creds (login,password, user_id, username, user_tg) VALUES ("{login}","{password}", "{user_id}", "{username}", "{user_tg}")''')
        db.commit()
        db.close()
    except Exception as e:
        print(e)

def select_db(data,column,log):
    try:
        cursor, db = open_db()
        data = cursor.execute(f'''SELECT {data} FROM creds WHERE {column}="{log}"''').fetchall()
        return data
    except Exception as e:
        print(e)
def select_id(id,log,pas):
    try:
        cursor, db = open_db()
        data = cursor.execute(f'''SELECT {id} FROM creds WHERE login="{log}" and password ="{pas}"''').fetchall()
        return data
    except Exception as e:
        print(e)
def check_login(login,password):
    try:
        cursor, db = open_db()
        user_login = cursor.execute(f'''SELECT login FROM creds WHERE login="{login}" and password="{password}"''').fetchone()
        return user_login
    except Exception as e:
        print(e)