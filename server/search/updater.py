from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)

    @scheduler.scheduled_job('cron', day_of_week='mon-sun', minute=5, id='search-ranking')
    def auto_update():
        from .viewsets.search import search_rank
        search_rank()

    scheduler.start()
