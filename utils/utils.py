from datetime import datetime
import pytz


def get_now_time():
    now = datetime.now(pytz.timezone('Europe/Bratislava'))
    return now.replace(tzinfo=None)


def get_refer_id(command_args):
    try:
        return int(command_args)
    except (TypeError, ValueError):
        return None