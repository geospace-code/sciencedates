#!/usr/bin/env python
"""
generate a random date (month and day) in a year.
Michael Hirsch, Ph.D.
"""
from datetime import date
from sciencedates import randomdate

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='generate random date in year')
    p.add_argument('year', type=int,
                   nargs='?', default=date.today().year)
    P = p.parse_args()

    print(randomdate(P.year))
