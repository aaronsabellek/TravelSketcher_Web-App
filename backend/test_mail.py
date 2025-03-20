from app import app, mail
from flask import current_app
from flask_mail import Message

def send_email_test(to_email, subject, body):
    """ Sendet eine E-Mail unter Verwendung der Flask-App-Konfiguration """
    with app.app_context():
        sender_email = app.config['MAIL_DEFAULT_SENDER']

        msg = Message(subject, recipients=[to_email], body=body, sender=sender_email)
        mail.send(msg)

send_email_test('aaronsabellek@gmx.de', 'subject', 'body')

