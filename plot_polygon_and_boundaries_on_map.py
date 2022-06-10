def plot_polygon_and_boundaries_on_map(index_lat, index_lon, lat, lon, poly_lat=None, poly_lon=None):
  from mpl_toolkits.basemap import Basemap
  from matplotlib.collections import PolyCollection, LineCollection
  import gc
  lat_temp = lat[index_lat]
  lon_temp = lon[index_lon]
  min_lat = lat_temp.min()
  max_lat = lat_temp.max()
  min_lon = lon_temp.min()
  max_lon = lon_temp.max()
  mean_lat = (max_lat+min_lat)/2.0
  mean_lon = (max_lon+min_lon)/2.0
  d_latlon = (lat[1] - lat[0])*2
  d_lat = (lat[1] - lat[0])/2.0
  d_lon = (lon[1] - lon[0])/2.0
  
  m = Basemap(projection='merc', lat_0 = mean_lat, lon_0 = mean_lon,
    resolution = 'h', area_thresh = 0.1,                                                                                                                                                                   
    llcrnrlon=min_lon-d_latlon, llcrnrlat=min_lat-d_latlon,
    urcrnrlon=max_lon+d_latlon, urcrnrlat=max_lat+d_latlon)
  m.drawcoastlines()
  
  xy_all = []
  rgb_poly = [] 
  for i in range(0, len(index_lat)):
    i_lat = index_lat[i]
    i_lon = index_lon[i]
    x_plot1, y_plot1 = m(lon[i_lon]-d_lon, lat[i_lat]-d_lat)
    x_plot2, y_plot2 = m(lon[i_lon]+d_lon, lat[i_lat]-d_lat)
    x_plot3, y_plot3 = m(lon[i_lon]+d_lon, lat[i_lat]+d_lat)
    x_plot4, y_plot4 = m(lon[i_lon]-d_lon, lat[i_lat]+d_lat)
    xy = [tuple([x_plot1, y_plot1]),tuple([x_plot2, y_plot2]),tuple([x_plot3, y_plot3]),tuple([x_plot4, y_plot4])]
    xy_all.append(xy)
    rgb_poly.append([1,0,0])
  coll = PolyCollection(xy_all, color=rgb_poly, linewidths=0.0, zorder=5)  # eventually use facecolor                                                                                                    
  plt.gca().add_collection(coll)

  if(poly_lat is not None):
    lines = []
    rgb_lines = []
    n_poly = len(poly_lon)
    for i_lines in range(0, n_poly-1):
      x_line1, y_line1 = m(poly_lon[i_lines], poly_lat[i_lines])
      x_line2, y_line2 = m(poly_lon[i_lines+1], poly_lat[i_lines+1])
      lines.append([(x_line1, y_line1),(x_line2, y_line2)])
      rgb_lines.append([0,0,1])
    x_line1, y_line1 = m(poly_lon[n_poly-1], poly_lat[n_poly-1])
    x_line2, y_line2 = m(poly_lon[0], poly_lat[0])  
    lines.append([(x_line1, y_line1),(x_line2, y_line2)])
    rgb_lines.append([0,0,1])     
    lc = LineCollection(lines, linewidths=2, colors=rgb_lines, zorder=8)
    plt.gca().add_collection(lc)
  plt.show()  
  
