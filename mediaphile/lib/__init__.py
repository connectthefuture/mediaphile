from datetime import datetime
import time
import logging
import sys

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
        return "%s. Duration: %s ms." % (self.text, self.stop - self.start)

    @classmethod
    def enable(cls, value=True, stream=sys.stdout, level=logging.DEBUG):
        """

        """
        cls.enabled = value
        logging.basicConfig(stream=stream)
        logging.getLogger("PerformanceLogger").setLevel(level)

