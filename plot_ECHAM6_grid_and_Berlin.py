# plots the grid of ECHAM6 and Berlin

from netCDF4 import Dataset
import matplotlib as mpl
#mpl.use('Agg')
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from plot_Berlin_shape import plot_Berlin_shape
import numpy as np
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon

def get_grid(filename_nc): 
  f = Dataset(filename_nc, "r", format="NetCDF4")
  lat = f.variables['lat'][:]
  lon = f.variables['lon'][:]
  f.close()
  d_lat = lat[1:len(lat)] - lat[0:len(lat)-1]
  d_lon = lon[1:len(lon)] - lon[0:len(lon)-1]
  lat = lat[0:len(lat)-1] - 0.5*d_lat
  lon = lon[0:len(lon)-1] - 0.5*d_lon
  lat = lat.tolist()
  lon = lon.tolist()
  lat.append(lat[len(lat)-1]+d_lat[len(d_lat)-1])
  lat.append(lat[len(lat)-1]+d_lat[len(d_lat)-1])
  lon.append(lon[len(lon)-1]+d_lon[len(d_lon)-1])
  lon.append(lon[len(lon)-1]+d_lon[len(d_lon)-1])
  lon = np.asarray(lon)
  lat = np.asarray(lat)
  return lat, lon 

def plot_grid_on_map(m, lat, lon, color):
  for i_lon in range(0, len(lon)-1):
    # print(i_lon, len(lon)-1)
    if((lon[i_lon] > m.llcrnrlon-1) and (lon[i_lon] < m.urcrnrlon + 1)):
      for i_lat in range(0, len(lat)-1):
        if((lat[i_lat] > m.llcrnrlat-1) and (lat[i_lat] < m.urcrnrlat + 1)):
          x1, y1 = m(lon[i_lon], lat[i_lat]) # lower left
          x2, y2 = m(lon[i_lon+1], lat[i_lat])
          x3, y3 = m(lon[i_lon+1], lat[i_lat+1])
          x4, y4 = m(lon[i_lon], lat[i_lat+1])
          m.plot([x1,x2],[y2,y2], color=color)
          m.plot([x2,x3],[y2,y3], color=color)
          m.plot([x3,x4],[y3,y4], color=color)
          m.plot([x4,x1],[y4,y1], color=color)

def test_polygon_inside(test_x, test_y, ref_x, ref_y):
  # only for grid-parallel polygons !!!
  inside = False
  if((min(test_x) < max(ref_x)) and (max(test_x) > min(ref_x))):
    if((min(test_y) < max(ref_y)) and (max(test_y) > min(ref_y))):
      inside = True
  return inside
   


filename_ECHAM_nc = "ssp585-LR_rcm_fx_1.nc"
lat_echam, lon_echam = get_grid(filename_ECHAM_nc)

filename_ERA5 = "ERA5_temperature_2009.nc"
lat_era5, lon_era5 = get_grid(filename_ERA5)

Berlin_lat = 52.518
Berlin_lon = 13.408



ilat_Berlin_echam = np.max(np.where(lat_echam >= Berlin_lat))
ilon_Berlin_echam = np.max(np.where(lon_echam <= Berlin_lon))
print("ECHAM ilat: ", ilat_Berlin_echam, " ilon: ",ilon_Berlin_echam) 

lon_min_plot = 10.0
lon_max_plot = 20.0
lat_min_plot = 50.0
lat_max_plot = 55.0

lat_0 = (lat_max_plot + lat_min_plot) / 2.0
lon_0 = (lon_min_plot + lon_max_plot) / 2.0

fig = plt.figure(figsize=(6, 6))
ax1 = fig.add_axes([0.05, 0.05, 0.75, 0.9])
m = Basemap(projection='merc', lat_0 = lat_0, lon_0 = lon_0,
    resolution = 'i', area_thresh = 150.0,
    llcrnrlon=lon_min_plot, llcrnrlat=lat_min_plot,
    urcrnrlon=lon_max_plot, urcrnrlat=lat_max_plot)
m.drawcountries(zorder=10)
m.drawcoastlines(zorder=10, color="grey")

print(m.llcrnrlon)

cmap = mpl.cm.get_cmap('jet')

plot_Berlin_shape(m, plt, fill=False, linewidth=1.0)

