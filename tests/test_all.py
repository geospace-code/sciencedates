#!/usr/bin/env python
import datetime
from pytz import timezone, UTC
from numpy.testing import assert_allclose,assert_equal,run_module_suite
#
import sciencedates as sd
#
T = [datetime.datetime(2013,7,2,12,0,0,tzinfo=UTC)]
T.append(T[0].date())

def test_yearint():

    for t in T:
        yd,utsec = sd.datetime2yd(t)

        utsec2 = sd.dt2utsec(t)

        if isinstance(t,datetime.datetime):
            assert sd.yd2datetime(yd,utsec) == t
        else:
            assert sd.yd2datetime(yd,utsec).date() == t

        assert utsec==utsec2

def test_date2doy():
    for t in T:
        doy,year = sd.date2doy(t)

        assert year == t.year
        assert doy == 183

def test_yeardec():
    for t,r in zip(T,(2013.5,2013.4986301369863)):
        yeardec = sd.datetime2yeardec(t)

        assert_allclose(yeardec, r)
        if isinstance(t,datetime.datetime):
            assert sd.yeardec2datetime(yeardec) == t
        else:
            assert sd.yeardec2datetime(yeardec).date() == t

def test_utc():

    estdt = T[0].astimezone(timezone('EST'))
    utcdt = sd.forceutc(estdt)

    assert utcdt==estdt
    assert utcdt.tzname()=='UTC'

    d = T[0].date()
    assert sd.forceutc(d) == d

def test_gtd():

    iyd,utsec,stl = sd.datetime2gtd(T, glon=42)

    assert_allclose(iyd,183)
    assert_allclose(utsec,(43200,0))
    assert_allclose(stl, (14.8, 2.8))


def test_findnearest():

    indf,xf = sd.find_nearest([10,15,12,20,14,33],[32,12.01])
    assert_allclose(indf,[5,2])
    assert_allclose(xf,[33.,12.])

    indf,xf = sd.find_nearest((datetime.datetime(2012,1,1,12),
                               datetime.datetime(2012,1,1,11)),
                               datetime.datetime(2012,1,1,11,30))
    assert_equal(indf,0)
    assert_equal(xf, datetime.datetime(2012,1,1,12))

def test_randomdate():
    assert sd.randomdate(2018).year == 2018


if __name__ == '__main__':
    run_module_suite()
