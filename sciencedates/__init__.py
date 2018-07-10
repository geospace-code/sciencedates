from __future__ import division
import datetime
from pytz import UTC
import numpy as np
from dateutil.parser import parse
import calendar
import random
from typing import Union, Tuple, Any


def datetime2yeardoy(time: Union[str, datetime.datetime]) -> Tuple[int, float]:
    """
    Inputs:
    T: Numpy 1-D array of datetime.datetime OR string for dateutil.parser.parse

    Outputs:
    yd: yyyyddd four digit year, 3 digit day of year (INTEGER)
    utsec: seconds from midnight utc
    """
    T: np.ndarray = np.atleast_1d(time)

    utsec = np.empty_like(T, float)
    yd = np.empty_like(T, int)
    for i, t in enumerate(T):
        if isinstance(t, np.datetime64):
            t = t.astype(datetime.datetime)
        elif isinstance(t, str):
            t = parse(t)

        utsec[i] = datetime2utsec(t)
        yd[i] = t.year*1000 + int(t.strftime('%j'))

    return yd.squeeze()[()], utsec.squeeze()[()]


def yeardoy2datetime(yeardate: int,
                     utsec: Union[float, int]=None) -> datetime.datetime:
    """
    Inputs:
    yd: yyyyddd four digit year, 3 digit day of year (INTEGER 7 digits)

    outputs:
    t: datetime

    http://stackoverflow.com/questions/2427555/python-question-year-and-day-of-year-to-date
    """
    if isinstance(yeardate, (tuple, list, np.ndarray)):
        if utsec is None:
            return np.asarray([yeardoy2datetime(y) for y in yeardate])
        elif isinstance(utsec, (tuple, list, np.ndarray)):
            return np.asarray([yeardoy2datetime(y, s) for y, s in zip(yeardate, utsec)])

    yeardate = int(yeardate)

    yd = str(yeardate)
    if len(yd) != 7:
        raise ValueError('yyyyddd expected')

    year = int(yd[:4])
    assert 0 < year < 3000, 'year not in expected format'

    dt = datetime.datetime(year, 1, 1) + datetime.timedelta(days=int(yd[4:]) - 1)
    assert isinstance(dt, datetime.datetime)

    if utsec is not None:
        dt += datetime.timedelta(seconds=utsec)

    return dt


def date2doy(time: Union[str, datetime.datetime]) -> Tuple[int, int]:
    """
    < 366 for leap year too. normal year 0..364.  Leap 0..365.
    """

    T = np.atleast_1d(time)

    year = np.empty(T.size, dtype=int)
    doy = np.empty_like(year)

    for i, t in enumerate(T):
        yd = str(datetime2yeardoy(t)[0])

        year[i] = int(yd[:4])
        doy[i] = int(yd[4:])

    assert ((0 < doy) & (doy < 366)).all(), 'day of year must be 0 < doy < 366'

    return doy, year


def datetime2gtd(time: Union[str, datetime.datetime],
                 glon: float=np.nan) -> Tuple[int, float, float]:
    """
    Inputs:
    time: Numpy 1-D array of datetime.datetime OR string for dateutil.parser.parse
    glon: Numpy 2-D array of geodetic longitudes (degrees)

    Outputs:
    iyd: day of year
    utsec: seconds from midnight utc
    stl: local solar time
    """
# %%
    T = np.atleast_1d(time)
    lon = np.atleast_2d(glon)
    iyd = np.empty_like(T, int)
    utsec = np.empty_like(T, float)
    stl = np.empty((T.size, lon.shape[0], lon.shape[1]))

    for i, t in enumerate(T):
        if isinstance(t, str):
            t = parse(t)
        elif isinstance(t, np.datetime64):
            t = t.astype(datetime.datetime)

        iyd[i] = int(t.strftime('%j'))
        # seconds since utc midnight
        utsec[i] = datetime2utsec(t)

        # FIXME let's be sure this is appropriate
        stl[i, ...] = utsec[i] / 3600 + lon / 15

    return iyd, utsec, stl.squeeze()


def datetime2utsec(t: Union[str, datetime.date, datetime.datetime, np.datetime64]) -> float:
    """
    input: datetime
    output: float utc seconds since THIS DAY'S MIDNIGHT
    """
    if isinstance(t, (tuple, list, np.ndarray)):
        return np.asarray([datetime2utsec(T) for T in t])
    elif isinstance(t, datetime.date) and not isinstance(t, datetime.datetime):
        return 0.
    elif isinstance(t, np.datetime64):
        t = t.astype(datetime.datetime)
    elif isinstance(t, str):
        t = parse(t)

    return datetime.timedelta.total_seconds(t - datetime.datetime.combine(t.date(),
                                                                          datetime.datetime.min.time()))


