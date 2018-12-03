program a

implicit none

integer :: y4d3, y2d3

y4d3 = 2015294  ! October 21, 2015

y2d3 = yyyyddd2yyddd(y4d3)

print '(i5)', y2d3


contains

elemental integer function yyyyddd2yyddd(y4d3) result(yyddd)

integer, intent(in) :: y4d3
integer :: year4, year2, doy

doy2 = modulo(y4d3, 1000)
year4 = (y4d3 - doy) / 1000
year2 = modulo(year4, 100)

yyddd = year2 * 1000 + doy
end function yyyyddd2yyddd

end program
