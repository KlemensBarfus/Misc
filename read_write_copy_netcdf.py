def read_netcdf(filename):
  # reads a netcdf file into a structure 
  from netCDF4 import Dataset

  # filename = "/home/barfus/DCUA/LCZ/geo_em.d03.nc"
  res = {}
  res["filename"] = filename

  # open file
  f = Dataset(filename, "r", format="NetCDF4")
  res["data_model"] = f.data_model
  # global attributes
  res["global_attributes"] = f.__dict__
  # dimensions
  res["dimensions"] = [] 
  for name, dimension in f.dimensions.items():
    if(dimension.isunlimited()):
      res["dimensions"].append({"name": name, "length": len(dimension), "dimension": dimension, "unlimited": True})
    else:
      res["dimensions"].append({"name": name, "length": len(dimension), "dimension": dimension, "unlimited": False})  
  # variables
  res["variables"] = []
  i_var = 0 
  for key in f.variables: # this is an ordered dict 
    v_temp = f.variables[key]
    res["variables"].append({"name": key, "type": v_temp.dtype, "dimensions": v_temp.dimensions, "var": v_temp[:]})
    #print(res["variables"])
    if(len(v_temp.ncattrs()) > 0): # attributes exist 
      #print(key, " ", v_temp.ncattrs())
      res["variables"][i_var]["attributes"] = []
      for attr in v_temp.ncattrs():
        attribute_name = attr
        attribute_value = v_temp.getncattr(attr)
        res["variables"][i_var]["attributes"].append({"name": attribute_name, "value": attribute_value})
    i_var = i_var + 1
  f.close()
  return res

def write_netcdf(res):
  from netCDF4 import Dataset
  # write to file
  # res["filename"] = "/home/barfus/DCUA/LCZ/geo_em.d03_test.nc"
  f_out = Dataset(res["filename"], "w", format=res["data_model"])
  # global attributes
  for key, value in res["global_attributes"].items():
    f_out.setncatts({key: value})
  # dimensions
  for dim in res["dimensions"]:
    if(dim["unlimited"] == True):
      f_out.createDimension(dim["name"], (None))
    else:
      f_out.createDimension(dim["name"], dim["length"])
  # variables
  i_var = 0
  for var in res["variables"]:
    v_temp = f_out.createVariable(var["name"], var["type"], var["dimensions"])
    v_temp[:] = var["var"]
    #if(i_var <= 1):
    #  print(var["name"])
    if("attributes" in var): # if attributes exist 
      for attr in var["attributes"]:
        #if(i_var <= 1):
          #print(attr["name"], " -> ", attr["value"])
        v_temp.setncatts({attr["name"]: attr["value"]})
    i_var = i_var + 1
  f_out.close()
