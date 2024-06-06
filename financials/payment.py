import ssl
from datetime import timedelta
from email.message import EmailMessage

EMAIL_SENDER = 'juchiewicz.malwina@gmail.com'


class Payment:
    def __init__(self, amount, date, how_often, title='Upcoming payment', description=None):
        self.context = None
        self.body_msg = ''
        self.date = date
        self.amount = amount
        self.title = title
        self.how_often = how_often
        self.description = description



