def combine_pickle_files(files):
  # combines files written by pickle provided as list to overall file
  import pickle
  import os
  from find_dates_in_string import find_dates_in_string
  from get_filename_from_path_and_filename import get_filename_from_path_and_filename
  # get min and max time
  start_date_str = []
  stop_date_str = []
  for i_files in range(0, len(files)):
    filename = get_filename_from_path_and_filename(files[i_files])
    dd_str, dd = find_dates_in_string(filename)
    if(len(dd_str) == 1):
      start_date_str.append(dd_str[0])
    else:
      if(len(dd_str) == 2):
        start_date_str.append(dd_str[0])
        stop_date_str.append(dd_str[1])
  start_date_str_overall = start_date_str[0]
  stop_date_str_overall = stop_date_str[len(stop_date_str)-1]
  filename_overall = files[0].replace(start_date_str[0],start_date_str_overall)
  filename_overall = filename_overall.replace(stop_date_str[0],stop_date_str_overall)
  f_out = open(filename_overall, "wb")
  for i_files in range(0, len(files)):
    st = os.stat(files[i_files])
    file_size = st.st_size
    f_in = open(files[i_files], 'rb')
    eof = False
    while eof == False:
      res ={}
      res["year"] = pickle.load(f_in)
      res["month"] = pickle.load(f_in)
      res["day"] = pickle.load(f_in)
      res["hour"] = pickle.load(f_in)
      res["minute"] = pickle.load(f_in)
      res["size_center"] = pickle.load(f_in)
      res["size_cell"] = pickle.load(f_in)
      res["size_center_saxony"] = pickle.load(f_in)
      res["size_cell_saxony"] = pickle.load(f_in)
      pickle.dump(res, f_out)
      if f_in.tell() == file_size:
        eof = True
    f_in.close()
  f_out.close()
  return filename_overall

