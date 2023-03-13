def remove_files_from_list(files):
  import os
  for ffile in files:
    if(os.path.exists(ffile)):
      sys_cmd = "rm "+ffile
      os.system(sys_cmd)

