from datetime import datetime
import time
import logging
import sys
from datetime import datetime
import dateutil.relativedelta

get_term_mapping = {
    'NIKON CORPORATION': 'Nikon',
    'NIKON': 'Nikon',
}

def sizeof_fmt(num):
    """
    Returns a human readably format for filesize.
    """
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if 1024.0 > num > -1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')


months = {}
if not months:
    for month in range(1, 12 + 1):
        date = datetime(1900, month, 1)
        months[month] = date.strftime('%B')


#!/usr/bin/env python

INTERVALS = [1, 60, 3600, 86400, 604800, 2419200, 29030400]
NAMES = [
    ('second', 'seconds'),
    ('minute', 'minutes'),
    ('hour',   'hours'),
    ('day',    'days'),
    ('week',   'weeks'),
    ('month',  'months'),
    ('year',   'years')]


def humanize_time(amount, units):
    """
    Credits: https://github.com/liudmil-mitev/experiments/blob/master/time/humanize_time.py
    Divide `amount` in time periods.
    Useful for making time intervals more human readable.

    >>> humanize_time(173, "hours")
    [(1, 'week'), (5, 'hours')]
    >>> humanize_time(17313, "seconds")
    [(4, 'hours'), (48, 'minutes'), (33, 'seconds')]
    >>> humanize_time(90, "weeks")
    [(1, 'year'), (10, 'months'), (2, 'weeks')]
    >>> humanize_time(42, "months")
    [(3, 'years'), (6, 'months')]
    >>> humanize_time(500, "days")
    [(1, 'year'), (5, 'months'), (3, 'weeks'), (3, 'days')]
    """
    result = []

    unit = map(lambda a: a[1], NAMES).index(units)
    # Convert to seconds
    amount = amount * INTERVALS[unit]

    for i in range(len(NAMES)-1, -1, -1):
        a = amount // INTERVALS[i]
        if a > 0:
            result.append( (a, NAMES[i][1 % a]) )
            amount -= a * INTERVALS[i]

    return result


class PerformanceLogger:
    """

    """
    enabled = False

    def __init__(self, text):
        """

        """
        self.text = text
        self.start = None
        self.stop = None
        self.logger = logging.getLogger("PerformanceLogger")

    def __enter__(self):
        """

        """
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """

        """
        self.stop = time.time()
        if PerformanceLogger.enabled:
            self.logger.debug(str(self))

        return True

    def __str__(self):
        """

        """
        duration = []

        dt1 = datetime.fromtimestamp(self.start)
        dt2 = datetime.fromtimestamp(self.stop)
        rd = dateutil.relativedelta.relativedelta(dt2, dt1)
        if rd.days > 0:
            duration.append('%s days' % rd.days)
        if rd.hours > 0:
            duration.append('%s hours' % rd.hours)
        if rd.minutes > 0:
            duration.append('%s minutes' % rd.minutes)
        if rd.seconds > 0:
            duration.append("%s seconds" % rd.seconds)
        if rd.microseconds > 0:
            duration.append('%s microseconds' % rd.microseconds)

        return "%s. Duration: %s." % (self.text, ', '.join(duration))

    @classmethod
    def enable(cls, value=True, stream=sys.stdout, level=logging.DEBUG):
        """

        """
        cls.enabled = value
        logging.basicConfig(stream=stream)
        logging.getLogger("PerformanceLogger").setLevel(level)

