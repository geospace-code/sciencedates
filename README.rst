.. image:: https://zenodo.org/badge/81351748.svg
   :target: https://zenodo.org/badge/latestdoi/81351748
.. image:: https://travis-ci.org/scivision/sciencedates.svg?branch=master
    :target: https://travis-ci.org/scivision/sciencedates

.. image:: https://coveralls.io/repos/github/scivision/sciencedates/badge.svg?branch=master
    :target: https://coveralls.io/github/scivision/sciencedates?branch=master

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
