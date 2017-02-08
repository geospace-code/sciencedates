#!/usr/bin/env python
from datetime import datetime
from pytz import timezone, UTC
from numpy.testing import run_module_suite,assert_allclose,assert_almost_equal
#
import sciencedates as sd

def test_yearint():
    adatetime=datetime(2013,7,2,12,0,0,tzinfo=UTC)
    yd,utsec = sd.datetime2yd(adatetime)

    utsec2 = sd.dt2utsec(adatetime)

    assert sd.yd2datetime(yd,utsec) == adatetime
    assert utsec==utsec2

def test_yeardec():
    adatetime=datetime(2013,7,2,12,0,0,tzinfo=UTC)
    yeardec = sd.datetime2yeardec(adatetime)

    assert_allclose(yeardec,2013.5)
    assert sd.yeardec2datetime(yeardec) == adatetime

def test_utc():
    adatetime=datetime(2013,7,2,12,0,0)
    estdt = timezone('EST').localize(adatetime)
    utcdt = sd.forceutc(estdt)

    assert utcdt==estdt
    assert utcdt.tzname()=='UTC'

def test_gtd():
    adatetime=datetime(2013,7,2,12,0,0)
    iyd,utsec,stl= sd.datetime2gtd(adatetime,glon=42)

    assert iyd[0]==183
    assert_allclose(utsec[0],43200)
    assert_allclose(stl[0],14.8)
    
    
def test_findnearest():
    indf,xf = sd.find_nearest([10,15,12,20,14,33],[32,12.01])
    assert_almost_equal(indf,[5,2])
    assert_almost_equal(xf,[33.,12.])

if __name__ == '__main__':
    run_module_suite()
