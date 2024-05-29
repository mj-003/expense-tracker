from datetime import datetime


class Expense:
    def __init__(self, amount, category, description, payment_method, date=None, image=None, expense_id=None):
        self.category = category
        self.amount = amount
        self.description = description
        self.payment_method = payment_method
        self.date = date if date else datetime.now().date()
        self.image = image
        self.expense_id = expense_id

    def add_expense(self, database):
        print('add_expense')
        self.expense_id = database.add_expense(self)

    def __str__(self):
        return f"{self.amount} - {self.category} - {self.date} - {self.payment_method} - {self.description}"