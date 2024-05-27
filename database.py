import sqlite3
from expenses.expense import Expense

class Database:
    def __init__(self, db_name='expenses.db'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL,
                category TEXT,
                description TEXT,
                payment_method TEXT,
                date DATE,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        ''')
        self.connection.commit()

    def add_user(self, username, password):
        try:
            self.cursor.execute('''
                INSERT INTO users (username, password) VALUES (?, ?)
            ''', (username, password))
            self.connection.commit()
        except sqlite3.IntegrityError:
            raise ValueError("Username already exists")

    def get_user(self, username, password):
        self.cursor.execute('''
            SELECT * FROM users WHERE username = ? AND password = ?
        ''', (username, password))
        return self.cursor.fetchone()

    def del_user(self, username):
        self.cursor.execute('''
            DELETE FROM users WHERE username = ?
        ''', (username,))
        self.connection.commit()

    def get_user_id(self, username):
        self.cursor.execute('''
            SELECT id FROM users WHERE username = ?
        ''', (username,))
        return self.cursor.fetchone()[0]

    def add_expense(self, user_id, expense: Expense):
        self.cursor.execute('''
            INSERT INTO expenses (user_id, amount, category, description, payment_method, date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, expense.amount, expense.category, expense.description, expense.payment_method, expense.date))
        self.connection.commit()

    def get_expenses(self, user_id):
        self.cursor.execute('''
            SELECT * FROM expenses WHERE user_id = ?
        ''', (user_id,))
        return self.cursor.fetchall()

    def del_expense(self, expense_id):
        self.cursor.execute('''
            DELETE FROM expenses WHERE id = ?
        ''', (expense_id,))
        self.connection.commit()

    def add_category(self, name):
        self.cursor.execute('''
            INSERT INTO categories (name) VALUES (?)
        ''', (name,))
        self.connection.commit()

    def get_categories(self):
        self.cursor.execute('''
            SELECT * FROM categories
        ''')
        return self.cursor.fetchall()

    def del_category(self, category_id):
        self.cursor.execute('''
            DELETE FROM categories WHERE id = ?
        ''', (category_id,))

    # for tests
    def get_columns(self):
        self.cursor.execute("PRAGMA table_info(expenses)")
        columns = self.cursor.fetchall()
        column_names = [column[1] for column in columns]
        return column_names





