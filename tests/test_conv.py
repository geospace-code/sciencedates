#!/usr/bin/env python
import datetime
from dateutil.parser import parse
import numpy as np
from numpy.testing import assert_allclose, assert_equal
import pytest
import sciencedates as sd
import sys
#
T = [datetime.datetime(2013, 7, 2, 12, 0, 0)]
T.append(T[0].date())
T.append(np.datetime64(T[0]))
T.append(str(T[0]))

Tdt = (T[0],)*3
OLDPY = sys.version_info < (3, 6)


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


@pytest.mark.xfail(OLDPY, reason='py36+')
def test_utc():
    pytz = pytest.importorskip('pytz')

    estdt = T[0].astimezone(pytz.timezone('EST'))
    utcdt = sd.forceutc(estdt)

    assert utcdt == estdt
    assert utcdt.tzname() == 'UTC'

    d = T[0].date()
    assert sd.forceutc(d) == d


if __name__ == '__main__':
    pytest.main([__file__])

if __name__ == '__main__':
    pytest.main()
