def get_polygon_lat_lon(i, j, lat, lon):
  import numpy as np
  # gets the vertices of the boundary including a polygon (convex or concave) with 4-point-connectivity.
  # vertices are stored clockwise, start and end point only appear once in the results.
  # input is
  # i: list or 1d array of horizontal indices of gridcells of polygon
  # j: list or 1d array of vertical indices of gridcells of polygon
  # lat: latitudes (equal distance) as list or 1d array corresponding to indices
  # lon: longitudes (equal distance) as list or 1d array corresponding to indices
  # written by K.Barfus 6/2022
    
  def test_side(rec_i, rec_j, i, j, side):
    # test for indices 'rec_i' and 'rec_j' if the pixel to one side
    # (defined by 'side' as "L": left, 'T': top, 'R': right, 'B': bottom)
    # is in lists of indices 'i' and 'j'
    # result is either 'True' or 'False'
    found = True
    if(side == "L"):
      if(rec_i > min(i)):
        if((rec_i-1,rec_j) in list(zip(i,j))):
          found = False
    if(side == "T"):
      if(rec_j < max(j)):
        if((rec_i,rec_j+1) in list(zip(i,j))):
          found = False
    if(side == "R"):
      if(rec_i < max(i)):
        if((rec_i+1,rec_j) in list(zip(i,j))):
          found	= False
    if(side == "B"):
      if(rec_j > min(j)):
        if((rec_i,rec_j-1) in list(zip(i,j))):
          found = False
    return found

  def add_coordinates(ii, jj, lat, lon, dd):
    # checks if coordinates can be added or if we are already closing the polygon
    # then 'found_last' will be set to 'True'
    # following variables are assumed to be 'global': lat, lon, d_lat, d_lon, eps,
    # lat_poly, lon_poly
    if(dd == 'L'):
      f_lat = -0.5
      f_lon = -0.5
    if(dd == 'U'):
      f_lat = +0.5
      f_lon = -0.5
    if(dd == 'R'):
      f_lat = +0.5
      f_lon = +0.5
    if(dd == 'D'):
      f_lat = -0.5
      f_lon = +0.5
    temp_lat = lat[jj] + f_lat * d_lat
    temp_lon = lon[ii] + f_lon * d_lon
    if((abs(temp_lat - lat_poly[0]) < eps) and (abs(temp_lon - lon_poly[0]) < eps)):
      found_last = True
    else:
      lat_poly.append(temp_lat)
      lon_poly.append(temp_lon)
      found_last = False
    return found_last


  d_lat = lat[1] - lat[0]
  d_lon = lon[1] - lon[0]
  lat_poly = [] 
  lon_poly = []
   # find pixel on the left edge (i == min(i))
  index_min = np.where(i == min(i))
  rec_i = np.asscalar(i[index_min[0]])
  rec_j = np.asscalar(j[index_min[0]])
  # to do: add coordinates to list
  lat_inside = lat[rec_j]
  lon_inside = lon[rec_i]
  lat_poly.append(lat[rec_j] - 0.5*d_lat) # lower left corner
  lon_poly.append(lon[rec_i] - 0.5*d_lon)
  lat_poly.append(lat[rec_j] + 0.5*d_lat) # upper left corner
  lon_poly.append(lon[rec_i] - 0.5*d_lon)
  eps = 0.000001
  direct = 'up' 
  found_last = False
  while(found_last == False):
    if(direct == 'up'):
      found_next = False
      if(found_last == False or found_next == False):
        # test left
        if((rec_i-1,rec_j+1) in list(zip(i,j))):
          test = test_side(rec_i-1,rec_j+1,i,j,'B')
          if(test == True):
            found_next = True
            found_last = add_coordinates(rec_i-1,rec_j+1,lat,lon,'L')
            rec_i = rec_i-1
            rec_j = rec_j+1
            direct = "left"
      if(found_last == False and found_next == False):
        # test up
        if((rec_i,rec_j+1) in list(zip(i,j))):
          test = test_side(rec_i-1,rec_j+1,i,j,'L')
          if(test == True):
            found_next = True
            found_last = add_coordinates(rec_i,rec_j+1,lat,lon,'U')
            rec_i = rec_i 
            rec_j = rec_j+1
            direct = "up"
      if(found_last == False and found_next == False):
        # test right
        if((rec_i,rec_j) in list(zip(i,j))):
          test = test_side(rec_i,rec_j,i,j,'T')
          if(test == True):
            found_next = True
            found_last = add_coordinates(rec_i,rec_j,lat,lon,'R')
            rec_i = rec_i
            rec_j = rec_j
            direct = "right"
    if(direct == 'left'):
      found_next = False
      # test down
      if(found_last == False and found_next == False):
        if((rec_i-1,rec_j-1) in list(zip(i,j))):
          test = test_side(rec_i-1,rec_j-1,i,j,'R')
          if(test == True):
            found_next = True
            found_last = add_coordinates(rec_i-1,rec_j-1,lat,lon,'D')
            rec_i = rec_i-1
            rec_j = rec_j-1
            direct = "down"
      if(found_last == False and found_next == False):
        # test left
      	if((rec_i-1,rec_j) in list(zip(i,j))):
          test = test_side(rec_i-1,rec_j,i,j,'B')
          if(test == True):
            found_next = True
            found_last = add_coordinates(rec_i-1,rec_j,lat,lon,'L')
            rec_i = rec_i-1
            rec_j = rec_j
            direct = "left"
      if(found_last == False and found_next == False):
        # test up
        if((rec_i,rec_j) in list(zip(i,j))):
          test = test_side(rec_i,rec_j,i,j,'L')
          if(test == True):
            found_next = True
            found_last = add_coordinates(rec_i,rec_j,lat,lon,'U')
            rec_j = rec_j
            direct = "up"
    if(direct == 'down'):
      found_next = False
      # test right
      if(found_last == False and found_next == False):
        if((rec_i+1,rec_j-1) in list(zip(i,j))):
          test = test_side(rec_i+1,rec_j-1,i,j,'U')
          if(test == True):
            found_next = True
            found_last = add_coordinates(rec_i+1,rec_j-1,lat,lon,'R')
            rec_i = rec_i+1
            rec_j = rec_j-1
            direct = "right"
      if(found_last == False and found_next == False):
        # test down
        if((rec_i,rec_j-1) in list(zip(i,j))):
          test = test_side(rec_i,rec_j-1,i,j,'R')
          if(test == True):
            found_next = True
            found_last = add_coordinates(rec_i,rec_j-1,lat,lon,'D')
            rec_j = rec_j-1
            direct = "down"
      if(found_last == False and found_next == False):
        # test left
        if((rec_i,rec_j) in list(zip(i,j))):
          test = test_side(rec_i,rec_j,i,j,'B')
          if(test == True):
            found_next = True
            found_last = add_coordinates(rec_i,rec_j,lat,lon,'L')
            rec_j = rec_j
            direct = "left"
    if(direct == 'right'):
      found_next = False
      if(found_last == False and found_next == False):
        # test up
        if((rec_i+1,rec_j+1) in list(zip(i,j))):
          test = test_side(rec_i+1,rec_j+1,i,j,'L')
          if(test == True):
            found_next = True
            found_last = add_coordinates(rec_i+1,rec_j+1,lat,lon,'U')
            rec_i = rec_i+1
            rec_j = rec_j+1
            direct = "up"
      if(found_last == False and found_next == False):
        # test right
        if((rec_i+1,rec_j) in list(zip(i,j))):
          test = test_side(rec_i+1,rec_j,i,j,'U')
          if(test == True):
            found_next = True
            found_last = add_coordinates(rec_i+1,rec_j,lat,lon,'R')
            rec_i = rec_i+1
            direct = "right"
      if(found_last == False and found_next == False):
        # test down                                                                                                                                                                                        
        if((rec_i,rec_j) in list(zip(i,j))):
          test = test_side(rec_i,rec_j,i,j,'R')
          if(test == True):
            found_next = True
            found_last = add_coordinates(rec_i,rec_j,lat,lon,'D')
            rec_j = rec_j
            direct = "down"
  return lat_poly, lon_poly, lat_inside, lon_inside


    
    

  
