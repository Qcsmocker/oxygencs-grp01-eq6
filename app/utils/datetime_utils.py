"""
Utility functions for handling date and time operations.
"""

from datetime import datetime

import pytz


def get_current_timestamp():
    """Return the current timestamp formatted as a string."""
    eastern = pytz.timezone("America/Toronto")
    return datetime.now(eastern).strftime("%Y-%m-%d %H:%M:%S")
