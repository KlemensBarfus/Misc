# Identify the shape defined by a shapefile in the radar domain
# -> output are radar indizes
from netCDF4 import Dataset
import numpy as np
from polarstereographic_projection import latlon_to_xy
from mpl_toolkits.basemap import Basemap
from xy2ij import xy_to_ij
import matplotlib.pyplot as plt
import matplotlib.path as mplPath
import math
import pickle
from lambert_conformal_projection import xy2latlon as lambert_xy2latlon
from lambert_conformal_projection import latlon2xy as lambert_latlon2xy
from read_index_file import read_index_file
#from radolan_coordinates import radolan_coordinates, radolan_plot_coordinates

def read_shapefile(shape_path, m):
  # reads a shapefile (currently with only one shape) and returns numpy arrays with longitude and latitude
  import numpy as np
  from matplotlib.patches import Polygon
  # plot polygon of Berlin
  #shape_path = "/home/barfus/Shapefiles/Berlin_WGS84_l"
  sf = m.readshapefile(shape_path, 'shape_data', drawbounds = False)
  lon = np.zeros(len(m.shape_data[0]))
  lat = np.zeros(len(m.shape_data[0]))
  for ii in range(0, len(m.shape_data[0])):
    x_temp = m.shape_data[0][ii][0]
    y_temp = m.shape_data[0][ii][1]
    lon_temp, lat_temp = m(x_temp, y_temp, inverse=True)
    lon[ii] = lon_temp
    lat[ii] = lat_temp
  return lat, lon

def read_wrf_coordinates(filename_wrf, x_min=None, x_max=None, y_min=None, y_max=None):
  # reads the WRF geo domain file
  f = Dataset(filename_wrf, "r", format="NetCDF4")
  latname = 'XLAT_C'
  lat = f.variables[latname]
  if(lat.ndim == 2):
    lat = lat[:,:]
  else:
    if(lat.ndim == 3):
      lat = lat[0,:,:]
      lat = np.squeeze(lat)
  lonname = 'XLONG_C'
  lon = f.variables[lonname]
  if(lon.ndim == 2):
    lon = lon[:,:]
  else:
    if(lon.ndim == 3):
      lon = lon[0,:,:] # <- lat and lon are pixel centers !
      lon = np.squeeze(lon)
  f.close()
  return lat, lon


def read_wrf_grid(filename_wrf, x_min=None, x_max=None, y_min=None, y_max=None):
  # reads the WRF geo domain file
  if(x_min != None):
    lat, lon = read_wrf_coordinates(filename_wrf, x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max)
  else:
    lat, lon = read_wrf_coordinates(filename_wrf)
  lon_temp_wrf, lat_temp_wrf = WRF_get_plot_grid_for_geographical_coordinates(lon, lat) # lon_temp_wrf[n_lon,n_lat,4] 
  if(x_min != None):
    nxy = lat.shape()
    n_lat = nxy[0]
    n_lon = nxy[1]
    x_min = 0
    x_max = n_lon
    y_min = 0
    y_max = n_lat
  # create polygon
  lat_res = []
  lon_res = []
  for i_lon in range(x_min, x_max+1): # lower bound
    lat_temp = lat_temp_wrf[i_lon,y_min,0]
    lon_temp = lon_temp_wrf[i_lon,y_min,0]
    lat_res.append(lat_temp)
    lon_res.append(lon_temp)
  for i_lat in range(y_min, y_max+1): # right bound
    lat_temp = lat_temp_wrf[x_max,i_lat,1]
    lon_temp = lon_temp_wrf[x_max,i_lat,1]
    lat_res.append(lat_temp)
    lon_res.append(lon_temp)
  for i_lon in range(x_max, x_min-1, -1): # upper bound
    lat_temp = lat_temp_wrf[i_lon,y_max,2]
    lon_temp = lon_temp_wrf[i_lon,y_max,2]
    lat_res.append(lat_temp)
    lon_res.append(lon_temp)  
  for i_lat in range(y_max, y_min-1, -1): # right bound
    lat_temp = lat_temp_wrf[x_min,i_lat,3]
    lon_temp = lon_temp_wrf[x_min,i_lat,3]
    lat_res.append(lat_temp)
    lon_res.append(lon_temp)
  return lat_res, lon_res

