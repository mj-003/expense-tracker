import sqlite3
from datetime import datetime

from financials.expense import Expense


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
                password TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                currency TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL,
                category TEXT,
                payment_method TEXT,
                date DATE,
                photo_path TEXT,
                description TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS incomes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        amount REAL,
                        sender TEXT,
                        date DATE,
                        description TEXT,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        ''')
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS payments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        amount REAL,
                        title TEXT,
                        date DATE,
                        how_often TEXT,
                        description TEXT,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                ''')
        self.connection.commit()
        self.connection.commit()

    def add_user(self, username, password, email, currency):
        try:
            self.cursor.execute('''
                INSERT INTO users (username, password, email, currency) VALUES (?, ?, ?, ?)
            ''', (username, password, email, currency))
            self.connection.commit()
            return self.cursor.lastrowid  # Return the id of the newly inserted user
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

    def get_user_currency(self, username):
        self.cursor.execute('''
            SELECT currency FROM users WHERE username = ?
        ''', (username,))
        return self.cursor.fetchone()[0]

    def change_currency(self, username, currency):
        self.cursor.execute('''
            UPDATE users
            SET currency = ?
            WHERE username = ?
        ''', (currency, username))
        self.connection.commit()

    def add_expense(self, user_id, expense: Expense):
        self.cursor.execute('''
            INSERT INTO expenses (user_id, amount, category, payment_method, date, photo_path, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, expense.amount, expense.category, expense.payment_method, expense.date, expense.photo_path,
              expense.description))
        self.connection.commit()
        return self.cursor.lastrowid

    def get_expenses(self, user_id):
        self.cursor.execute('''
            SELECT * FROM expenses WHERE user_id = ?
        ''', (user_id,))
        return self.cursor.fetchall()

    def get_expense(self, expense_id):
        self.cursor.execute('''
            SELECT * FROM expenses WHERE id = ?
        ''', (expense_id,))
        return self.cursor.fetchone()

    def update_expense(self, expense_id, expense: Expense):
        self.cursor.execute('''
            UPDATE expenses
            SET amount = ?, category = ?, payment_method = ?, date = ?, photo_path = ?, description = ?
            WHERE id = ?
        ''', (
        expense.amount, expense.category, expense.payment_method, expense.date, expense.photo_path, expense.description,
        expense_id))
        self.connection.commit()

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
        self.cursor.execute("PRAGMA table_info(financials)")
        columns = self.cursor.fetchall()
        column_names = [column[1] for column in columns]
        return column_names

    def add_income(self, user_id, income):
        self.cursor.execute('''
            INSERT INTO incomes (user_id, amount, sender, date, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, income.amount, income.sender, income.date, income.description))
        self.connection.commit()
        return self.cursor.lastrowid

    def get_incomes(self, user_id):
        self.cursor.execute('''
            SELECT * FROM incomes WHERE user_id = ?
        ''', (user_id,))
        return self.cursor.fetchall()

    def get_income(self, income_id):
        self.cursor.execute('''
            SELECT * FROM incomes WHERE id = ?
        ''', (income_id,))
        return self.cursor.fetchone()

    def update_income(self, income_id, income):
        self.cursor.execute('''
            UPDATE incomes
            SET amount = ?, sender = ?, date = ?, description = ?
            WHERE id = ?
        ''', (income.amount, income.sender, income.date, income.description, income_id))
        self.connection.commit()

    def del_income(self, income_id):
        self.cursor.execute('''
            DELETE FROM incomes WHERE id = ?
        ''', (income_id,))
        self.connection.commit()

    def add_payment(self, user_id, payment):
        self.cursor.execute('''
            INSERT INTO payments (user_id, amount, title, date, how_often, description)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, payment.amount, payment.title, payment.date, payment.how_often, payment.description))
        self.connection.commit()
        return self.cursor.lastrowid

    def get_payments(self, user_id):
        self.cursor.execute('''
            SELECT * FROM payments WHERE user_id = ?
        ''', (user_id,))
        return self.cursor.fetchall()

    def get_payment(self, payment_id):
        self.cursor.execute('''
            SELECT * FROM payments WHERE id = ?
        ''', (payment_id,))
        return self.cursor.fetchone()

    def update_payment(self, payment_id, payment):
        self.cursor.execute('''
            UPDATE payments
            SET amount = ?, title = ?, date = ?, how_often = ?, description = ?
            WHERE id = ?
        ''', (payment.amount, payment.title, payment.date, payment.how_often, payment.description, payment_id))
        self.connection.commit()

    def del_payment(self, payment_id):
        self.cursor.execute('''
            DELETE FROM payments WHERE id = ?
        ''', (payment_id,))
        self.connection.commit()

    def get_upcoming_payments(self):
        """
        Get upcoming payments (payments that are due today)
        :return:
        """
        today = datetime.now().date()
        self.cursor.execute('''
               SELECT p.*, u.username, u.email FROM payments p
               JOIN users u ON p.user_id = u.id
               WHERE p.date = ?
           ''', (today,))
        return self.cursor.fetchall()

    def update_payment_date(self, payment_id, how_often):
        """
        Update the date of the payment
        :param payment_id:
        :param how_often:
        :return:
        """
        from datetime import timedelta
        current_date = self.get_payment(payment_id)['date']
        new_date = current_date

        if how_often == 'Daily':
            new_date += timedelta(days=1)
        elif how_often == 'Weekly':
            new_date += timedelta(weeks=1)
        elif how_often == 'Monthly':
            month = current_date.month % 12 + 1
            year = current_date.year if month > 1 else current_date.year + 1
            day = min(current_date.day,
                      [31, 29 if year % 4 == 0 and not year % 400 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][
                          month - 1])
            new_date = current_date.replace(year=year, month=month, day=day)
        elif how_often == 'Yearly':
            new_date += timedelta(days=365)
        else:
            self.del_payment(payment_id)  # delete single payment

        self.cursor.execute('''
            UPDATE payments
            SET date = ?
            WHERE id = ?
        ''', (new_date, payment_id))
        self.connection.commit()

    def change_email(self, username, new_email):
        self.cursor.execute('''
            UPDATE users
            SET email = ?
            WHERE username = ?
        ''', (new_email, username))
        self.connection.commit()

    def change_password(self, username, new_password):
        self.cursor.execute('''
            UPDATE users
            SET password = ?
            WHERE username = ?
        ''', (new_password, username))
        self.connection.commit()
