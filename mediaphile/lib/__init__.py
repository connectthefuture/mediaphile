from datetime import datetime

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