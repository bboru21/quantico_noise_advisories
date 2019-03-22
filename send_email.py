import os
from simple_settings import settings

import smtplib
from email.mime.text import MIMEText

def send_email(message):
    if settings.SEND_EMAIL:
        msg = MIMEText(message)
        msg['Subject'] = 'Quantico Noise Advisories Script Error'
        msg['From'] = settings.SENDER_EMAIL
        msg['To'] = settings.RECIPIENT_EMAIL

        server = smtplib.SMTP_SSL(settings.SENDER_EMAIL_HOST, settings.SENDER_EMAIL_PORT)
        server.ehlo()
        server.login(settings.SENDER_EMAIL, settings.SENDER_PASSWORD)

        #Send the mail
        server.sendmail(settings.SENDER_EMAIL, settings.RECIPIENT_EMAIL, msg.as_string())
        server.quit()