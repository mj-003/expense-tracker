from datetime import datetime


class Expense:
    def __init__(self, category, amount, description, payment_method, date=None, image=None):
        self.category = category
        self.amount = amount
        self.description = description
        self.payment_method = payment_method
        self.date = date if date else datetime.now().date()
        self.image = image

    def __str__(self):
        return f"{self.amount} - {self.category} - {self.date} - {self.payment_method} - {self.description}"

