#!/usr/bin/env julia
#=
generate a random date (month and day) in a year.
Michael Hirsch, Ph.D.
=#

using Dates

function randomdate(year::Int)
  t = DateTime(year)
  t += Day(rand(0:daysinyear(t)-1))
end


t = randomdate(parse(Int,ARGS[1]))

println(Dates.format(t,"yyyy-mm-dd"))
