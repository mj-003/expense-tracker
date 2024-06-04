import smtplib
import ssl
from datetime import datetime, timedelta
from email.message import EmailMessage
from financials.payment import Payment

EMAIL_SENDER = 'juchiewicz.malwina@gmail.com'
EMAIL_PASSWORD = 'zftw elox vfxy snbg'


class UserPayments:
    def __init__(self):
        self.payments = []

    def add_payment(self, payment):
        self.payments.append(payment)

    def send_notifications(self):
        for payment in self.payments:
            if datetime.now() >= payment.send_date:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context()) as smtp:
                    smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
                    smtp.send_message(payment.em)