#!/usr/bin/env python3
"""
command-line utility to convert date to day of year
"""
from argparse import ArgumentParser
from sciencedates import date2doy


p = ArgumentParser(description="convert date to day of year")
p.add_argument("date", help="yyyy-mm-dd")
P = p.parse_args()

doy, year = date2doy(P.date)

print(doy.item())
