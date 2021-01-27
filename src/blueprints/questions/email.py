from flask_mail import Message, Mail
from flask import current_app
from threading import Thread

mail = Mail()

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body, session_id):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    with current_app.open_resource("output/pdf/"+session_id+".pdf") as fp:
        msg.attach('DataEnWatNu.pdf', 'application/pdf', fp.read())
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()