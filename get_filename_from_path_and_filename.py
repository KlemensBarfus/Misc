def get_filename_from_path_and_filename(path_and_filename):
  temp1 = path_and_filename.split("/")
  res = temp1[len(temp1)-1]
  return res
