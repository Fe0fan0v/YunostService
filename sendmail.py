import smtplib, ssl
from env import email_login, email_password
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send(email: str, subject: str, course: str, group: str):
    text = f"""
<html>
  <body>
    <p>Ваша запись успешно зарегистрирована.</p>
    <p>Вы записались на {course} в группу {group}</p>
    <p>Ожидайте приглашения на родительское собрание (в конце августа) для оформления пакета документов:</p>
    <ul>
        <li>Заявление</li>
        <li>Согласие на фото и видеосъемку</li>
        <li>Копия свидетельства о рождении ребенка, либо копия паспорта ребенка (для детей старше 14)</li>
    </ul>
    <a href="http://priem.ddt-miass.ru/download/documents.zip"> Скачать образцы бланков документов </a>
    <p>*Расписание является предварительным, возможна корректировка</p>
    <p>С уважением,</p>
    <p>МАУ ДО "ДДТ "Юность" им.В.П.Макеева"</p>
    <p>наш телефон +73513532265</p>
    <p>наш сайт  <a href="http://ddt-miass.ru/">http://ddt-miass.ru/</a></p>
    <p>ВКонтакте <a href="https://vk.com/ddt_yunost">https://vk.com/ddt_yunost</a></p>
  </body>
</html>
"""
    address = email_login
    password = email_password
    html = MIMEText(text, "html")
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = address
    message["To"] = email
    message.attach(html)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.yandex.ru', 465, context=context) as server:
        server.login(address, password)
        try:
            server.sendmail(address, email, message.as_string())
        except:
            pass
