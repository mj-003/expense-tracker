from datetime import datetime


class Expense:
    """

    Class Expense - a class representing an expense.

    Attributes:
    - amount: the amount of the expense
    - category: the category of the expense
    - payment_method: the payment method of the expense
    - date: the date of the expense
    - photo_path: the path of the photo of the expense
    - description: the description of the expense
    - expense_id: the id of the expense

    """
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
