from schedule import every, repeat, run_pending
import time

from utilities import update_database


@repeat(every().day.at("00:00:00"))
def job():
    update_database()


while True:
    run_pending()
    time.sleep(600)
