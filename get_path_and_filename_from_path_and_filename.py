def get_path_filename_from_path_and_filename(path_and_filename):
  temp1 = path_and_filename.split("/")
  path = "/"+"/".join(temp1[0:len(temp1)-1])+"/"
  filename = temp1[len(temp1)-1]
  return path, filename
