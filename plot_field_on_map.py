# plots data on an already existing map
# input is:
# data
# lon_plot = fltarr(nx,ny,4) with last dimension counterclockwise longitudes
# lat_plot = "
# m is the coordinate conversion matrix for the specific map projection
# optional arguments: minvalue and maxvalue, if not provided they are derived from the data
# optional: exclude_zero (default: false), if true only values > 0.0 are plotted
# written by K.Barfus 4/2016

from __future__ import unicode_literals
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
import gc



def plot_field_on_map(data, lon_plot, lat_plot, m, cmap, minvalue=float('nan'), maxvalue=float('nan'), exclude_zero=False ):
  if(math.isnan(minvalue)):
    minvalue = np.nanmin(data)
  if(math.isnan(maxvalue)):
    maxvalue = np.nanmax(data)
  n_lon = data.shape[1]
  n_lat = data.shape[0]
  x_plot, y_plot = m(lon_plot, lat_plot)
  xy_all = []
  rgb = []
  for i_lat in range(0, n_lat):
    for i_lon in range(0, n_lon):
      if(np.isfinite(data[i_lat,i_lon])):  
        d_val = data[i_lat,i_lon]
        d = (d_val - minvalue) / (maxvalue - minvalue)
        e = d * (1.0 - 0.2) + 0.2
        rgba = cmap(e)  #(d_val - minvalue)/ (maxvalue - minvalue))
        if(exclude_zero):
          if(data[i_lat,i_lon] > 0.0):
            xy = [tuple([x_plot[i_lat,i_lon,0], y_plot[i_lat,i_lon,0]]),tuple([x_plot[i_lat,i_lon,1], y_plot[i_lat,i_lon,1]]),tuple([x_plot[i_lat,i_lon,2], y_plot[i_lat,i_lon,2]]),tuple\
                 ([x_plot[i_lat,i_lon,3], y_plot[i_lat,i_lon,3]])]
            xy_all.append(xy)
            rgb.append(rgba)
        else:
          xy = [tuple([x_plot[i_lat,i_lon,0], y_plot[i_lat,i_lon,0]]),tuple([x_plot[i_lat,i_lon,1], y_plot[i_lat,i_lon,1]]),tuple([x_plot[i_lat,i_lon,2], y_plot[i_lat,i_lon,2]]),tuple\
               ([x_plot[i_lat,i_lon,3], y_plot[i_lat,i_lon,3]])]
          xy_all.append(xy)
          rgb.append(rgba)
  coll = PolyCollection(xy_all, color=rgb, linewidths=0.5, zorder=5)  # eventually use facecolor                                                                                                    
  plt.gca().add_collection(coll)
  

