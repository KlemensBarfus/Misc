def sort_files_by_date(filenames):
  from get_path_and_filename_from_string import get_path_and_filename_from_string
  from find_dates_in_string import find_dates_in_string
  import datetime
  import numpy as np
  time_of_files = []
  for i_files in range(0, len(filenames)):
    if("/" in filenames[i_files]):
      path, filename_temp = get_path_and_filename_from_string(filenames[i_files])
    else:
      filename_temp = filenames[i_files]
    res, dd = find_dates_in_string(filename_temp)
    time_of_files.append(dd[0]) 
  time_of_files = np.asarray(time_of_files)
  index_sorted = np.argsort(time_of_files)
  filenames = np.asarray(filenames) 
  filenames = filenames[index_sorted]
  filenames = filenames.tolist()
  return filenames

