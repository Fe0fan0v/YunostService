import smtplib
from env import email_login, email_password
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send(email: str, subject: str):
    text = """
<html>
  <body>
    <p>Ваша запись успешно зарегистрирована.</p>
    <p>Ожидайте приглашения на родительское собрание (в конце августа) для оформления пакета документов:</p>
    <ul>
        <li>Заявление</li>
        <li>Согласие на фото и видеосъемку</li>
        <li>Копию свидетельства о рождении ребенка, либо копию паспорта ребенка (для детей старше 14)</li>
    </ul>
    <p>Образцы бланков документов - <a href="priem.ddt-miass.ru/download/documents.zip">скачать</a></p>
    <p>*Расписание является предварительным, возможна корректировка</p>
    <p>С уважением,</p>
    <p>МАУ ДО "ДДТ "Юность" им.В.П.Макеева"</p>
    <p>наш телефон +73513532265</p>
    <p>наш сайт  <a href="http://ddt-miass.ru/">http://ddt-miass.ru/</p>
    <p>ВКонтакте <a href="https://vk.com/ddt_yunost">https://vk.com/ddt_yunost</a></p>
  </body>
</html>
"""
    address = email_login
    password = email_password
    server = smtplib.SMTP('smtp.yandex.ru', 587)
    server.ehlo()   # Кстати, зачем это?
    server.starttls()
    server.login(address, password)
    html = MIMEText(text, "html")
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = address
    message["To"] = email
    message.attach(html)
    server.sendmail(address, email, html.as_string())
    server.quit()
