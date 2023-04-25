#import matplotlib.pyplot as plt
#from matplotlib.collections import LineCollection

def multicolored_line(x, y, c, d):
  import math
  # makes a multicoloured line where new colour starts after a certain lenght of the line
  # input is an array with x and y (coordinates)
  # c: array with colours (e.g. ['r','b'])
  # d = length of segment in data coordinates

  def distance(x1,y1,x2,y2):
    dx = x2 - x1
    dy = y2 - y1
    res = math.sqrt(dx**2 + dy**2)
    return res
    
  lines = []
  colours = []
  ic = 0
  i = 0
  rest_dist = 0
  rec_x = x[i]
  rec_y = y[i]
  dist_test = distance(rec_x,rec_y,x[len(x)-1],y[len(y)-1])
  while(dist_test > 0.000001):
    dist = distance(rec_x,rec_y,x[i+1],y[i+1])
    if(rest_dist == 0):
      if(dist <= d):
        lines.append([(rec_x,rec_y),(x[i+1],y[i+1])])
        colours.append(c[ic])
        rest_dist = d - dist
        rec_x = x[i+1]
        rec_y = y[i+1]
        i = i + 1
      else: # d < dist
        q = d / dist
        dx = x[i+1] - rec_x
        dy = y[i+1] - rec_y
        rec_x2 = rec_x + q * dx
        rec_y2 = rec_y + q * dy
        lines.append([(rec_x,rec_y),(rec_x2,rec_y2)])
        colours.append(c[ic])
        ic = ic + 1
        if(ic == len(c)):
          ic = 0
        rest_dist = 0
        rec_x = rec_x2
        rec_y = rec_y2
    else: # rest_dist > 0
      if(rest_dist >= dist):
        lines.append([(rec_x,rec_y),(x[i+1],y[i+1])])
        colours.append(c[ic])
        rest_dist = rest_dist - dist
        rec_x = x[i+1]
        rec_y = y[i+1]
        i = i +	1
      else: # rest_dist < dist
        q = rest_dist /	dist
        dx = x[i+1] - rec_x
        dy = y[i+1] - rec_y
        rec_x2 = rec_x + q * dx
        rec_y2 = rec_y + q * dy
        lines.append([(rec_x,rec_y),(rec_x2,rec_y2)])
        colours.append(c[ic])
        ic = ic + 1
        if(ic == len(c)):
          ic = 0
        rest_dist = 0
        rec_x = rec_x2
        rec_y = rec_y2
    dist_test = distance(rec_x,rec_y,x[len(x)-1],y[len(y)-1])
    
  return lines, colours

#x = [0, 2, 5, 6, 8, 12]
#y = [4, 2, 6, 9, 12, 6]

#c = ['r','b']
#d = 1
#lines, colours = multicolored_line(x, y, c, d)

#plt.plot(x, y, color='k')
#line_segments = LineCollection(lines, colors=colours)
#line_segments.set_linewidth(3)
#plt.gca().add_collection(line_segments)

#plt.show()

