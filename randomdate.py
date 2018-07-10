#!/usr/bin/env python
"""
generate a random date (month and day) in a year.
Michael Hirsch, Ph.D.
"""
from argparse import ArgumentParser
from datetime import date
from sciencedates import randomdate


def main():
    p = ArgumentParser(description='generate random date in year')
    p.add_argument('year', type=int,
                   nargs='?', default=date.today().year)
    P = p.parse_args()

    print(randomdate(P.year))


if __name__ == '__main__':
    main()
