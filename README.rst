.. image:: https://zenodo.org/badge/81351748.svg
   :target: https://zenodo.org/badge/latestdoi/81351748
   
.. image:: https://travis-ci.org/scivision/sciencedates.svg?branch=master
    :target: https://travis-ci.org/scivision/sciencedates

.. image:: https://coveralls.io/repos/github/scivision/sciencedates/badge.svg?branch=master
    :target: https://coveralls.io/github/scivision/sciencedates?branch=master
    
.. image:: https://ci.appveyor.com/api/projects/status/r6adn3fdvk1qcx4r?svg=true
    :target: https://ci.appveyor.com/project/scivision/sciencedates

.. image:: https://api.codeclimate.com/v1/badges/47852e6e896d404d20a5/maintainability
   :target: https://codeclimate.com/github/scivision/sciencedates/maintainability
   :alt: Maintainability

============
sciencedates
============
Date conversions used in the sciences.

.. contents::

Install
=======
::

    python -m pip install -e .
    

Usage
========


Datetime => Year,DayOfYear
--------------------------

.. code:: python

    import sciencedates as sd

    T = '2013-07-02T12'
    yeardoy, utsec = sd.datetime2yd(T)
    
Results in year,DayOfYear; UTC fraction of day [seconds]

    (2013102, 72000.0)

