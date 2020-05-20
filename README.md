[![image](https://zenodo.org/badge/81351748.svg)](https://zenodo.org/badge/latestdoi/81351748)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/scivision/sciencedates.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/scivision/sciencedates/context:python)
[![Actions Status](https://github.com/scivision/sciencedates/workflows/ci/badge.svg)](https://github.com/scivision/sciencedates/actions)
[![Python versions (PyPI)](https://img.shields.io/pypi/pyversions/sciencedates.svg)](https://pypi.python.org/pypi/sciencedates)
[![PyPi Download stats](http://pepy.tech/badge/sciencedates)](http://pepy.tech/project/sciencedates)

# Science Dates & Times

Date & time conversions used in the sciences.
The assumption is that datetimes are **timezone-naive**, as this is required in Numpy *et al* for `numpy.datetime64`.


## Install

```sh
python -m pip install sciencedates
```

## Usage

### Datetime => Year, DayOfYear

```python
import sciencedates as sd

T = '2013-07-02T12'
yeardoy, utsec = sd.datetime2yd(T)
```

Results in year,DayOfYear; UTC fraction of day [seconds]

> (2013102, 72000.0)


## Julia

Julia [examples](./julia) are provided

## Matlab / GNU Octave

Matlab / GNU Octave [examples](./matlab) are provided

## Fortran

Fortran [examples](./fortran) are provided.
For Python-like modern Fortran datetime, see
[Datetime-Fortran](https://github.com/wavebitscientific/datetime-fortran).
