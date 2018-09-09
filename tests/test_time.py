#!/usr/bin/env python
import sciencedates as sd
import numpy.testing as npt
import datetime
import pytest


def test_findnearest():

    indf, xf = sd.find_nearest([10, 15, 12, 20, 14, 33], [32, 12.01])
    npt.assert_allclose(indf, [5, 2])
    npt.assert_allclose(xf, [33., 12.])

    indf, xf = sd.find_nearest((datetime.datetime(2012, 1, 1, 12),
                                datetime.datetime(2012, 1, 1, 11)),
                               datetime.datetime(2012, 1, 1, 11, 30))
    npt.assert_equal(indf, 0)
    npt.assert_equal(xf, datetime.datetime(2012, 1, 1, 12))


def test_randomdate():
    assert sd.randomdate(2018).year == 2018


if __name__ == '__main__':
    pytest.main([__file__])
