from __future__ import division #needed for py2.7
from datetime import timedelta,datetime, time
from pytz import UTC
from numpy import atleast_1d, empty_like, atleast_2d,nan,empty,datetime64,ndarray,asarray
from dateutil.parser import parse

def datetime2yd(T):
    """
    Inputs:
    T: Numpy 1-D array of datetime.datetime OR string suitable for dateutil.parser.parse

    Outputs:
    yd: yyyyddd four digit year, 3 digit day of year (INTEGER)
    utsec: seconds from midnight utc
    """
    T = forceutc(T)
    T = atleast_1d(T)

    utsec=empty_like(T,dtype=float)
    yd = empty_like(T,dtype=int)
    for i,t in enumerate(T):
        utsec[i] = dt2utsec(t)
        yd[i] = t.year*1000 + int(t.strftime('%j'))

    return yd.squeeze()[()] , utsec.squeeze()[()]

def yd2datetime(yd,utsec=None):
    """
    Inputs:
    yd: yyyyddd four digit year, 3 digit day of year (INTEGER 7 digits)

    outputs:
    t: datetime

    http://stackoverflow.com/questions/2427555/python-question-year-and-day-of-year-to-date
    """
    yd = str(yd)
    assert len(yd)==7,'yyyyddd expected'

    year = int(yd[:4])
    assert 0 < year < 3000,'year not in expected format'

    dt = forceutc(datetime(year, 1, 1) + timedelta(days=int(yd[4:]) - 1))
    if utsec is not None:
        dt += timedelta(seconds=utsec)

    return dt


def datetime2gtd(T,glon=nan):
    """
    Inputs:
    T: Numpy 1-D array of datetime.datetime OR string suitable for dateutil.parser.parse
    glon: Numpy 2-D array of geodetic longitudes (degrees)

    Outputs:
    iyd: day of year
    utsec: seconds from midnight utc
    stl: local solar time
    """
    T = atleast_1d(T); glon=atleast_2d(glon)
    iyd=empty_like(T,dtype=int)
    utsec=empty_like(T,dtype=float)
    stl = empty((T.size,glon.shape[0],glon.shape[1]))

    for i,t in enumerate(T):
        t = forceutc(t)
        iyd[i] = int(t.strftime('%j'))
        #seconds since utc midnight
        utsec[i] = dt2utsec(t)

        stl[i,...] = utsec[i]/3600 + glon/15 #FIXME let's be sure this is appropriate

    return iyd,utsec,stl

#def dt2utsec(t: datetime) -> float:
def dt2utsec(t):
    """
    input: datetime
    output: float utc seconds since THIS DAY'S MIDNIGHT
    """
    t = forceutc(t)

    return timedelta.total_seconds(t-datetime.combine(t.date(),time(0,tzinfo=UTC)))


def forceutc(t):
    """
    Add UTC to datetime-naive and convert to UTC for datetime aware

    input: python datetime (naive, utc, non-utc) or Numpy datetime64  #FIXME add Pandas and AstroPy time classes
    output: utc datetime
    """
#%% polymorph to datetime
    if isinstance(t,str):
        t = parse(t)
    elif isinstance(t,datetime64):
        t=t.astype('M8[ms]').astype('O') #for Numpy 1.10 at least...
    elif isinstance(t,datetime):
        pass
    elif isinstance(t,(ndarray,list,tuple)):
        return asarray([forceutc(T) for T in t])
    else:
        raise TypeError('datetime only input')
#%% enforce UTC on datetime
    if t.tzinfo == None: #datetime-naive
        t = t.replace(tzinfo = UTC)
    else: #datetime-aware
        t = t.astimezone(UTC) #changes timezone, preserving absolute time. E.g. noon EST = 5PM UTC
    return t


"""
http://stackoverflow.com/questions/19305991/convert-fractional-years-to-a-real-date-in-python
Authored by "unutbu" http://stackoverflow.com/users/190597/unutbu

In Python, go from decimal year (YYYY.YYY) to datetime,
and from datetime to decimal year.
"""
def yeardec2datetime(atime):
    """
    Convert atime (a float) to DT.datetime
    This is the inverse of datetime2yeardec.
    assert dt2t(t2dt(atime)) == atime
    """
    if isinstance(atime,(float,int)): #typically a float

        year = int(atime)
        remainder = atime - year
        boy = datetime(year, 1, 1)
        eoy = datetime(year + 1, 1, 1)
        seconds = remainder * (eoy - boy).total_seconds()

        return forceutc(boy + timedelta(seconds=seconds))
    elif isinstance(atime[0],float):
        T = []
        for t in atime:
            T.append(yeardec2datetime(t))
        return T
    else:
        raise TypeError('expecting float, not {}'.format(type(atime)))

def datetime2yeardec(t):
    """
    Convert a datetime into a float. The integer part of the float should
    represent the year.
    Order should be preserved. If adate<bdate, then d2t(adate)<d2t(bdate)
    time distances should be preserved: If bdate-adate=ddate-cdate then
    dt2t(bdate)-dt2t(adate) = dt2t(ddate)-dt2t(cdate)
    """
    if isinstance(t,str):
        t = parse(t)

    t = forceutc(t)

    assert isinstance(t,datetime)

    year = t.year
    boy = datetime(year, 1, 1,tzinfo=UTC)
    eoy = datetime(year + 1, 1, 1, tzinfo=UTC)
    return year + ((t - boy).total_seconds() / ((eoy - boy).total_seconds()))