def read_radar_grid(x_min=None, x_max=None, y_min=None, y_max=None):
  lat_radar, lon_plot = get_radolan_plot_coordinates('YW')
  if(x_min != None):
    nxy = lat_radar.shape()
    n_lat = nxy[0]
    n_lon = nxy[1]
    x_min = 0
    x_max = n_lon
    y_min = 0
    y_max = n_lat
  # create polygon
  lat_res = []
  lon_res = []
  for i_lon in range(x_min, x_max+1): # lower bound
    lat_temp = lat_temp_wrf[i_lon,y_min,0]
    lon_temp = lon_temp_wrf[i_lon,y_min,0]
    lat_res.append(lat_temp)
    lon_res.append(lon_temp)
  for i_lat in range(y_min, y_max+1): # right bound
    lat_temp = lat_temp_wrf[x_max,i_lat,1]
    lon_temp = lon_temp_wrf[x_max,i_lat,1]
    lat_res.append(lat_temp)
    lon_res.append(lon_temp)
  for i_lon in range(x_max, x_min-1, -1): # upper bound
    lat_temp = lat_temp_wrf[i_lon,y_max,2]
    lon_temp = lon_temp_wrf[i_lon,y_max,2]
    lat_res.append(lat_temp)
    lon_res.append(lon_temp)
  for i_lat in range(y_max, y_min-1, -1): # right bound
    lat_temp = lat_temp_wrf[x_min,i_lat,3]
    lon_temp = lon_temp_wrf[x_min,i_lat,3]
    lat_res.append(lat_temp)
    lon_res.append(lon_temp)
  return lat_res, lon_res  
  
def test_if_rectangle_is_in_list(rec, list_x, list_y):
  # rectangle is [x_min,y_min,x_max,y_max]
  # list_x and list_y are numpy arrays 
  # if it is in it returns the indices for the list
  nx = rec[2] - (rec[0]-1)
  ny = rec[3] - (rec[1]-1)
  n = nx * ny
  index_list_xy = []
  ix = rec[0]
  iy = rec[1]
  found_all = False
  while(found_all == False):
    ix_temp = np.where(list_x == ix)
    if(len(ix_temp[0]) > 0):
      iy_temp  = np.where(list_y == iy)
      if(len(iy_temp[0]) > 0):
        ixy_temp = np.intersect1d(ix_temp,iy_temp)
        if(len(ixy_temp) > 0):
          index_list_xy.append(ixy_temp[0])
          ix = ix + 1
          if(ix > rec[2]):
            ix = rec[0]
            iy = iy + 1
            if(iy > rec[3]):
              found_all = True  
        else:
          found_all = True
      else:
        found_all = True  
    else:
      found_all = True
  if(len(index_list_xy) == n):
    in_list = True
  else:
    in_list = False
  return in_list, index_list_xy

def pixel_closest_to_median_values(median_i, median_j, list_i, list_j):     
  # pixel closest to median values
  di = list_i - median_i
  dj = list_j - median_j
  dist = np.sqrt(np.square(di) + np.square(dj))
  min_dist = np.min(dist)
  k_min = np.where(dist == min_dist)
  i_res = np.asscalar(list_i[k_min[0][0]])
  j_res = np.asscalar(list_j[k_min[0][0]])
  return i_res, j_res  

def read_polygon_for_index(shape_path=None,filename=None,grid_subset=None):
  # reads the polygon where we want to get the indices for
  # can be shapefile or gridded file like wrf
  # if gridded file, part of the gridfile can be determined by
  # grid_subset = [x_min,y_min,x_max,y_max]
  
  if(shape_path != None):
    from mpl_toolkits.basemap import Basemap
    lon_min_plot = 10.0
    lon_max_plot = 16.0
    lat_min_plot = 49.0
    lat_max_plot = 53.0
    lat_0 = (lat_max_plot + lat_min_plot) / 2.0
    lon_0 = (lon_min_plot + lon_max_plot) / 2.0
    m = Basemap(projection='merc', lat_0 = lat_0, lon_0 = lon_0,
      resolution = 'h', area_thresh = 0.1,
      llcrnrlon=lon_min_plot, llcrnrlat=lat_min_plot,
      urcrnrlon=lon_max_plot, urcrnrlat=lat_max_plot)
    lat_boundary, lon_boundary = read_shapefile(shape_path, m)

  if(filename != None):
    if(grid_subset != None):
        x_min = grid_subset[0]
        y_min = grid_subset[1]
        x_max = grid_subset[2]
        y_max = grid_subset[3]
    if("geo_em.d0" in filename): # WRF file
      if(grid_subset != None):
        lat_boundary, lon_boundary = read_wrf_grid(filename, x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max)
      else:  
        lat_boundary, lon_boundary = read_wrf_grid(filename)
    else:                      # currently radar file
      product = 'YW'
      if(grid_subset != None):
        lat_boundary, lon_boundary = read_radar_grid(x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max)
      else:
        lat_boundary, lon_boundary = read_radar_grid()
  return lat_boundary, lon_boundary

