import smtplib
import ssl
from datetime import datetime, timedelta
from email.message import EmailMessage

EMAIL_SENDER = 'juchiewicz.malwina@gmail.com'
EMAIL_PASSWORD = 'zftw elox vfxy snbg'


class EmailSender:
    def __init__(self, email_receiver, subject, body, send_date, how_often):
        self.email_receiver = email_receiver
        self.subject = subject
        self.body = body
        self.send_date = send_date
        self.how_often = how_often

        self.em = EmailMessage()
        self.em['From'] = EMAIL_SENDER
        self.em['To'] = self.email_receiver
        self.em['Subject'] = self.subject
        self.em.set_content(body)
        self.context = ssl.create_default_context()

        self.set_send_date()

    def set_send_date(self):
        if self.how_often == 'single one':
            self.send_date = self.send_date - timedelta(days=3)
        elif self.how_often == 'every month':
            # Ustawienie daty wysyłki na 3 dni przed każdym miesiącem
            self.send_date = self.send_date.replace(day=self.send_date.day, month=1,
                                                    year=self.send_date.year) - timedelta(days=3)
        else:
            raise ValueError(
                "Nieprawidłowa wartość dla how_often. Dopuszczalne wartości to 'single one' i 'every month'.")

    def send_email(self):
        if datetime.now() >= self.send_date:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=self.context) as smtp:
                smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
                smtp.sendmail(EMAIL_SENDER, self.email_receiver, self.em.as_string())
        else:
            print(
                f"Nie wysyłam emaila, bo aktualna data ({datetime.now()}) jest wcześniejsza niż data wysyłki ({self.send_date}).")


# Przykład użycia
send_date = datetime(2023, 4, 1)  # Ustawienie daty wysyłki na 1 kwietnia 2023
email_sender = EmailSender('juchiewicz.malwina@gmail.com', 'test', 'test', send_date, 'every month')
email_sender.send_email()
