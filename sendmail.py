import smtplib


def send(email, text):
    smtpObj = smtplib.SMTP('smtp.yandex.ru', 465)
    smtpObj.starttls()
    smtpObj.login('ddt-miass@yandex.ru', 'Vfu,jhjnv,hf')
    smtpObj.sendmail('ddt-miass@yandex.ru', email, text)