def convert_polygon_latlon_to_grid_projection(grid,lat_boundary,lon_boundary,filename_wrf=None):
  # converts latitude and longitude of the polygon to projection of the (rectangular) target grid
  # 'grid' defines the target grid (currently either 'radar' (YW)  or 'WRF'
  # output are 2 lists: x_boundary and y_boundary  
  x_boundary = []
  y_boundary = []
  if(grid == 'radar'):
    # get radar coordinates
    # convert reference to target projection
    for i in range(0, len(lat_boundary)):
      x_boundary_temp, y_boundary_temp = latlon_to_xy(lat_boundary[i], lon_boundary[i])
      x_boundary.append(x_boundary_temp)
      y_boundary.append(y_boundary_temp)
  if(grid == 'WRF'):
    from WRF_read_projection_data import WRF_read_projection_data
    proj_WRF = WRF_read_projection_data(filename_wrf)
    if(proj_WRF['map_projection'] == 'Lambert Conformal'):
      m_wrf =Basemap(width=12000000,height=9000000,\
            rsphere=(6370000.00,6370000.00), projection='lcc',\
            lat_1=proj_WRF['truelat1'],lat_2=proj_WRF['truelat2'],\
            lat_0=proj_WRF['center_latitude'],lon_0=proj_WRF['center_longitude'])
      lat_0=proj_WRF['center_latitude']
      lon_0=proj_WRF['center_longitude']
      x0, y0 = m_wrf(lat_0, lon_0)
      for i in range(0, len(lat_boundary)):
        x_temp, y_temp = m_wrf(lat_boundary[i], lon_boundary[i])
        x_boundary.append(x_temp - x0) # WHY THE DIFFERENCE ??
        y_boundary.append(y_temp - y0)
  return x_boundary, y_boundary        

def get_target_grid_in_projection_coordinates(grid, filename_wrf=None):
  if(grid == 'radar'):
    x_temp, y_temp, test_lat, test_lon = radolan_coordinates('/home/klemens/Radar/test.nc')
    n_temp = test_lat.shape
    n_lat = n_temp[0]
    n_lon = n_temp[1]
    x_test, y_test = latlon_to_xy(test_lat, test_lon)
  if(grid == 'WRF'):
    from WRF_read_projection_data import WRF_read_projection_data
    lat_wrf, lon_wrf = read_wrf_coordinates(filename_wrf)
    n_temp = lat_wrf.shape
    n_lat = n_temp[0]
    n_lon = n_temp[1]
    x_test = np.zeros((n_lat,n_lon))
    y_test = np.zeros((n_lat,n_lon))
    proj_WRF = WRF_read_projection_data(filename_wrf)
    if(proj_WRF['map_projection'] == 'Lambert Conformal'):
      m_wrf =Basemap(width=12000000,height=9000000,\
            rsphere=(6370000.00,6370000.00), projection='lcc',\
            lat_1=proj_WRF['truelat1'],lat_2=proj_WRF['truelat2'],\
            lat_0=proj_WRF['center_latitude'],lon_0=proj_WRF['center_longitude'])
      lat_0=proj_WRF['center_latitude']
      lon_0=proj_WRF['center_longitude']
      x0, y0 = m_wrf(lat_0, lon_0)
    for i_lat in range(0, n_lat):
      for i_lon in range(0, n_lon):
        x_test_temp, y_test_temp = m_wrf(lat_wrf[i_lat,i_lon], lon_wrf[i_lat,i_lon])
        x_test[i_lat,i_lon] = x_test_temp - x0
        y_test[i_lat,i_lon] = y_test_temp - y0
  return x_test, y_test

