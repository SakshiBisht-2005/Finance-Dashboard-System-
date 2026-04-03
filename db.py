import sqlite3

def init_db():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    # TRANSACTIONS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        amount REAL,
        category TEXT,
        date TEXT
    )
    """)
    

    conn.commit()
    conn.close()

def get_connection():
    conn = sqlite3.connect("finance.db")
    conn.row_factory = sqlite3.Row  # access like dict
    return conn