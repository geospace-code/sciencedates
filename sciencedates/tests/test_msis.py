#!/usr/bin/env python
"""
tests for time conversions relevant to MSISE00
"""
import numpy as np
import datetime
import pytest
from pytest import approx
import typing

import sciencedates as sd

T: typing.List[typing.Any] = [datetime.datetime(2013, 7, 2, 12, 0, 0)]
T.append(T[0].date())
T.append(np.datetime64(T[0]))
T.append(str(T[0]))


def test_str():
    t = T[3]
    assert isinstance(t, str)

    iyd, utsec, stl = sd.datetime2gtd(t, glon=42)

    assert iyd == 183
    assert utsec == 43200
    assert stl == approx(14.8)


def test_dt64():
    t = T[2]
    assert isinstance(t, np.datetime64)

    iyd, utsec, stl = sd.datetime2gtd(t, glon=42)

    assert iyd == 183
    assert utsec == 43200
    assert stl == approx(14.8)


def test_date():
    t = T[1]
    assert isinstance(t, datetime.date)

    iyd, utsec, stl = sd.datetime2gtd(t, glon=42)

    assert iyd == 183
    assert utsec == 0
    assert stl == approx(2.8)


def test_datetime():
    t = T[0]
    assert isinstance(t, datetime.datetime)

    iyd, utsec, stl = sd.datetime2gtd(t, glon=42)

    assert iyd == 183
    assert utsec == 43200
    assert stl == approx(14.8)


def test_list():

    iyd, utsec, stl = sd.datetime2gtd(T, glon=42)

    assert (iyd == 183).all()
    assert utsec == approx((43200, 0, 43200, 43200))
    assert stl == approx((14.8, 2.8, 14.8, 14.8))


def test_glon():
    glon = range(-180, 180 + 45, 45)

    iyd, utsec, stl = sd.datetime2gtd(T, glon)

    Estl = np.array([np.arange(0, 24 + 3, 3), np.arange(-12, 12 + 3, 3), np.arange(0, 24 + 3, 3), np.arange(0, 24 + 3, 3)])

    assert utsec == approx((43200, 0, 43200, 43200))
    assert stl == approx(Estl)


if __name__ == "__main__":
    pytest.main([__file__])
