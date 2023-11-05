#import matplotlib.pyplot as plt
#from matplotlib.collections import LineCollection

def multicolored_line(ax, x, y, c, dist_color):
  import math
  # makes a multicoloured line where new colour starts after a certain lenght of the line
  # input is an array with x and y (coordinates)
  # c: array with colours (e.g. ['r','b'])
  # d = length of segment in axes coordinates coordinates

  def distance(x1,y1,x2,y2):
    dx = x2 - x1
    dy = y2 - y1
    res = math.sqrt(dx**2 + dy**2)
    return res
    
  lines = []
  colours = []
  ic = 0

  rest_dist_color = 0
  xp = []
  yp = []
  for i in range(0, len(x)):
    xyp = ax.transData.transform((x[i],y[i]))
    xp.append(xyp[0])
    yp.append(xyp[1])
    
  i = 0
  rec_xp = xp[i]
  rec_yp= yp[i]
  
  dist_left = distance(rec_xp,rec_yp,xp[len(xp)-1],yp[len(yp)-1])
  while(dist_left > 0.000001):
    dist_next_point = distance(rec_xp,rec_yp,xp[i+1],yp[i+1])
    if(rest_dist_color == 0):
      if(dist_next_point <= dist_color): # full segment plotted, no change of color needed
        rec_xy = ax.transData.inverted().transform((rec_xp,rec_yp))
        rec_x = rec_xy[0]
        rec_y = rec_xy[1]
        lines.append([(rec_x,rec_y),(x[i+1],y[i+1])])
        colours.append(c[ic])
        rest_dist_color = dist_color - dist_next_point
        rec_xp = xp[i+1]
        rec_yp = yp[i+1]
        i = i + 1
      else: # d < dist # only part of segment is plotted now -> change of color for rest of segment is needed 
        q = dist_color / dist_next_point
        dx = xp[i+1] - rec_xp
        dy = yp[i+1] - rec_yp
        rec_xp2 = rec_xp + q * dx
        rec_yp2 = rec_yp + q * dy
        rec_xy = ax.transData.inverted().transform((rec_xp,rec_yp))
        rec_x =	rec_xy[0]
        rec_y =	rec_xy[1]
        rec_xy2 = ax.transData.inverted().transform((rec_xp2,rec_yp2))
        rec_x2 = rec_xy2[0]
        rec_y2 = rec_xy2[1]
        lines.append([(rec_x,rec_y),(rec_x2,rec_y2)])
        colours.append(c[ic])
        rest_dist_color = 0
        rec_xp = rec_xp2
        rec_yp = rec_yp2
        ic = ic + 1
        if(ic == len(c)):
          ic = 0
    else: # rest_dist > 0
      if(rest_dist_color >= dist_next_point):
        rec_xy = ax.transData.inverted().transform((rec_xp,rec_yp))
        rec_x = rec_xy[0]
        rec_y = rec_xy[1]
        lines.append([(rec_x,rec_y),(x[i+1],y[i+1])])
        colours.append(c[ic])
        rest_dist_color = rest_dist_color - dist_next_point
        rec_xp = xp[i+1]
        rec_yp = yp[i+1]
        i = i +	1
      else: # rest_dist < dist
        q = rest_dist_color / dist_next_point
        dx = xp[i+1] - rec_xp
        dy = yp[i+1] - rec_yp
        rec_xp2 = rec_xp + q * dx
        rec_yp2 = rec_yp + q * dy
        rec_xy = ax.transData.inverted().transform((rec_xp,rec_yp))
        rec_x = rec_xy[0]
        rec_y = rec_xy[1]
        rec_xy2 = ax.transData.inverted().transform((rec_xp2,rec_yp2))
        rec_x2 = rec_xy2[0]
        rec_y2 = rec_xy2[1]
        lines.append([(rec_x,rec_y),(rec_x2,rec_y2)])
        colours.append(c[ic])
        ic = ic + 1
        if(ic == len(c)):
          ic = 0
        rest_dist_color = 0
        rec_xp = rec_xp2
        rec_yp = rec_yp2
    dist_left = distance(rec_xp,rec_yp,xp[len(x)-1],yp[len(y)-1])
    
  return lines, colours

#import matplotlib.pyplot as plt
#from matplotlib.collections import LineCollection

#x = [0, 2, 5, 6, 8, 12]
#y = [4, 2, 6, 9, 12, 6]
#y = [i * 100 for i in y]

#c = ['r','b']
#d = 100

#fig = plt.figure()
#ax = fig.add_subplot(111)
#ax.plot([], [], color='k')
#plt.xlim([-0.5,12.5])
#plt.ylim([0,1300])
#lines, colours = multicolored_line(ax, x, y, c, d)
#line_segments = LineCollection(lines, colors=colours)
#line_segments.set_linewidth(3.0)
#plt.gca().add_collection(line_segments)

#plt.show()

