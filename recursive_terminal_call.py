# runs recursively through a directory and acts on predefined files
# directory is defined by 'start_dir'
# filename is defined by 'pattern'
# action is a terminal call and defined by 'sys_cmd' 
# written by Klemens Barfus 8/2023

import os
import fnmatch

start_dir = "/scratch/ws/0/barfus-WRF4.3/WRF-4.3/test/em_real/urb/"

pattern = "wrf_d01_????-??-??_??:??:??"       # unix filename pattern 
sys_cmd = "rm -v "                            # terminal command

for root, dirs, files in os.walk(start_dir):
  for name in files:
    if fnmatch.fnmatch(name, pattern):
      #print(sys_cmd+os.path.join(root, name))
      os.system(sys_cmd+os.path.join(root, name))