def forceutc(t: Union[str, datetime.datetime, datetime.date, np.datetime64]) -> Union[datetime.datetime, datetime.date]:
    """
    Add UTC to datetime-naive and convert to UTC for datetime aware

    input: python datetime (naive, utc, non-utc) or Numpy datetime64  #FIXME add Pandas and AstroPy time classes
    output: utc datetime
    """
    # need to passthrough None for simpler external logic.
# %% polymorph to datetime
    if isinstance(t, str):
        t = parse(t)
    elif isinstance(t, np.datetime64):
        t = t.astype(datetime.datetime)
    elif isinstance(t, datetime.datetime):
        pass
    elif isinstance(t, datetime.date):
        return t
    elif isinstance(t, (np.ndarray, list, tuple)):
        return np.asarray([forceutc(T) for T in t])
    else:
        raise TypeError('datetime only input')
# %% enforce UTC on datetime
    if t.tzinfo is None:  # datetime-naive
        t = t.replace(tzinfo=UTC)
    else:  # datetime-aware
        t = t.astimezone(UTC)  # changes timezone, preserving absolute time. E.g. noon EST = 5PM UTC

    return t


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

        T = boy + datetime.timedelta(seconds=seconds)
        assert isinstance(T, datetime.datetime)
    elif isinstance(atime[0], float):
        return np.asarray([yeardec2datetime(t) for t in atime])
    else:
        raise TypeError('expecting float, not {}'.format(type(atime)))

    return T


def datetime2yeardec(time: Union[str, datetime.datetime, datetime.date]) -> float:
    """
    Convert a datetime into a float. The integer part of the float should
    represent the year.
    Order should be preserved. If adate<bdate, then d2t(adate)<d2t(bdate)
    time distances should be preserved: If bdate-adate=ddate-cdate then
    dt2t(bdate)-dt2t(adate) = dt2t(ddate)-dt2t(cdate)
    """
    if isinstance(time, str):
        t = parse(time)
    elif isinstance(time, datetime.datetime):
        t = time
    elif isinstance(time, datetime.date):
        t = datetime.datetime.combine(time, datetime.datetime.min.time())
    elif isinstance(time, (tuple, list, np.ndarray)):
        return np.asarray([datetime2yeardec(t) for t in time])
    else:
        raise TypeError(f'unknown input type {type(time)}')

    year = t.year

    boy = datetime.datetime(year, 1, 1)
    eoy = datetime.datetime(year + 1, 1, 1)

    return year + ((t - boy).total_seconds() / ((eoy - boy).total_seconds()))


# %%
def find_nearest(x, x0) -> Tuple[int, Any]:
    """
    This find_nearest function does NOT assume sorted input

    inputs:
    x: array (float, int, datetime, h5py.Dataset) within which to search for x0
    x0: singleton or array of values to search for in x

    outputs:
    idx: index of flattened x nearest to x0  (i.e. works with higher than 1-D arrays also)
    xidx: x[idx]

    Observe how bisect.bisect() gives the incorrect result!

    idea based on:
    http://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array

    """
    x = np.asanyarray(x)  # for indexing upon return
    x0 = np.atleast_1d(x0)
# %%
    if x.size == 0 or x0.size == 0:
        raise ValueError('empty input(s)')

    if x0.ndim not in (0, 1):
        raise ValueError('2-D x0 not handled yet')
# %%
    ind = np.empty_like(x0, dtype=int)

    # NOTE: not trapping IndexError (all-nan) becaues returning None can surprise with slice indexing
    for i, xi in enumerate(x0):
        if xi is not None and (isinstance(xi, (datetime.datetime, datetime.date, np.datetime64)) or np.isfinite(xi)):
            ind[i] = np.nanargmin(abs(x-xi))
        else:
            raise ValueError('x0 must NOT be None or NaN to avoid surprising None return value')

    return ind.squeeze()[()], x[ind].squeeze()[()]   # [()] to pop scalar from 0d array while being OK with ndim>0


def randomdate(year: int) -> datetime.date:
    """ gives random date in year"""
    if calendar.isleap(year):
        doy = random.randrange(366)
    else:
        doy = random.randrange(365)

    return datetime.date(year, 1, 1) + datetime.timedelta(days=doy)
