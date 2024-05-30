from datetime import datetime


class Income:
    def __init__(self, amount, sender, date=None, income_id=None):
        self.amount = amount
        self.sender = sender
        self.date = date if date else datetime.now().date()
        self.income_id = income_id

    def add_income(self, database):
        print('add_income')
        self.income_id = database.add_income(self)

    def __str__(self):
        return f"{self.amount} - {self.sender} - {self.date}"
