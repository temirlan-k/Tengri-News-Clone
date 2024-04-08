from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.jobstores.base import JobLookupError

from news_service.parser import parse_and_save_news_wrapper


def parse_news_job():
    try:
        parse_and_save_news_wrapper()
        print("News Parsed successfully")
    except Exception as e:
        print(f"Parsing Error: {e}")


def setup_scheduler():
    scheduler = BackgroundScheduler()

    try:
        scheduler.add_job(
            parse_news_job,
            trigger=IntervalTrigger(minutes=5),
            id="parse_news_job",
            name="Parse and save news every 5 minutes",
            replace_existing=True,
        )
        scheduler.start()
        print("Scheduler running")
    except JobLookupError:
        print("Job with id already exist")
    except Exception as e:
        print(f"Scheduler running failed : {e}")


setup_scheduler()
