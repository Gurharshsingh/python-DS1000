
import sqlite3

DATABASE_NAME='users.db'

def get_connection():
    conn=sqlite3.connect(DATABASE_NAME)
    conn.row_factory=sqlite3.Row
    return conn

def create_table():
    conn=get_connection()
    c=conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

