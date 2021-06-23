import os
import glob

# requires CDO installed

path_to_search = "/scratch/ws/0/barfus-DCUA/ERA5/OWK/"
files = glob.glob(path_to_search+"*.grib")
for ffile in files:
  filename_nc = ffile.replace("grib", "nc")
  if (os.path.isfile(filename_nc) == False): # check if file exists
    sys_cmd = "cdo -f nc copy "+ffile+" "+filename_nc
