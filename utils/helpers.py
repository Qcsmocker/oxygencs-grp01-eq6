from datetime import datetime
import pytz


def format_timestamp():
    eastern = pytz.timezone("America/Toronto")
    return datetime.now(eastern).strftime("%Y-%m-%d %H:%M:%S")
