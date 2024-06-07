from datetime import datetime


# Expense - a class representing an expense
class Expense:
    def __init__(self, amount, category, payment_method, date=None, photo_path=None, expense_id=None, description=None):
        self.category = category
        self.amount = amount
        self.payment_method = payment_method
        self.date = date if date else datetime.now().date()
        self.photo_path = photo_path if photo_path else ''
        self.expense_id = expense_id
        self.description = description

    def add_expense(self, database):
        self.expense_id = database.add_expense(self)

    def __str__(self):
        return f"{self.amount} - {self.category} - {self.date} - {self.payment_method}"
