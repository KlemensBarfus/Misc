def check_if_timeseries_is_complete(date, var, d_time=None, start_date=None, stop_date=None, missing_value='NaN'):
  import numpy as np
  import datetime
  # checks if (equidistant) timeseries is complete
  # input is date (1d numpy array or list) of datetime object
  # var: variable (1d numpy array or list)
  # d_time [datetime.timedelta object]: temporal distance between timestamps (if not provided d_time is derived from provided data
  # start_date (datetime object), if not provided, first date entry is assumed to be the start_date
  # stop_date (datetime object), if not provided, last date entry is assumed to be the stop_date
  # missing value to be inserted, of not provided np.nan 
  # written by KBarfus, 08/10/2021

  if(missing_value == 'NaN'):
    missing_value = np.nan
    
  # check which type date and var are
  if(isinstance(date,list)):
    type_date = 'list'
    date = np.asarray(date)
  else:
    type_date = 'np_array'
  if(isinstance(var,list)):
    type_var =	'list'
    var = np.asarray(var)
  else:
    type_var =	'np_array'
  
  n_times = len(date)
  if(start_date is None):
    start_date = date[0]
  if(stop_date is None):
    stop_date = date[n_times-1]
  if(d_time is None):
    d_time_temp = date[1:n_times] - date[0:n_times-1]
    d_time = np.min(d_time_temp)

  n_times_new = np.int((stop_date - start_date) / d_time + 1)
  date_new = np.arange(float(0), float(n_times_new), 1.0) * d_time + start_date
  var_new = np.zeros((n_times_new))
  for i in range(0, len(date_new)):
    j = np.where(date == date_new[i])
    if(len(j[0]) > 1):
      print("error: ", date_new[i])
      exit
    else:
      if(len(j[0]) == 0):
        var_new[i] = missing_value
      else:
        var_new[i] = var[j]
  if(type_var == 'list'):
    var_new = var_new.tolist()
  if(type_date == 'list'):
    date_new = date_new.tolist()                   
  return date_new, var_new  
    
