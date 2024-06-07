import ssl
from datetime import timedelta
from email.message import EmailMessage


class Payment:
    """

    Class Payment - a class representing a payment.
    Attributes:
    - amount: the amount of the payment
    - date: the date of the payment
    - how_often: how often the payment is made
    - title: the title of the payment
    - description: the description of the payment
    - payment_id: the id of the payment

    """
    def __init__(self, amount, date, how_often, title='Upcoming payment', description=None, payment_id=None):
        self.context = None
        self.body_msg = ''
        self.date = date
        self.amount = amount
        self.title = title
        self.how_often = how_often
        self.description = description
        self.payment_id = payment_id

    def add_payment(self, database):
        self.payment_id = database.add_payment(self)

    def __str__(self):
        return f"{self.amount} - {self.date} - {self.how_often} - {self.title}"
