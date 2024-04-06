import schedule
import time
from news_service.parser import parse_and_save_news

def schedule_parser():
    schedule.every().day.at("02:50").do(parse_and_save_news)

    while True:
        schedule.run_pending()
        time.sleep(1)
