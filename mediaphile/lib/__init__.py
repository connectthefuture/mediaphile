from datetime import datetime

months = {}
if not months:
    for month in range(1, 12 + 1):
        date = datetime(1900, month, 1)
        months[month] = date.strftime('%B')