import calendar
import random
import datetime


def randomdate(year: int) -> datetime.date:
    """ gives random date in year"""
    if calendar.isleap(year):
        doy = random.randrange(366)
    else:
        doy = random.randrange(365)

    return datetime.date(year, 1, 1) + datetime.timedelta(days=doy)
