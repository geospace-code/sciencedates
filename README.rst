.. image:: https://travis-ci.org/scienceopen/sciencedates.svg?branch=master
    :target: https://travis-ci.org/scienceopen/sciencedates

.. image:: https://coveralls.io/repos/github/scienceopen/sciencedates/badge.svg?branch=master
    :target: https://coveralls.io/github/scienceopen/sciencedates?branch=master

============
sciencedates
============
Date conversions used in the sciences.

.. contents::

Install
=======
::

    pip install sciencedates

Examples
========
::

    from pytz import UTC
    from datetime import datetime
    import sciencedates as sd

    T = datetime(2013,7,2,12,0,0,tzinfo=UTC)
    yd,utsec=sd.datetime2yd(T)
