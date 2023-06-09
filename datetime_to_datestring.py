def datetime_to_datestring(dt, fmt=None):
  import datetime
  # converts a datetime object (dt) to a string
  # optional parameter can be any part of "yyyymmddhhmmss"
  rec_year_str = str(dt.year).zfill(4)
  rec_month_str = str(dt.month).zfill(2)
  rec_day_str = str(dt.day).zfill(2)
  rec_hour_str = str(dt.hour).zfill(2)
  rec_minute_str = str(dt.minute).zfill(2)
  rec_second_str = str(dt.second).zfill(2)
  if(fmt is None):
    res = rec_year_str+rec_month_str+rec_day_str+rec_hour_str+rec_minute_str+rec_second_str
  else:
    res=""
    if("yyyymm" in fmt):
      res = res + rec_year_str + rec_month_str
    else:
      if("yyyy" in fmt):
        res = res + rec_year_str
      if("dd" in fmt):
        res = res + rec_day_str
      if("hhmm" in fmt):
        res = res + rec_hour_str + rec_minute_str
      else:
        if("hh" in fmt):
          res = res + rec_hour_str
        if("ss" in fmt):
          res = res + rec_second_str
  return res  
