import typing as T
import datetime
import numpy as np
import dateutil.parser

from .dec import datetime2utsec

__all__ = ["datetime2yeardoy", "yeardoy2datetime", "date2doy", "datetime2gtd"]


def datetime2yeardoy(time: T.Union[str, datetime.datetime]) -> T.Tuple[int, float]:
    """
    Inputs:
    T: Numpy 1-D array of datetime.datetime OR string for dateutil.parser.parse

    Outputs:
    yd: yyyyddd four digit year, 3 digit day of year (INTEGER)
    utsec: seconds from midnight utc
    """
    time = np.atleast_1d(time)

    utsec = np.empty_like(time, float)
    yd = np.empty_like(time, int)
    for i, t in enumerate(time):
        if isinstance(t, np.datetime64):
            t = t.astype(datetime.datetime)
        elif isinstance(t, str):
            t = dateutil.parser.parse(t)

        utsec[i] = datetime2utsec(t)
        yd[i] = t.year * 1000 + int(t.strftime("%j"))

    return yd.squeeze()[()], utsec.squeeze()[()]


def yeardoy2datetime(yeardate: int, utsec: T.Union[float, int] = None) -> datetime.datetime:
    """

    Parameters
    ----------
    yd: yyyyddd four digit year, 3 digit day of year (INTEGER 7 digits)

    utsec: float, optional
        seconds since midnight

    Returns
    -------
    t: datetime.datetime
        datetime of yeardoy

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
        raise ValueError("yyyyddd expected")

    year = int(yd[:4])
    assert 0 < year < 3000, "year not in expected format"

    dt = datetime.datetime(year, 1, 1) + datetime.timedelta(days=int(yd[4:]) - 1)

    if utsec is not None:
        dt += datetime.timedelta(seconds=utsec)

    return dt


def date2doy(time: T.Union[str, datetime.datetime]) -> T.Tuple[int, int]:
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

    assert ((0 < doy) & (doy < 366)).all(), "day of year must be 0 < doy < 366"

    return doy, year


def datetime2gtd(time: T.Union[str, datetime.datetime, np.datetime64], glon: np.ndarray = np.nan) -> T.Tuple[int, float, float]:
    """

    Parameters
    ----------
    time: Numpy 1-D array of datetime.datetime OR string for dateutil.parser.parse
    glon: Numpy 2-D array of geodetic longitudes (degrees)

    Returns
    -------
    iyd: day of year
    utsec: seconds from midnight utc
    stl: local solar time
    """
    # %%
    T = np.atleast_1d(time)
    glon = np.asarray(glon)
    doy = np.empty_like(T, int)
    utsec = np.empty_like(T, float)
    stl = np.empty((T.size, *glon.shape))

    for i, t in enumerate(T):
        if isinstance(t, str):
            t = dateutil.parser.parse(t)
        elif isinstance(t, np.datetime64):
            t = t.astype(datetime.datetime)
        elif isinstance(t, (datetime.datetime, datetime.date)):
            pass
        else:
            raise TypeError("unknown time datatype {}".format(type(t)))
        # %% Day of year
        doy[i] = int(t.strftime("%j"))
        # %% seconds since utc midnight
        utsec[i] = datetime2utsec(t)

        stl[i, ...] = utsec[i] / 3600.0 + glon / 15.0

    return doy, utsec, stl
