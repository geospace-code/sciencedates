#!/usr/bin/env julia
#=
generate a random date (month and day) in a year.
Michael Hirsch, Ph.D.
=#

using Base.Dates
using ArgParse

function randomdate(year)
    t = DateTime(year)
    t += Day(rand(0:daysinyear(t)-1))
end


s = ArgParseSettings()
@add_arg_table s begin
    "year"
        help = "year in which to generate a random date"
        arg_type = Int
        required = true
end
s = parse_args(s)

t = randomdate(s["year"])

println(Dates.format(t,"yyyy-mm-dd"))
