#!/usr/bin/env python3
"""
generate a random date (month and day) in a year.
Michael Hirsch, Ph.D.
"""
from argparse import ArgumentParser
from datetime import date
from sciencedates import randomdate


p = ArgumentParser(description="generate random date in year")
p.add_argument("year", type=int, nargs="?", default=date.today().year)
P = p.parse_args()

print(randomdate(P.year))