## test connected component labeling
#import numpy as np
#import matplotlib as mpl
#import matplotlib.pyplot as plt

#nx = 5
#ny = 5
#r = np.random.randint(0, 2, size=(nx, ny))
#plt.plot([0],[0])
#plt.xlim(0,nx)
#plt.ylim(0,ny)
#for i in range(0, nx):
#  x1= i
#  x2 = i+1
#  for j in range(0, ny):
#    y1 = j
#    y2 = j+1
#    if(r[i,j]==0):
#     plt.fill([x1,x2,x2,x1,x1],[y1,y1,y2,y2,y1],color='black')
#plt.gca().set_aspect('equal', adjustable='box')
#plt.show() 
#d = connected_component_labeling(r)
#cmap = mpl.cm.get_cmap('jet')
#plt.plot([0],[0])
#plt.xlim(0,nx)
#plt.ylim(0,ny)
#for i in range(0, nx):
#  x1= i
#  x2 = i+1
#  for j in range(0, ny):
#    y1 = j
#    y2 = j+1
#    if(d[i,j]==0):
#      plt.fill([x1,x2,x2,x1,x1],[y1,y1,y2,y2,y1],color='black')
#    else:
#      if(np.max(d) > 1):
#        ratio = (d[i,j] - 1)/(np.max(d)-1)
#      else:
#        ratio = 0.0
#      col= cmap(ratio)
#      plt.fill([x1,x2,x2,x1,x1],[y1,y1,y2,y2,y1],color=col)
#plt.gca().set_aspect('equal', adjustable='box')
#plt.show()
