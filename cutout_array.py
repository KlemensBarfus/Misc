# cuts out a 2d array due to specific conditions
# conditions are >= minvalue and <= maxvalue
# function also acts on arrays with NaNs 
# to test uncomment the lower part


def cutout_array(f, minv, maxv):
  import numpy as np
  index_nan = np.isnan(f)
  if(len(index_nan[0]) > 0):
    f2 = np.copy(f)
    f[index_nan] = minv-1
  ji = np.where((f >= minv) & (f <= maxv))
  j = ji[0]
  i = ji[1]
  j_min = j.min()
  j_max = j.max()
  i_min = i.min()
  i_max = i.max()
  nj = j_max - (j_min-1)
  ni = i_max - (i_min-1)
  if(len(index_nan[0]) > 0):
    res = f2[j_min:j_max+1,i_min:i_max+1]
  else:  
    res = f[j_min:j_max+1,i_min:i_max+1]
  return j_min, i_min, nj, ni, res


#import numpy as np    
#f = np.zeros((10,10))
#f[4,4] = np.nan
#f[5:7,5:7] = 5
#f[7,7] = 6
#print(f)
#minv = 5
#maxv = 6 
#j_min,	i_min, nj, ni, res = cutout_array(f, minv, maxv)
#print(j_min,  i_min, nj, ni)
#print(res)






