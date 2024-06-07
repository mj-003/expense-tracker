from datetime import datetime


# Income - a class representing an income
class Income:
    def __init__(self, amount, sender, date=None, income_id=None, description=None):
        self.amount = amount
        self.sender = sender
        self.date = date if date else datetime.now().date()
        self.income_id = income_id
        self.description = description

    def add_income(self, database):
        self.income_id = database.add_income(self)

    def __str__(self):
        return f"{self.amount} - {self.sender} - {self.date}"
