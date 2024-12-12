import sqlite3

DATABASE = 'users.db'

def test_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cars';")
        table_exists = cursor.fetchone()
        if table_exists:
            print("Cars table exists.")
        else:
            print("Cars table does not exist.")

test_db()
