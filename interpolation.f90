module mod_interpolation

contains

subroutine interpolation(nx_data, ny_data, x_data, y_data, var, ncols, nrows, x_rekis, y_rekis, max_n, max_search_dist, data_rekis)

implicit none

integer, intent(in):: nx_data, ny_data
real, dimension(1:nx_data,1:ny_data), intent(in):: x_data, y_data, var
integer, intent(in):: ncols, nrows
real, dimension(1:ncols,1:nrows), intent(in):: x_rekis, y_rekis
integer, intent(in):: max_n
real, intent(in):: max_search_dist
real, dimension(1:ncols,1:nrows), intent(out):: data_rekis   


integer:: i, j, k
integer:: i0, i1, ni, j0, j1, nj, n_summed 
real:: min_dist, max_dist, summed_weights, temp_var, weight_temp
integer, dimension(1:2):: index_min
real, dimension(1:nx_data,1:ny_data):: dist
real, dimension(1:11,1:11):: dist_temp, var_temp
logical:: found  
real, dimension(1:max_n):: temp_res, temp_dist
 


! interpolation
!max_n = 4
!max_dist = 15000.0
do i = 1, ncols
  if(mod(i,20).eq.0)then 
    print *, i
  endif   
  do j = 1, nrows
    dist = sqrt((x_data-x_rekis(i,j))**2 + (y_data-y_rekis(i,j))**2)
    index_min = minloc(dist)
    max_dist = maxval(dist)
    if(dist(index_min(1),index_min(2)) < 1.0)then
      data_rekis(i,j) = var(index_min(1),index_min(2))
     else
      i0 = max(index_min(1)-5, 1)
      i1 = min(index_min(1)+5, nx_data)
      ni = i1-(i0-1)
      j0 = max(index_min(2)-5, 1)
      j1 = min(index_min(2)+5, ny_data)
      nj = j1-(j0-1) 
      dist_temp = max_dist
      dist_temp(1:ni,1:nj) = dist(i0:i1,j0:j1)
      var_temp(1:ni,1:nj) = var(i0:i1,j0:j1) 
      found = .false.
      k = 1
      do
        if(found.eqv.(.true.)) exit
        min_dist = minval(dist_temp)
        if(min_dist.le.max_search_dist)then
          index_min = minloc(dist_temp)
          temp_res(k) = var_temp(index_min(1),index_min(2))
          temp_dist(k) = dist_temp(index_min(1),index_min(2))
          dist_temp(index_min(1),index_min(2)) = max_dist
          k = k + 1
          if(k.gt.max_n)then
            found = .true.
          endif
         else
          found = .true.
        endif
      enddo
      summed_weights = 0.0
      temp_var = 0.0
      n_summed = 0
      do k = 1, max_n
        if(temp_dist(k).gt.0.0)then
          weight_temp = 1.0 / temp_dist(k)
          temp_var = temp_var + weight_temp * temp_res(k)
          summed_weights = summed_weights + weight_temp
          n_summed = n_summed + 1
        endif
      enddo
      data_rekis(i,j) = temp_var / summed_weights
    endif 
  enddo
enddo

end subroutine

end module
