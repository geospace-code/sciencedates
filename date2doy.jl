#!/usr/bin/env julia
#=
command-line utility to convert date to day of year
=#
using Base.Dates
using ArgParse


function date2doy(date)

  date = DateTime(date, "yyyy-mm-dd")

  year = DateTime(Dates.year(date))
  
  doy = Day(date - year)
  
end

s = ArgParseSettings()
@add_arg_table s begin
    "date"
        help = "date yyyy-mm-dd"
        required = true
end
s = parse_args(s)


doy = date2doy(s["date"])

println("Day of Year  $doy")


