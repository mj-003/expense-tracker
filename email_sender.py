import smtplib
import ssl
from email.message import EmailMessage
import os

from database import Database

# get email and password from environment variables
EMAIL_SENDER = os.environ['EMAIL_USER']
EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']


# create a database instance
db = Database()


def send_notifications():
    """

    Sends email notifications for upcoming payments and updates the payment dates.
    This function is dedicated to be run as a cron job.

    """

    # get upcoming payments
    upcoming_payments = db.get_upcoming_payments()

    # send email notifications
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
            print(f"Email sent to {payment['email']}")
        except smtplib.SMTPException as e:
            print(f"Failed to send email for {payment['email']}: {e}")

    # update payment dates
    for payment in upcoming_payments:
        db.update_payment_date(payment['id'], payment['how_often'])