def get_target_grid_in_latlon_coordinates(grid, filename_wrf=None):
  if(grid == 'radar'):
    x_temp, y_temp, test_lat, test_lon = radolan_coordinates('/home/klemens/Radar/test.nc')
    res_lat = test_lat
    res_lon = test_lon
  if(grid == 'WRF'):
    lat_wrf, lon_wrf = read_wrf_coordinates(filename_wrf)
    res_lat = lat_wrf
    res_lon = lon_wrf
  return res_lat, res_lon


def testplot_result(filename_indices, lat_boundary, lon_boundary, grid, filename_wrf=None):
  index_list = read_index_file(filename_indices)
  if(grid == 'radar'):
    test_lat, test_lon = get_target_grid_in_latlon_coordinates(grid)
  else:  
    test_lat, test_lon = get_target_grid_in_latlon_coordinates(grid, filename_wrf=filename_wrf)
  d_latlon = 1.0
  min_lat = min(lat_boundary)
  max_lat = max(lat_boundary)
  min_lon = min(lon_boundary)
  max_lon = max(lon_boundary)
  m = Basemap(projection='merc',llcrnrlat=min_lat-d_latlon,urcrnrlat=max_lat+d_latlon,\
            llcrnrlon=min_lon-d_latlon,urcrnrlon=max_lon+d_latlon,lat_ts=(min_lat+max_lat)/2.0,resolution='c')  
  m.drawcoastlines()
  m.drawcountries()
  n_temp = test_lat.shape
  n_lat = n_temp[0]
  n_lon = n_temp[1]
  for i_lat in range(0, n_lat):
    for i_lon in range(0, n_lon):
      res =  ij_in_index_list(i_lon,i_lat,index_list)
      if(res == True):
        x,y = m(test_lon[i_lat,i_lon], test_lat[i_lat,i_lon])
        m.plot(x, y, 'bo', markersize=4)
  # plot boundary
  for i in range(0, len(lat_boundary)):
    if(i == 0):
      x1, y1 = m(lon_boundary[i], lat_boundary[i])
    else:
      x2, y2 = m(lon_boundary[i], lat_boundary[i])
      m.plot([x1, x2], [y1, y2], color='r', linestyle='-', linewidth=2)
      x1 = x2
      y1 = y2
  x2, y2 = m(lon_boundary[0], lat_boundary[0])
  m.plot([x1, x2], [y1, y2], color='r', linestyle='-', linewidth=2)
  plt.show()
        
def ij_in_index_list(i,j,index_list):
  n = len(index_list) # index_list has format [[x_min,y_min,x_max,y_max],...] 
  found = False
  k = 0
  while((found == False) and (k < n)):
    temp_list = index_list[k]
    if(i >= temp_list[0]):
      if(i <= temp_list[2]):
        if(j >= temp_list[1]):
          if(j <= temp_list[3]):
            found = True
    if(found == False):
      k = k + 1
  return found    

shape_path = "/home/klemens/Shapefiles/Berlin_WGS84_l" # either the absolute path for the shapefile or empty if index area is not defined by shape
result_name = "/home/klemens/test6/indices_Berlin_in_WRF.dat" # defines file where indices are written
filename_wrf = "/home/klemens/test6/geo_em.d03.nc"
grid = 'WRF'
testplot = True
# 'reference' provides the shape/polygon and target are the data with indizes going into final list                                                                                                        
# #### reference polygon either shapefile or WRF geo_em file ######

lat_boundary, lon_boundary = read_polygon_for_index(shape_path=shape_path)
x_boundary, y_boundary = convert_polygon_latlon_to_grid_projection(grid,lat_boundary,lon_boundary,filename_wrf=filename_wrf) 

# generate polygon for point into polygon routine
bounds = np.zeros((len(x_boundary),2))
bounds[:,0] = x_boundary
bounds[:,1] = y_boundary
boundsPath = mplPath.Path(bounds)
r = 0.001 # accuracy for point into polygon check
      
# start testing pixels from target grid (currently radar or WRF)
x_test, y_test = get_target_grid_in_projection_coordinates(grid, filename_wrf=filename_wrf)  

n_temp = x_test.shape
n_lon = n_temp[1]
n_lat = n_temp[0]
  
