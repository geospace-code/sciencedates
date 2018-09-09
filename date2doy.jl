#!/usr/bin/env julia
# convert date to day of year
using Dates

doy = Dates.dayofyear(DateTime(ARGS[1], "yyyy-mm-dd"))

println(doy)

