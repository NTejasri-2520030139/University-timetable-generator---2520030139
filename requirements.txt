"""
models/user.py — User model and authentication helpers
"""

import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


def get_db():
    from app import DATABASE
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


class User:
    def __init__(self, row):
        self.id = row['id']
        self.fullname = row['fullname']
        self.email = row['email']
        self.role = row['role']
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        return str(self.id)

    @staticmethod
    def get_by_id(user_id):
        db = get_db()
        row = db.execute('SELECT * FROM users WHERE id=?', (user_id,)).fetchone()
        db.close()
        return User(row) if row else None

    @staticmethod
    def get_by_email(email):
        db = get_db()
        row = db.execute('SELECT * FROM users WHERE email=?', (email,)).fetchone()
        db.close()
        return row

    @staticmethod
    def create(fullname, email, password, role):
        db = get_db()
        pw_hash = generate_password_hash(password)
        try:
            db.execute(
                'INSERT INTO users (fullname, email, password, role) VALUES (?,?,?,?)',
                (fullname, email, pw_hash, role)
            )
            db.commit()
            return True, None
        except sqlite3.IntegrityError:
            return False, 'Email already registered.'
        finally:
            db.close()

    @staticmethod
    def verify_password(stored_hash, password):
        return check_password_hash(stored_hash, password)

    @staticmethod
    def get_all_teachers():
        db = get_db()
        rows = db.execute("SELECT * FROM users WHERE role='teacher'").fetchall()
        db.close()
        return [dict(r) for r in rows]
