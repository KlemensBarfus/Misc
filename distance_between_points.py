def distance_between_points(lon1, lat1, lon2, lat2):
  import numpy as np
  import math
  # calculates the distance of points defined by latitude and longitude applying the so-called Haversine formula                                                                                    
  # described in R. W. Sinnott, "Virtues of the Haversine," Sky and Telescope, vol. 68, no. 2, 1984, p. 159                                                                                             
  # assumes a sphere and so does not take into the oblatness of the earth                                                                                                                               
  # radius of the earth is assumed as 6371 km 

  # input:
  # lon1, lat1: longitude and latitude, scalar values [deg]
  # lon2, lat2: longitude and latitude, can be scalar or arrays [deg] 
  
  
  R = 6371.0 # radius of the earth in km
  to_rad = math.pi / 180.0

  
  lat2 = np.asarray(lat2)
  lon2 = np.asarray(lon2)

  scalar_input = False
  if lat2.ndim == 0:
    lat2 = lat2[None]
    lon2 = lon2[None]
    scalar_input = True

  dLat = lat2-lat1
  dLat_rad = dLat * to_rad
  dLon = lon2-lon1
  dLon_rad = dLon * to_rad
  lat1_rad = lat1 * to_rad
  lat2_rad = lat2 * to_rad

  a = np.sin(dLat_rad/2.0) * np.sin(dLat_rad/2.0) + np.sin(dLon_rad/2.0) * np.sin(dLon_rad/2.0) * np.cos(lat1_rad) * np.cos(lat2_rad)
  c = 2.0 * np.arctan2(np.sqrt(a), np.sqrt(1.0-a))
  d = R * c
  d = np.abs(d)
  
  if scalar_input:
    return np.squeeze(d)
  return d
