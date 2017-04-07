module mod_leap_year

contains

logical function leap_year(year)

implicit none

integer, intent(in):: year

logical:: lp

! determines if year is a leap year

lp = .false.
if(mod(year,4).eq.0)then
  lp = .true.
  if(mod(year,100).eq.0)then
    lp = .false.
    if(mod(year,400).eq.0)then
      lp = .true.
    endif
  endif
endif     

leap_year = lp

end function leap_year

end module mod_leap_year
