import typing as T
import numpy as np
import datetime
import dateutil.parser

__all__ = ["datetime2utsec", "datetime2yeardec", "yeardec2datetime"]


def datetime2utsec(t: T.Union[str, datetime.date, datetime.datetime, np.datetime64]) -> float:
    """
    input: datetime
    output: float utc seconds since THIS DAY'S MIDNIGHT
    """
    if isinstance(t, (tuple, list, np.ndarray)):
        return np.asarray([datetime2utsec(T) for T in t])
    elif isinstance(t, datetime.date) and not isinstance(t, datetime.datetime):
        return 0.0
    elif isinstance(t, np.datetime64):
        t = t.astype(datetime.datetime)
    elif isinstance(t, str):
        t = dateutil.parser.parse(t)

    return datetime.timedelta.total_seconds(t - datetime.datetime.combine(t.date(), datetime.datetime.min.time()))


def yeardec2datetime(atime: float) -> datetime.datetime:
    """
    Convert atime (a float) to DT.datetime
    This is the inverse of datetime2yeardec.
    assert dt2t(t2dt(atime)) == atime

    http://stackoverflow.com/questions/19305991/convert-fractional-years-to-a-real-date-in-python
    Authored by "unutbu" http://stackoverflow.com/users/190597/unutbu

    In Python, go from decimal year (YYYY.YYY) to datetime,
    and from datetime to decimal year.
    """
    # %%
    if isinstance(atime, (float, int)):  # typically a float

        year = int(atime)
        remainder = atime - year
        boy = datetime.datetime(year, 1, 1)
        eoy = datetime.datetime(year + 1, 1, 1)
        seconds = remainder * (eoy - boy).total_seconds()

        time = boy + datetime.timedelta(seconds=seconds)
        assert isinstance(time, datetime.datetime)
    elif isinstance(atime[0], float):
        return np.asarray([yeardec2datetime(t) for t in atime])
    else:
        raise TypeError("expecting float, not {}".format(type(atime)))

    return time


def datetime2yeardec(time: T.Union[str, datetime.datetime, datetime.date]) -> float:
    """
    Convert a datetime into a float. The integer part of the float should
    represent the year.
    Order should be preserved. If adate<bdate, then d2t(adate)<d2t(bdate)
    time distances should be preserved: If bdate-adate=ddate-cdate then
    dt2t(bdate)-dt2t(adate) = dt2t(ddate)-dt2t(cdate)
    """
    if isinstance(time, str):
        t = dateutil.parser.parse(time)
    elif isinstance(time, datetime.datetime):
        t = time
    elif isinstance(time, datetime.date):
        t = datetime.datetime.combine(time, datetime.datetime.min.time())
    elif isinstance(time, (tuple, list, np.ndarray)):
        return np.asarray([datetime2yeardec(t) for t in time])
    else:
        raise TypeError("unknown input type {}".format(type(time)))

    year = t.year

    boy = datetime.datetime(year, 1, 1)
    eoy = datetime.datetime(year + 1, 1, 1)

    return year + ((t - boy).total_seconds() / ((eoy - boy).total_seconds()))
