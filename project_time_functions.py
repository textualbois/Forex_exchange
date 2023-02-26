import datetime
import pytz


def get_current_time():
    moscow_tz = pytz.timezone('Europe/Moscow')
    moscow_time = datetime.datetime.now(tz=moscow_tz)
    return moscow_time.timestamp()


