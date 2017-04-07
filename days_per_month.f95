module mod_days_per_month

contains

integer function days_per_month(year, month)
use mod_leap_year

implicit none

integer, intent(in):: year
integer, intent(in):: month

logical:: lp
integer, dimension(1:12):: dd

lp = leap_year(year)
if(lp.eqv.(.true.))then
  dd = (/31,29,31,30,31,30,31,31,30,31,30,31/)
 else
  dd = (/31,28,31,30,31,30,31,31,30,31,30,31/)
endif

days_per_month = dd(month)

end function

end module  
