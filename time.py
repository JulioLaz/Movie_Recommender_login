import datetime
import pytz

def get_current_time():
    return datetime.datetime.now(pytz.timezone('US/Eastern')).strftime("%H:%M:%S")
