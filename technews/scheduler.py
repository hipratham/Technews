from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django.utils import timezone
from .views import generate_tech_news
import logging

logger = logging.getLogger(__name__)

def start():
    try:
        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")
        
        # Schedule job to run at 3 AM every day
        scheduler.add_job(
            generate_tech_news,
            'cron',
            hour=3,
            minute=0,
            name='generate_daily_news',
            replace_existing=True,
            misfire_grace_time=None  # Always run, even if misfired
        )
        
        scheduler.start()
        logger.info("Scheduler started. News will be generated daily at 3 AM.")
    except Exception as e:
        logger.error(f"Error starting scheduler: {str(e)}")
