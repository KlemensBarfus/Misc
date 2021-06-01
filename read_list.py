# reads a list from a text file
# written by K.Barfus 11/2020

import os
def read_list(list_name):
  list=[]
  st = os.stat(list_name)  
  file_size = st.st_size
  f = open(list_name, 'rt')
  eof = 0
  while eof == 0:
    line = f.readline()
    list.append(line.rstrip())
    if f.tell() == file_size:
      eof = 1
  f.close()    
  return list
