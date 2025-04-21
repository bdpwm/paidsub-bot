from create_bot import scheduler
from db_handlers.db_subscription import daily_check_subscriptions

def start_scheduler():
    scheduler.add_job(daily_check_subscriptions, 'cron', hour=0, minute=0)
    scheduler.start()