def datestring_to_datetime(string):
  # gets a datetime date from a string
  # string can be any part of (starting at the beginning) 'yyyymmddhhmmss'
  # everything missing is filled up with ones(mm,dd) and zeros(hhmmss)
  # written by K.Barfus 2/2021
  import datetime
  len_str = len(string)
  month = 1
  day = 1
  hour = 0
  minute = 0
  second = 0
  year = int(string[0:4])
  if(len_str >= 6):
    month = int(string[4:6])
    if(len_str >= 8):
      day = int(string[6:8])
      if(len_str >= 10):
        hour = int(string[8:10])
        if(len_str >= 12):
          minute = int(string[10:12])
          if(len_str >= 14):
            second = int(string[12:14])
  rec_date = datetime.datetime(year,month,day,hour,minute,second)
  return rec_date
