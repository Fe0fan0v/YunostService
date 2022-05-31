import smtplib
from env import email_login, email_password


def send(email: str, subject: str, text: str):
    address = email_login
    password = email_password
    server = smtplib.SMTP('smtp.yandex.ru', 587)
    server.ehlo()   # Кстати, зачем это?
    server.starttls()
    server.login(address, password)
    message = f'From: {address}\nTo: {email}\nSubject: {subject}\n\n{text}'
    server.sendmail(address, email, message.encode('utf-8'))
    server.quit()
