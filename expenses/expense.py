from datetime import datetime


class Expense:
    def __init__(self, amount, category, payment_method, date=None, photo_path=None, expense_id=None):
        self.category = category
        self.amount = amount
        self.payment_method = payment_method
        self.date = date if date else datetime.now().date()
        self.photo_path = photo_path if photo_path else ''
        self.expense_id = expense_id

    def add_expense(self, database):
        print('add_expense')
        print('amount: ', self.amount)
        print('category: ', self.category)
        print('payment_method: ', self.payment_method)
        print('date: ', self.date)
        print('photo_path: ', self.photo_path)
        print('expense_id: ', self.expense_id)
        self.expense_id = database.add_expense(self)

    def __str__(self):
        return f"{self.amount} - {self.category} - {self.date} - {self.payment_method}"
