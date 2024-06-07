from datetime import datetime


class Income:
    """

    Class Income - a class representing an income.

    Attributes:
    - amount: the amount of the income
    - sender: the sender of the income
    - date: the date of the income
    - description: the description of the income
    - income_id: the id of the income

    """
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
