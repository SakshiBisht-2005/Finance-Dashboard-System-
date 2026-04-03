import sqlite3
from db import get_connection
def add_transaction(type, amount, category, date):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO transactions (type, amount, category, date) VALUES (?, ?, ?, ?)",
        (type, amount, category, date)
    )

    conn.commit()
    conn.close()


def get_income():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='income'")
    result = cursor.fetchone()[0]

    conn.close()
    return result if result else 0


def get_expense():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='expense'")
    result = cursor.fetchone()[0]

    conn.close()
    return result if result else 0


def get_transactions():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions ORDER BY id DESC")
    data = cursor.fetchall()

    conn.close()
    return data

def delete_transaction(id):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM transactions WHERE id=?", (id,))
    conn.commit()
    conn.close()


def get_transaction_by_id(id):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions WHERE id=?", (id,))
    data = cursor.fetchone()

    conn.close()
    return data


def update_transaction(id, type, amount, category, date):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE transactions
        SET type=?, amount=?, category=?, date=?
        WHERE id=?
    """, (type, amount, category, date, id))

    conn.commit()
    conn.close()

def get_user_counts():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users WHERE role='admin'")
    admin = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM users WHERE role='analyst'")
    analyst = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM users WHERE role='viewer'")
    viewer = cursor.fetchone()[0]

    conn.close()

    return admin, analyst, viewer


# 📅 Monthly Data
def get_monthly_data(month=None):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date, SUM(amount)
        FROM transactions
        WHERE strftime('%Y-%m', date) = ?
        GROUP BY date
        ORDER BY date
    """, (month,))

    data = cursor.fetchall()
    conn.close()

    dates = [row[0] for row in data]
    amounts = [row[1] for row in data]

    return dates, amounts


# 🔍 Search Transactions
def search_transactions(keyword):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM transactions
        WHERE type LIKE ? OR category LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%"))

    data = cursor.fetchall()
    conn.close()

    return data

def get_category_expense():
    import sqlite3

    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM transactions
        WHERE type='expense'
        GROUP BY category
    """)

    data = cursor.fetchall()
    conn.close()

    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    return categories, amounts

def insert_dummy_data():
    conn = get_connection()
    cursor = conn.cursor()

    data = [
        ("income", 50000, "Salary", "2026-04-01"),
        ("income", 2000, "Freelance", "2026-04-05"),
        ("expense", 2000, "Food", "2026-04-02"),
        ("expense", 3000, "Rent", "2026-04-03"),
        ("expense", 1000, "Travel", "2026-04-06"),
        ("expense", 500, "Entertainment", "2026-04-07"),
    ]

    cursor.executemany(
        "INSERT INTO transactions (type, amount, category, date) VALUES (?, ?, ?, ?)",
        data
    )

    conn.commit()
    conn.close()