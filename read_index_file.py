def read_index_file(filename_indices):
  # res has format [[x_min,y_min,x_max,y_max],...]                                                                                                                                                         
  import pickle
  f_in = open(filename_indices, "rb")
  res = pickle.load(f_in)
  f_in.close()
  return res

