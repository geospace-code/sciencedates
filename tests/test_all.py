#!/usr/bin/env python
import datetime
from dateutil.parser import parse
import numpy as np
from pytz import timezone
from numpy.testing import assert_allclose, assert_equal, run_module_suite
#
import sciencedates as sd
#
T = [datetime.datetime(2013, 7, 2, 12, 0, 0)]
T.append(T[0].date())
T.append(np.datetime64(T[0]))
T.append(str(T[0]))

Tdt = (T[0],)*3


def test_yearint():

    for t in T:
        yd, utsec = sd.datetime2yeardoy(t)

        utsec2 = sd.datetime2utsec(t)

        if isinstance(t, datetime.datetime):
            assert sd.yeardoy2datetime(yd, utsec) == t
        elif isinstance(t, np.datetime64):
            assert sd.yeardoy2datetime(yd, utsec) == t.astype(datetime.datetime)
        elif isinstance(t, str):
            assert sd.yeardoy2datetime(yd, utsec) == parse(t)
        else:
            assert sd.yeardoy2datetime(yd, utsec).date() == t

        assert utsec == utsec2
# %% array
    y, s = sd.datetime2yeardoy(Tdt)
    assert_equal(sd.yeardoy2datetime(y, s), T[0])


def test_date2doy():
    for t in T:
        doy, year = sd.date2doy(t)

        assert year == T[0].year
        assert doy == 183
# %% array
    doy, year = sd.date2doy(Tdt)
    assert_equal(year, T[0].year)
    assert_equal(doy, 183)


def test_yeardec():
    for t, r in zip(T, (2013.5, 2013.4986301369863)):
        yeardec = sd.datetime2yeardec(t)

        assert_allclose(yeardec, r)
        if isinstance(t, datetime.datetime):
            assert sd.yeardec2datetime(yeardec) == t
        else:
            assert sd.yeardec2datetime(yeardec).date() == t
# %% array
    assert_equal(sd.yeardec2datetime(sd.datetime2yeardec(Tdt)), T[0])


def test_utc():
    estdt = T[0].astimezone(timezone('EST'))
    utcdt = sd.forceutc(estdt)

    assert utcdt == estdt
    assert utcdt.tzname() == 'UTC'

    d = T[0].date()
    assert sd.forceutc(d) == d


def test_gtd():

    iyd, utsec, stl = sd.datetime2gtd(T, glon=42)

    assert_allclose(iyd, 183)
    assert_allclose(utsec, (43200, 0, 43200, 43200))
    assert_allclose(stl, (14.8, 2.8, 14.8, 14.8))


def test_findnearest():

    indf, xf = sd.find_nearest([10, 15, 12, 20, 14, 33], [32, 12.01])
    assert_allclose(indf, [5, 2])
    assert_allclose(xf, [33., 12.])

    indf, xf = sd.find_nearest((datetime.datetime(2012, 1, 1, 12),
                               datetime.datetime(2012, 1, 1, 11)),
                               datetime.datetime(2012, 1, 1, 11, 30))
    assert_equal(indf, 0)
    assert_equal(xf, datetime.datetime(2012, 1, 1, 12))


def test_randomdate():
    assert sd.randomdate(2018).year == 2018


if __name__ == '__main__':
    run_module_suite()
