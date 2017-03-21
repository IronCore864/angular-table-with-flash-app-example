from datetime import datetime

from settings import RUN_ON_PROD


def get_max_delayed_time_in_seconds(time):
    if not time:
        return 0 
    delay = int((datetime.now() - time).total_seconds())
    # local host on the laptop has a time difference of an hour than prod db
    if not RUN_ON_PROD:
        delay -= 3600
    return delay
