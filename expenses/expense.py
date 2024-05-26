from datetime import datetime


class Expense:
    def __init__(self, category, amount, description, date=None):
        self.category = category
        self.amount = amount
        self.description = description
        self.date = date if date else datetime.now().date()