i_in = [] # initial list with indizes 
j_in = []
for i_lon in range(0, n_lon):
  if(i_lon % 20 == 0):  
    print(i_lon, n_lon)  
  for i_lat in range(0, n_lat):
    x_test_temp = x_test[i_lat,i_lon]
    y_test_temp = y_test[i_lat,i_lon]
    # test if pixel is in polygon
    isIn = boundsPath.contains_point([x_test_temp,y_test_temp],radius=r) or boundsPath.contains_point([x_test_temp,y_test_temp],radius=-r)
    if(isIn == True):
      i_in.append(i_lon)
      j_in.append(i_lat)

# consolidate result
f = []
i_in = np.asarray(i_in)
j_in = np.asarray(j_in)
while(len(i_in) > 0):
  found_rectangle = False
  median_i_in = np.median(i_in)
  median_j_in = np.median(j_in)
  i_res, j_res = pixel_closest_to_median_values(median_i_in, median_j_in, i_in, j_in)  
  # start iteration
  res = [i_res,j_res,i_res,j_res]  # res has format [x_min,y_min,x_max,y_max]
  # delete start pixel from list
  i_delete = np.where(i_in == i_res)
  j_delete = np.where(j_in == j_res)
  ij_delete = np.intersect1d(i_delete, j_delete)
  i_in = np.delete(i_in, ij_delete)
  j_in = np.delete(j_in, ij_delete)
  while(found_rectangle == False):
    #print(cc)
    counter_tests = 0
    # test to the right
    rec_test = [res[2]+1,res[1],res[2]+1,res[3]]
    in_list, index_list_xy = test_if_rectangle_is_in_list(rec_test, i_in, j_in)
    if(in_list == True):
      counter_tests = counter_tests + 1
      i_in = np.delete(i_in, index_list_xy)
      j_in = np.delete(j_in, index_list_xy)
      res[2] = res[2] + 1
    # test to the top
    rec_test = [res[0],res[3]+1,res[2],res[3]+1]
    in_list, index_list_xy = test_if_rectangle_is_in_list(rec_test, i_in, j_in)
    if(in_list == True):
      counter_tests = counter_tests + 1
      i_in = np.delete(i_in, index_list_xy)
      j_in = np.delete(j_in, index_list_xy)
      res[3] = res[3] + 1
    # test to the left
    rec_test = [res[0]-1,res[1],res[0]-1,res[3]]
    in_list, index_list_xy = test_if_rectangle_is_in_list(rec_test, i_in, j_in)
    if(in_list == True):
      counter_tests = counter_tests + 1
      i_in = np.delete(i_in, index_list_xy)
      j_in = np.delete(j_in, index_list_xy)
      res[0] = res[0] - 1
    # test the bottom
    rec_test = [res[0],res[1]-1,res[2],res[1]-1]
    in_list, index_list_xy = test_if_rectangle_is_in_list(rec_test, i_in, j_in)
    if(in_list == True):
      counter_tests = counter_tests + 1
      i_in = np.delete(i_in, index_list_xy)
      j_in = np.delete(j_in, index_list_xy)
      res[1] = res[1] - 1
    if(counter_tests == 0):
      found_rectangle = True
      f.append(res)
        
      
       
# test result
i_res = []
j_res = []
for i1 in range(0, len(f)):        
  for i2 in range(f[i1][0], f[i1][2]+1):
    for j2 in range(f[i1][1], f[i1][3]+1):
      i_res.append(i2)
      j_res.append(j2)
nn = len(i_res)
xa = np.array(i_res)
xb = np.array(j_res)
xab = np.zeros((nn,2))
xab[:,0] = xa
xab[:,1] = xb
xab_unique = np.unique(xab, axis=0)
print(xab_unique.shape) 
x_test = n_lon * n_lat

min_i = xa.min()
max_i = xa.max()
min_j = xb.min()
max_j = xb.max()
test = np.zeros((max_i+1,max_j+1))
test[xa,xb] = 1
plt.imshow(test[min_i:max_i+1,min_j:max_j+1])
plt.draw()


# output results
f_out = open(result_name, "wb")
pickle.dump(f, f_out)
f_out.close()
print("fertig")

if(testplot == True):
  testplot_result(result_name, lat_boundary, lon_boundary, grid, filename_wrf=filename_wrf)
