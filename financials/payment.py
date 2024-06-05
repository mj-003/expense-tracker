import ssl
from datetime import timedelta
from email.message import EmailMessage

EMAIL_SENDER = 'juchiewicz.malwina@gmail.com'


class Payment:
    def __init__(self, amount, date, how_often, title='Upcoming payment'):
        self.context = None
        self.body_msg = ''
        self.date = date
        self.amount = amount
        self.title = title
        self.how_often = how_often
        self.set_send_date()


    def set_send_date(self): # daily, weeksly, monthly, yearly, single
        if self.how_often == 'single':
            self.send_date = self.send_date - timedelta(days=3)
        elif self.how_often == 'every month':
            self.send_date = self.send_date.replace(day=self.send_date.day, month=1,
                                                    year=self.send_date.year) - timedelta(days=3)


