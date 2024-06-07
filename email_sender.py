import smtplib
import ssl
from email.message import EmailMessage
import os

from database import Database
EMAIL_SENDER = os.environ['EMAIL_USER']
EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']


db = Database()


def send_notifications():
    upcoming_payments = db.get_upcoming_payments()
    for payment in upcoming_payments:
        msg = EmailMessage()
        msg['From'] = EMAIL_SENDER
        msg['To'] = payment['email']
        msg['Subject'] = f'Upcoming payment reminder: {payment["title"]}'
        msg.set_content(
            f'Hello {payment["username"]}, you have an upcoming payment of {payment["amount"]} due on {payment["date"]}.')

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context()) as smtp:
                smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
                smtp.send_message(msg)
                db.update_payment_date(payment['id'], payment['how_often'])
            print(f"Email sent to {payment['email']}")
        except smtplib.SMTPException as e:
            print(f"Failed to send email for {payment['email']}: {e}")

    for payment in upcoming_payments:
        db.update_payment_date(payment['id'], payment['how_often'])
