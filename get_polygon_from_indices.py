def get_polygon_from_indices(i, j):
  import numpy as np

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

  def add_coordinates(ii, jj, dd):
    # checks if coordinates can be added or if we are already closing the polygon
    # then 'found_last' will be set to 'True'
    # following variables are assumed to be 'global': lat, lon, d_lat, d_lon, eps,
    # lat_poly, lon_poly
    if(dd == 'L'):
      fi = -0.5
      fj = -0.5
    if(dd == 'U'):
      fi = -0.5
      fj = +0.5
    if(dd == 'R'):
      fi = +0.5
      fj = +0.5
    if(dd == 'D'):
      fi = +0.5
      fj = -0.5
    temp_i = ii + fi
    temp_j = jj + fj
    if((abs(temp_i - i_poly[0]) < eps) and (abs(temp_j - j_poly[0]) < eps)):
      found_last = True
    else:
      i_poly.append(temp_i)
      j_poly.append(temp_j)
      found_last = False
    return found_last   

  i_poly = []
  j_poly = []
  found_edge = False
  k = 0
  while(found_edge == False):
    rec_i = i[k]
    rec_j = j[k]
    found = test_side(rec_i, rec_j, i, j, "L") 
    if(found == True):
      found_edge = True
    else:  
      k = k + 1
  # to do: add coordinates to list
  poly_i_inside = rec_i
  poly_j_inside = rec_j
  i_poly.append(rec_i - 0.5)
  j_poly.append(rec_j - 0.5)
  i_poly.append(rec_i - 0.5)
  j_poly.append(rec_j + 0.5)
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
            found_last = add_coordinates(rec_i-1,rec_j+1, 'L')
            rec_i = rec_i-1
            rec_j = rec_j+1
            direct = "left"
      if(found_last == False and found_next == False):
        # test up
        if((rec_i,rec_j+1) in list(zip(i,j))):
          test = test_side(rec_i-1,rec_j+1,i,j,'L')
          if(test == True):
            found_next = True
            found_last = add_coordinates(rec_i,rec_j+1,'U')
            rec_i = rec_i 
            rec_j = rec_j+1
            direct = "up"
      if(found_last == False and found_next == False):
        # test right
        if((rec_i,rec_j) in list(zip(i,j))):
          test = test_side(rec_i,rec_j,i,j,'T')
          if(test == True):
            found_next = True
            found_last = add_coordinates(rec_i,rec_j,'R')
            rec_i = rec_i
            rec_j = rec_j
            direct = "right"
    if(direct == 'left'):
      found_next = False
      # test down 
      if(found_last == False and found_next == False):
        if((rec_i-1,rec_j-1) in list(zip(i,j))):
          test = test_side(rec_i-1,rec_j-1,i,j,'B')
          if(test == True):
            found_next = True
            found_last = add_coordinates(rec_i-1,rec_j-1,'D')
            rec_i = rec_i-1
            rec_j = rec_j-1
            direct = "down"
      if(found_last == False and found_next == False):
        # test left
      	if((rec_i-1,rec_j) in list(zip(i,j))):
          test = test_side(rec_i-1,rec_j,i,j,'B')
          if(test == True):
            found_next = True
            found_last = add_coordinates(rec_i-1,rec_j,'L')
            rec_i = rec_i-1
            rec_j = rec_j
            direct = "left"
      if(found_last == False and found_next == False):
        # test up
        if((rec_i,rec_j+1) in list(zip(i,j))):
          test = test_side(rec_i,rec_j+1,i,j,'L')
          if(test == True):
            found_next = True
            found_last = add_coordinates(rec_i,rec_j+1,'U')
            rec_j = rec_j+1
            direct = "up"
    if(direct == 'down'):
      found_next = False
      # test right
      if(found_last == False and found_next == False):
        if((rec_i+1,rec_j-1) in list(zip(i,j))):
          test = test_side(rec_i+1,rec_j-1,i,j,'U')
          if(test == True):
            found_next = True
            found_last = add_coordinates(rec_i+1,rec_j-1,'R')
            rec_i = rec_i+1
            rec_j = rec_j-1
            direct = "right"
      if(found_last == False and found_next == False):
        # test down
        if((rec_i,rec_j-1) in list(zip(i,j))):
          test = test_side(rec_i,rec_j-1,i,j,'R')
          if(test == True):
            found_next = True
            found_last = add_coordinates(rec_i,rec_j-1,'D')
            rec_j = rec_j-1
            direct = "down"
      if(found_last == False and found_next == False):
        # test left
        if((rec_i,rec_j) in list(zip(i,j))):
          test = test_side(rec_i,rec_j,i,j,'B')
          if(test == True):
            found_next = True
            found_last = add_coordinates(rec_i,rec_j,'L')
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
            found_last = add_coordinates(rec_i+1,rec_j+1,'U')
            rec_i = rec_i+1
            rec_j = rec_j+1
            direct = "up"
      if(found_last == False and found_next == False):
        # test right
        if((rec_i+1,rec_j) in list(zip(i,j))):
          test = test_side(rec_i+1,rec_j,i,j,'U')
          if(test == True):
            found_next = True
            found_last = add_coordinates(rec_i+1,rec_j,'R')
            rec_i = rec_i+1
            direct = "right"
      if(found_last == False and found_next == False):
        # test down                                                                                                                                                                                        
        if((rec_i,rec_j) in list(zip(i,j))):
          test = test_side(rec_i,rec_j,i,j,'R')
          if(test == True):
            found_next = True
            found_last = add_coordinates(rec_i,rec_j,'D')
            rec_j = rec_j
            direct = "down"
  return i_poly, j_poly


#i = [1,2,1]
#j = [1,1,2]
#i_poly, j_poly = get_polygon(i,j)
#print(i_poly)
#print(j_poly)
    

