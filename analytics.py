import sqlite3

def get_summary():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='income'")
    income = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='expense'")
    expense = cursor.fetchone()[0] or 0

    conn.close()

    return income, expense, income - expense
def get_monthly_data(month=None):
    import sqlite3

    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    if month:
        cursor.execute("""
            SELECT date, SUM(amount)
            FROM transactions
            WHERE date LIKE ?
            GROUP BY date
            ORDER BY date
        """, (month + "%",))
    else:
        cursor.execute("""
            SELECT date, SUM(amount)
            FROM transactions
            GROUP BY date
            ORDER BY date
        """)

    data = cursor.fetchall()
    conn.close()

    dates = [row[0] for row in data]
    amounts = [row[1] for row in data]

    return dates, amounts