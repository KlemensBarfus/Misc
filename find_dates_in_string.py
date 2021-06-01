def find_dates_in_string(string):
  # E.g. in case of filenames this routine extracts dates as strings as well as datetime objects
  # dates are in the format YYYYMMDD, YYYYMMDDHH, YYYYMMDDHHMM or YYYYMMDDHHMMSS and so
  # every string with digits >= 8 is interpreted as a date   
  import datetime
  from calendar import monthrange
  #num_days = monthrange(2019, 2)[1] # num_days = 28
  res = []
  dd = []
  j = 0
  for i in range(0, len(string)):
    if(string[i].isdigit() == True):
      if(len(res) == 0):
        res.append(string[i])
      else:
        if(string[i-1].isdigit() == True):
          res[j] = res[j] + string[i]
        else:
          res.append(string[i])
          j = j + 1
  # remove short strings        
  i  = 0
  tested_all = False
  allowed_length = [8,10,12,14]
  while(tested_all == False):
    remove_flag = False
    length = len(res[i])
    if(length in allowed_length == False):  # too short or wrong length
      remove_flag = True
    else:
      year_temp = int(res[i][0:4])
      month_temp = int(res[i][4:6])
      day_temp = int(res[i][6:8])
      hour_temp = 0
      minute_temp = 0
      second_temp = 0
      if(len(res[i]) > 8):
        hour_temp = int(res[i][8:10])
      if(len(res[i]) > 10):
        minute_temp = int(res[i][10:12])
      if(len(res[i]) > 12):
        second_temp = int(res[i][12:14])
      if(month_temp > 12): # not a month
        remove_flag = True
      else:
        num_days = monthrange(year_temp, month_temp)[1]     
        if(day_temp > num_days):  # are there climate models with 31 days in each month ?
          remove_flag = True
        else:
          if(hour_temp > 23):
            remove_flag = True
          else:
            if(minute_temp > 59):
              remove_flag = True
            else:
              if(second_temp > 59):
                remove_flag = True
    if(remove_flag == False):
      rec_date = datetime.datetime(year_temp,month_temp,day_temp,hour_temp,minute_temp,second_temp)
      dd.append(rec_date)
      i = i + 1
      if(i == len(res)):
        tested_all = True
    else:
      del(res[i])
  return res, dd    
