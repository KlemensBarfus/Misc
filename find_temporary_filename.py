def find_temporary_filename(filename):
  # finds a temporary filename that does not exist in the current directory
  # e.g. for temporary storage of data when using CDO
  # it is expected (due to fuzziness of the temporary filename) that temporary file is later removed or modified
  # in principle the next free number is appended to filename
  import os

  counter = 1
  found = False

  temporary_filename = filename+str(counter)
  while found == False:
    if os.path.exists(temporary_filename):
      counter = counter + 1
      temporary_filename = filename+str(counter)
    else:
      found = True
  return temporary_filename       

    