color = "b"
plot_grid_on_map(m, lat_echam, lon_echam, color)

x1_echam, y1_echam = m(lon_echam[ilon_Berlin_echam], lat_echam[ilat_Berlin_echam]) # lower left
x2_echam, y2_echam = m(lon_echam[ilon_Berlin_echam+1], lat_echam[ilat_Berlin_echam])
x3_echam, y3_echam = m(lon_echam[ilon_Berlin_echam+1], lat_echam[ilat_Berlin_echam+1])
x4_echam, y4_echam = m(lon_echam[ilon_Berlin_echam], lat_echam[ilat_Berlin_echam+1])
xy = np.zeros((4,2))
xy[:,0] = np.asarray([x1_echam,x2_echam,x3_echam,x4_echam])
xy[:,1] = np.asarray([y1_echam,y2_echam,y3_echam,y4_echam])
polygon = Polygon(xy, color="green")
collection = PatchCollection([polygon])
ax1.add_collection(collection)        

color = "r"
plot_grid_on_map(m, lat_era5, lon_era5, color)

color = "g"
ref_x_echam = [x1_echam,x2_echam,x3_echam,x4_echam]
if(y1_echam > y4_echam):
  ref_y_echam = [y4_echam,y3_echam,y2_echam,y1_echam]
else:  
  ref_y_echam = [y1_echam,y2_echam,y3_echam,y4_echam]

res_ilon_era5 = []
res_ilat_era5 = []
res_area_era5 = []
for ilon in range(0, len(lon_era5)-2):
  if((lon_era5[ilon] > lon_min_plot-5) and ((lon_era5[ilon] < lon_max_plot+5))):
    for ilat in range(0, len(lat_era5)-2):
      if((lat_era5[ilat] > lat_min_plot-5) and ((lat_era5[ilat] < lat_max_plot+5))):
        x1_era5, y1_era5 = m(lon_era5[ilon], lat_era5[ilat])
        x2_era5, y2_era5 = m(lon_era5[ilon+1], lat_era5[ilat])
        x3_era5, y3_era5 = m(lon_era5[ilon+1], lat_era5[ilat+1]) 
        x4_era5, y4_era5 = m(lon_era5[ilon], lat_era5[ilat+1])
        test_x_era5 = [x1_era5, x2_era5, x3_era5, x4_era5]
        test_y_era5 = [y1_era5, y2_era5, y3_era5, y4_era5]
        inside = test_polygon_inside(test_x_era5, test_y_era5, ref_x_echam, ref_y_echam)
        if(inside == True):
          xy = np.zeros((4,2))
          xy[:,0] = np.asarray(test_x_era5)
          xy[:,1] = np.asarray(test_y_era5)
          polygon = Polygon(xy, color=(0.0,1.0,0.0))
          collection = PatchCollection([polygon], zorder=10)
          ax1.add_collection(collection)
          # get intersection of polygon
          x1_intersect = max([min(test_x_era5),min(ref_x_echam)])
          x2_intersect = min([max(test_x_era5),max(ref_x_echam)])
          y1_intersect = max([min(test_y_era5),min(ref_y_echam)])
          y2_intersect = min([max(test_y_era5),max(ref_y_echam)])
          dx = x2_intersect - x1_intersect
          dy = y2_intersect - y1_intersect
          area_temp = dx * dy
          res_ilon_era5.append(ilon)
          res_ilat_era5.append(ilat)
          res_area_era5.append(area_temp)
          
sum_area_era5 = sum(res_area_era5)
area_echam6 = (ref_x_echam[1] - ref_x_echam[0]) * (ref_y_echam[2] - ref_y_echam[1])
print(sum_area_era5, area_echam6)
for i in range(0, len(res_area_era5)):
  res_area_era5[i] = res_area_era5[i]/sum_area_era5
  res_area_era5[i] = round(res_area_era5[i], 6)
  
for i in range(0, len(res_area_era5)):
  print(res_ilat_era5[i], res_ilon_era5[i], res_area_era5[i])
print(sum(res_area_era5))

filename_plot = "ECHAM6_grid_and_Berlin.png"
plt.savefig(filename_plot, dpi=300, bbox_inches='tight')
plt.close()
print("fertig")

