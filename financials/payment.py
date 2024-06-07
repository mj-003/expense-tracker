import ssl
from datetime import timedelta
from email.message import EmailMessage

EMAIL_SENDER = 'juchiewicz.malwina@gmail.com'


# Payment - a class representing a payment
class Payment:
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
