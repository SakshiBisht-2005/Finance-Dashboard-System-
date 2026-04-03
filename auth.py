import sqlite3
from werkzeug.security import generate_password_hash,check_password_hash

def register_user(username, password, role):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    hashed_password = generate_password_hash(password)

    try:
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, hashed_password, role)
        )
        conn.commit()
        return True

    except sqlite3.IntegrityError:
        # ONLY duplicate username error
        return False

    finally:
        conn.close()


def login_user(username, password):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("SELECT password, role FROM users WHERE username=?", (username,))
    user = cursor.fetchone()

    conn.close()

    if user and check_password_hash(user[0], password):
        return user[1]  # role

    return None