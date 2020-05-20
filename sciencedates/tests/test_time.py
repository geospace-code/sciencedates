#!/usr/bin/env python3
import datetime
import pytest
from pytest import approx

import sciencedates as sd


def test_findnearest():

    indf, xf = sd.find_nearest([10, 15, 12, 20, 14, 33], [32, 12.01])
    assert (indf == [5, 2]).all()
    assert xf == approx([33.0, 12.0])

    indf, xf = sd.find_nearest(
        (datetime.datetime(2012, 1, 1, 12), datetime.datetime(2012, 1, 1, 11)), datetime.datetime(2012, 1, 1, 11, 30)
    )
    assert indf == 0
    assert xf == datetime.datetime(2012, 1, 1, 12)


def test_randomdate():
    assert sd.randomdate(2018).year == 2018


if __name__ == "__main__":
    pytest.main([__file__])
