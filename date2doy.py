#!/usr/bin/env python
"""
command-line utility to convert date to day of year
"""
from sciencedates import date2doy


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='convert date to day of year')
    p.add_argument('date', help='yyyy-mm-dd')
    P = p.parse_args()

    doy, year = date2doy(P.date)

    print(doy)
