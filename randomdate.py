#!/usr/bin/env python
"""
generate a random date (month and day) in a year.
Michael Hirsch, Ph.D.
"""
from datetime import date
from sciencedates import randomdate

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('year',type=int,nargs='?',default=date.today().year)
    p = p.parse_args()

    print(randomdate(p.year))
