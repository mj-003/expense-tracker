import ssl
from datetime import timedelta
from email.message import EmailMessage
EMAIL_SENDER = 'juchiewicz.malwina@gmail.com'

class Payment:
    def __init__(self, amount, date, how_often, title='Upcoming payment'):
        self.context = None
        self.date = date
        self.amount = amount
        self.title = title
        self.body_msg = 'You have an upcoming payment of ' + str(self.amount) + ' on ' + str(self.date) + ' for ' + self.title
        self.how_often = how_often

        self.em = EmailMessage()

        self.create_email_message()
        self.set_send_date()

    def set_send_date(self):
        if self.how_often == 'single one':
            self.send_date = self.send_date - timedelta(days=3)
        elif self.how_often == 'every month':
            self.send_date = self.send_date.replace(day=self.send_date.day, month=1,
                                                    year=self.send_date.year) - timedelta(days=3)

    def create_email_message(self):
        self.em['From'] = EMAIL_SENDER
        self.em['To'] = 'juchiewicz.malwina@gmail.com'
        self.em['Subject'] = 'Upcoming payment for ' + self.title
        self.em.set_content(self.body_msg)
        self.context = ssl.create_default_context()
        self.em.set_content(self.body_msg)