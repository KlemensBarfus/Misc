# calculates lambert projection based on spherical datum
# NOT BASED ON ELLIPSOIDAL DATUM LIKE WGS84 !!!!
# bases on http://mathworld.wolfram.com/LambertConformalConicProjection.html
# and the book of Snyder
# last changes KB 17.9.2022

# IMPORTANT:
# Basemaps m(lon,lat) does not provide x and y from the book of Snyder but x_basemap = x_Snyder(lat0,lon0) + 0.5*width and y_basemap = y_Snyder(lat0,lon0) + 0.5*height


import math
#from mpl_toolkits.basemap import Basemap
import numpy as np

def lambert_spherical_n(phi1, phi2):
  if(phi1 != phi2):
    n = (math.log(math.cos(math.radians(phi1)) * (1.0 / math.cos(math.radians(phi2)))) /
        math.log(math.tan(0.25 * math.pi + 0.5 * math.radians(phi2)) * (1.0 / math.tan(0.25 * math.pi + 0.5 * math.radians(phi1)))))
  else:
    n = math.sin(math.radians(phi1))
  return n
  
def lambert_spherical_F(phi1, n):
  F = (math.cos(math.radians(phi1)) * (math.tan(0.25*math.pi + 0.5 * math.radians(phi1)))**n) / n
  return F
  
def lambert_spherical_rho(F, phi, n, R):
  phi = np.asarray(phi)
  scalar_input = False
  if phi.ndim == 0:
    phi = phi[None]  # Makes x 1D
    scalar_input = True
    
  rho = R * F * (1.0/np.tan(0.25*math.pi + 0.5 * np.radians(phi)))**n

  if scalar_input:
    return np.squeeze(rho)
  return rho
  
def lambert_spherical_rho0(F, phi0, n, R):  
  rho0 = R * F * (1.0/math.tan(0.25*math.pi + 0.5 * math.radians(phi0)))**n
  return rho0
  
def lambert_spherical_x(phi1, phi2, phi, lambdaa, lambdaa0, R):
  phi = np.asarray(phi)
  lambdaa = np.asarray(lambdaa)
  scalar_input = False
  if phi.ndim == 0:
    phi = phi[None]  # Makes x 1D
    lambdaa = lambdaa[None]
    scalar_input = True
  
  n = lambert_spherical_n(phi1, phi2)
  F = lambert_spherical_F(phi1, n)
  rho = lambert_spherical_rho(F, phi, n, R)
  x = rho * np.sin((n*np.radians(lambdaa - lambdaa0)))  

  if scalar_input:
    return np.squeeze(x)
  return x


def lambert_spherical_y(phi1, phi2, phi0, phi, lambdaa, lambdaa0, R):
  phi = np.asarray(phi)
  lambdaa = np.asarray(lambdaa)
  scalar_input = False
  if phi.ndim == 0:
    phi = phi[None]  # Makes x 1D
    lambdaa = lambdaa[None]
    scalar_input = True

  n = lambert_spherical_n(phi1, phi2)
  F = lambert_spherical_F(phi1, n)
  rho0 = lambert_spherical_rho0(F, phi0, n, R)
  rho = lambert_spherical_rho(F, phi, n, R)
  y = rho0 - rho * np.cos(n* np.radians(lambdaa - lambdaa0))

  if scalar_input:
    return np.squeeze(y)
  return y

def lambert_spherical_lat(phi1, phi2, phi0, x, y, R):
  x = np.asarray(x)
  y = np.asarray(y)
  scalar_input = False
  if x.ndim == 0:
    x = x[None]  # Makes x 1D
    y = y[None]
    scalar_input = True
    
  n = lambert_spherical_n(phi1, phi2)
  F = lambert_spherical_F(phi1, n)
  rho0 = lambert_spherical_rho0(F, phi0, n, R)
  if(n >= 0):
    rho = (x**2.0 + (rho0-y)**2.0)**(0.5)
  else:
    rho = (x**2.0 + (rho0-y)**2.0)**(0.5) * (-1.0)
  phi = 2.0 * np.arctan((R*F / rho)**(1.0/n)) - 0.5 * math.pi
  phi = phi * (180.0/math.pi)

  if scalar_input:
    return np.squeeze(phi)
  return phi
  
def lambert_spherical_lon(phi1, phi2, phi0, lambdaa0, x, y, R):
  x = np.asarray(x)
  y = np.asarray(y)
  scalar_input = False
  if x.ndim == 0:
    x = x[None]  # Makes x 1D                                                                                                                                                                           
    y = y[None]
    scalar_input = True

  n = lambert_spherical_n(phi1, phi2)
  F = lambert_spherical_F(phi1, n)
  rho0 = lambert_spherical_rho0(F, phi0, n, R)
  theta = (np.arctan(x/(rho0 - y)))*(180.0/math.pi)
  lambdaa = lambdaa0 + theta / n

  if scalar_input:
    return np.squeeze(lambdaa)
  return lambdaa
  
def xy2latlon(x,y,lat1,lat2,lat0,lon0,R=6370000.0):
  phi1 = lat1 # standard latitude1
  phi2 = lat2 # standard latitude2
  phi0 = lat0 # reference latitude
  lambdaa0 = lon0 # reference longitude
  x = np.asarray(x)
  y = np.asarray(y)
  scalar_input = False
  if x.ndim == 0:
    x = x[None]  # Makes x 1D                                                                                                                                                                           
    y = y[None]
    scalar_input = True

  lat = lambert_spherical_lat(phi1, phi2, phi0, x, y, R)
  lon = lambert_spherical_lon(phi1, phi2, phi0, lambdaa0, x, y, R)                   

  if scalar_input:
    return np.squeeze(lat), np.squeeze(lon)
  return lat, lon
                     
def latlon2xy(lat,lon,lat1,lat2,lat0,lon0,R=6370000.0):
  phi1 = lat1 # standard latitude1
  phi2 = lat2 # standard latitude2
  phi0 = lat0 # reference latitude
  phi = lat
  lambdaa0 = lon0 # reference longitude
  lambdaa = lon                    
  phi = np.asarray(phi)
  lambdaa = np.asarray(lambdaa)
  scalar_input = False
  if phi.ndim == 0:
    phi = phi[None]  # Makes x 1D
    lambdaa = lambdaa[None]
    scalar_input = True

  x = lambert_spherical_x(phi1, phi2, phi, lambdaa, lambdaa0, R)
  y = lambert_spherical_y(phi1, phi2, phi0, phi, lambdaa, lambdaa0, R)

  if scalar_input:
    return np.squeeze(x), np.squeeze(y)
  return x, y




R = 6370000.0 # WRF radius
#lat0 = 51.049259
#lat1 = lat0 - 1.0
#lat2 = lat0 + 1.0
#lon0 = 13.73836

#lat = 51.0
#lon = 13.0


#R = 1.0
lat1 = 33.0
lat2 = 45.0
lat0 = 23.0
lon0 = -96.0

lat = np.asarray([[23.0,24.0],[23.0,24.0]]) #35.0
lon = np.asarray([[-96.0,-95.0],[-96.0,-95.0]]) #-75.0

print(lat, lon)

x,y = latlon2xy(lat,lon,lat1,lat2,lat0,lon0,R=R)
print(x, y)
lat_test, lon_test =  xy2latlon(x,y,lat1,lat2,lat0,lon0,R=R)
print(lat_test, lon_test)



