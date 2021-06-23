# converts windspeed and -direction to u and v and vice versa
import numpy as np

def ws_wdir_to_uv(ws,wdir):

  rad = 4.0*np.arctan(1)/180.
  ws = np.asarray(ws)
  wdir = np.asarray(wdir)
  scalar_input = False
  if ws.ndim == 0:
    ws = ws[None]
    wdir = wdir[None]
    scalar_input = True

  u = -wspd*np.sin(rad*wdir)
  v = -wspd*np.cos(rad*wdir)  

  if scalar_input:
    return np.asscalar(u), np.asscalar(v)
  return u, v
    
def uv_to_ws_wdir(u,v):
  u = np.asarray(u)
  v = np.asarray(v)
  scalar_input = False
  if u.ndim == 0:
    u = u[None]
    v = v[None]
    scalar_input = True
  wdir = (270-np.rad2deg(np.arctan2(v,u)))%360
  i_nan = np.where((u == 0.0) & (v == 0.0))
  wdir[i_nan] = np.nan
  ws = np.sqrt(np.square(u)+np.square(v))

  if scalar_input:
    return np.asscalar(wdir), np.asscalar(ws)
  return wdir, ws

## test section - start
#u = np.asarray([0.0,0.0])
#v = np.asarray([-4.0,0.0])
#wdir, ws = uv_to_ws_wdir(u,v)
#print(wdir, ws)
## test section - stop
