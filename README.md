[![image](https://zenodo.org/badge/81351748.svg)](https://zenodo.org/badge/latestdoi/81351748)
[![image](https://travis-ci.org/scivision/sciencedates.svg?branch=master)](https://travis-ci.org/scivision/sciencedates)
[![image](https://coveralls.io/repos/github/scivision/sciencedates/badge.svg?branch=master)](https://coveralls.io/github/scivision/sciencedates?branch=master)
[![image](https://ci.appveyor.com/api/projects/status/r6adn3fdvk1qcx4r?svg=true)](https://ci.appveyor.com/project/scivision/sciencedates)
[![Maintainability](https://api.codeclimate.com/v1/badges/47852e6e896d404d20a5/maintainability)](https://codeclimate.com/github/scivision/sciencedates/maintainability)
[![pypi format](https://img.shields.io/pypi/format/sciencedates.svg)](https://pypi.python.org/pypi/sciencedates)
[![PyPi Download stats](http://pepy.tech/badge/sciencedates)](http://pepy.tech/project/sciencedates)
[![PyPi Download stats](http://pepy.tech/badge/sciencedates)](http://pepy.tech/project/sciencedates)

# Science Dates & Times

Date & time conversions used in the sciences. 
The assumption is that datetimes are timezone-naive, as this will be required soon in Numpy *et al* for
`numpy.datetime64`.


## Install

    python -m pip install -e .

## Usage

### Datetime => Year, DayOfYear

```python
import sciencedates as sd

T = '2013-07-02T12'
yeardoy, utsec = sd.datetime2yd(T)
```

Results in year,DayOfYear; UTC fraction of day [seconds]

> (2013102, 72000.0)
