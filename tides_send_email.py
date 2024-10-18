import smtplib, ssl
from email.message import EmailMessage


def send_email(message):
    host = "smtp.gmail.com"
    port = 465
    context = ssl.create_default_context()

    sender = "leobot1010@gmail.com"
    password = 'vuihokpyyfphutnc'
    receiver = 'kieran303@hotmail.com'
    # receiver = 'leobot1010@gmail.com'

    em = EmailMessage()
    em['From'] = sender
    em['To'] = receiver
    em['Subject'] = "Today's tides times for Rossbeigh"
    em.set_content(message)

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, em.as_string())

    print("Email was sent")