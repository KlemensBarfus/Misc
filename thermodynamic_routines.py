### some thermodynamic routines ####

def calc_dtdp_dry(T,p):
  # not applying mixed-phase model !
  # input is
  # T: temperature [K]
  # p: pressure [hPa]
  # output is:
  # [K/hPa]    
  R0 = 287.058 # gas constant for dry air [J * kg**-1 * K**-1]
  cp0 = specific_heat_dry_air(T)  
  dtdp = (T*R0)/(p*cp0)
  return dtdp
  
def calc_dtdp_wet(T, p, rF):
  # not applying mixed-phase model !
  # input is
  # T: temperature [K]
  # pressure [hPa]
  # rF is liquid mixing ratio <- here 0.0 because of an irreversible process
  # output is:
  # [K/hPa]    
  R0 = 287.058 # gas constant for dry air [J * kg**-1 * K**-1]
  R1 = 461.5   # gas constant for water vapour [J * kg**-1 * K**-1]
  pF1 = saturation_vapour_pressure(T) # hPa
  p0 = p - pF1                        # hPa
  rF1 = calc_rF1(pF1,p0)  # saturation mixing ratio in g/g
  lF1 = latent_heat_gas_to_liquid(T) #J/kg
  LLF1 = pF1 * lF1                   # hPa * (J/kg)
  cp0 = specific_heat_dry_air(T)      # J/(kg*K)
  cp1 = specific_heat_water_vapour(T)  # J/(kg*K)
  cp2 = specific_heat_liquid_water(T)  # J/(kg*K)
  Cp = cp0 + cp1 * rF1 + cp2 * rF  # J/(kg*K)
  v = (rF1 * lF1)/pF1 * (1.0 + (R1/R0)*rF1) * (LLF1/(R1*T**2.0))
  dtdp = ((rF1*R1*T/pF1) * (1.0 + (rF1*lF1/(R0*T))))/(Cp + v)
  return dtdp

def calc_rF1(pF1,p0):  # Frueh and Wirth, Eq. 4
  # input variables:
  # pF1 is saturation vapour pressure [hPa]
  # p0 is partial pressure of dry air [hPa]  
  R0 = 287.058 # gas constant for dry air [J * kg**-1 * K**-1]
  R1 = 461.5   # gas constant for water vapour [J * kg**-1 * K**-1]

  res = (R0 * pF1) / (R1 * p0)
  return res
  
def saturation_vapour_pressure(T,ice=False):
  import numpy as np  
  # calculates the saturation vapour pressure in hPa using the Clausius-Claperon equation
  # incoming variables are
  # T, temperature in [K]
  # keyword ice, indicates if even in case of temperatures lower than 273.15 K es is calculated with
  # respect to liquid water (then ice must not been set)
  # output is in hPa
  # written by K.Barfus 12/2009

  e0 = 0.611 # [kPa]
  T0 = 273.15 # [K]
  Rv = 461.0 # [J K**-1 kg**-1] gas constant for water vapour

  T = np.asarray(T)

  scalar_input = False
  if T.ndim == 0:
    T = T[None]  # Makes x 1D                                                                                                                                                                
    scalar_input = True

  if(ice == True):
    if(T > 273.15):  # water
      L = 2.5 * 10.0**6.0 # J kg**-1
    else:
      L = 2.83 * 10.0**6.0  # J kg**-1
  else:
    L = 2.5 * 10.0**6.0 # J kg**-1

  es = np.copy(T)
  es.fill(0.0)
  index_valid = np.where(T > 0)
  es[index_valid] = e0 * np.exp((L/Rv)*(1.0/T0-1.0/T[index_valid]))
  es = es * 10.0

  if scalar_input:
    return np.squeeze(es)
  return es
  
def latent_heat_gas_to_liquid(T):
  # latent heat of condensation due to Rogers and Yau in J/kg
  # valid for 248.15 K < T < 313.15 K
  # input parameters:
  T  # temperature in [K]
  T_temp = T - 273.15
  latent_heat = 2500.8 - 2.36 * T_temp + 0.0016 * T_temp**2.0 - 0.00006 * T_temp**3.0
  res = latent_heat * 1000.0
  return res
  
  # alternative approach
  # calculates the latent heat of condensation (gas -> liquid) due to
  # Fleagle, R.G. and J.A. Businger, (1980)
  # An Introduction to Atmospheric Physics.  2d ed.  Academic Press, 432 pp.
  # input
  # T in K
  # output in J kg^-1 K^-1
  #t_temp = T - 273.15
  #Lv = (25.00 - 0.02274 * t_temp) * 10.0^5.0
  

def potential_temperature(t,p):
  # calculates the potential temperature
  # input is temperature [K]
  # pressure [hPa] 
  import numpy as np
  
  t = np.asarray(t)
  p = np.asarray(p)

  p0 = 1000.0

  scalar_input = False
  if t.ndim == 0:
    t = t[None]  # Makes x 1D
    scalar_input = True
 
  theta = t * (p0/p)**(2.0/7.0)

  if scalar_input:
    return np.squeeze(theta)
  return theta

def specific_heat_dry_air(T):
  # source is unknown
  # input:: T  ![K]
  # T should be: -40°C < T < 40^C
  # output is in [J kg^-1 C^-1]

  t_temp = T - 273.15
  C_pd = 1005.60 + 0.017211 * t_temp + 0.000392 * t_temp**2.0
  return C_pd

def specific_heat_water_vapour(T):
  # due to
  # Reid, R.C., J.M. Prausnitz, and B.E. Poling (1987)
  # The Properties of Gases and Liquids.  4th ed.  McGraw-Hill, 741 pp.
  # input: T temperature [K]
  # output is in J kg^-1 K^-1
  t_temp = T - 273.15
  c_pv = 1858.0 + 3.820 * 10.0**(-1.0) * t_temp + 4.220 * 10.0**(-4.0) * t_temp**2.0 - \
   1.996 * 10.0**(-7.0) * T**3.0
  return c_pv 
  
def specific_heat_liquid_water(T):
  # input: T  ! temperature [K]
  # output is in J kg^-1 K^-1
  t_temp = T - 273.15
  c_pw =  4217.4 - 3.720283 * t_temp +0.1412855 * t_temp**2.0 - 2.654387 * 10.0**(-3.0) * t_temp**3.0 \
       + 2.093236 * 10.0**(-5.0) * t_temp**(4.0)
  return c_pw 

  
def specific_humidity_from_dewpoint(dewpoint, pressure):
  ## calculate specific humidity from dewpoint temperature and pressure ###
  #  based on Stull: Meteorology for Scientists and Engineers.
  # written by K.Barfus 2/2019
  # input is dewpoint [K]
  # pressure [hPa]
  # returns specific humidity in [g/g]                                                                                                                                                                      

  import numpy as np
  dewpoint = np.asarray(dewpoint)
  pressure = np.asarray(pressure)
  pressure = pressure / 10.0 # hPa -> kPa
  scalar_input = False
  if dewpoint.ndim == 0:
    dewpoint = dewpoint[None]  # Makes x 1D
    scalar_input = True

  epsilon = 0.622 #[g/g]
  T0 = 273.15 #[K]
  e0 = 0.6114 #[kPa]
  Rv_Lv = 1.844 * 10.0**(-4) # [K**-1]
  e = np.exp((dewpoint/T0-1.0)/(dewpoint*Rv_Lv)+np.log(e0))
  specific_humidity = (epsilon*e) / (pressure-e *(1.0-epsilon))
  # The magic happens here

  if scalar_input:
    return np.squeeze(specific_humidity)
  return specific_humidity
  

def dewpoint_from_specific_humidity(spec_hum,p):
  # calculates Dewpoint temperature from specific humidity and pressure
  import numpy as np
  # input is:
  # specific humidity [g/g]
  # pressure [hPa]
  # output is:
  # dewpoint temperature [K] 


  spec_hum = np.asarray(spec_hum)
  p = np.asarray(p)
  p = p / 10.0 # hPa -> kPa

  Rd = 287.058 # gas constant for dry air [J * kg**-1 * K**-1]
  Rv = 461.5   # gas constant for water vapour [J * kg**-1 * K**-1]
  epsilon = Rd/Rv

  scalar_input = False
  if spec_hum.ndim == 0:
    spec_hum = spec_hum[None]
    p = p[None]
    scalar_input = True

  e = (spec_hum * (p + epsilon)) / (epsilon + spec_hum)  # vapor pressure in [kPa] 
  T0 = 273.15 # [K]
  RvLv = 1.844*10**(-4) # [K**-1]
  e0 = 0.6113 # [kPa]
  Td = (1.0/T0 - RvLv * np.log(e/e0))**(-1.0)
  if scalar_input:
    return np.squeeze(Td)
  return Td
  
def relative_humidity_from_specific_humidity(q, p, t):
  # derives vapour pressure from specific humidity 
  # equation derived from Stull: Meteorology for Scientists and Engineers
  # input is: 
  # q: specific humidity [g_water_vapour / g_total]
  # p: pressure in hPa
  # t: temperatue [K]
  # output is relative humidity [%]
  import numpy as np
  from thermodynamic_routines import saturation_vapour_pressure

  q = np.asarray(q)
  p = np.asarray(p)
  t = np.asarray(t)

  epsilon = 0.622 #[g/g]
  scalar_input = False
  if q.ndim == 0:
    q = q[None]
    p = p[None]
    t = t[None]
    scalar_input = True

  es = saturation_vapour_pressure(t)
  qs = (epsilon * es) / (p- es * (1.0-epsilon))
  RH = (q / qs) * 100.0
  RH[RH > 100.0] = 100.0
  if scalar_input:
    return np.squeeze(RH)
  return RH

def specific_humidity_from_relative_humidity(T,Pressure,RH):
  # derives the specific humidity from relative humidity
  # equation derived from Stull: Meteorology for Scientists and Engineers
  # input is:
  # T: temperature in K
  # Pressure: Pressure in hPa
  # RH: relative humidity [%]
  import numpy as np  
  eta = 0.622
  
  T = np.asarray(T)
  Pressure = np.asarray(Pressure)
  RH = np.asarray(RH)
  
  scalar_input = False
  if T.ndim == 0:
    T = T[None]
    Pressure = Pressure[None]
    RH = RH[None]
    scalar_input = True
  
  es = saturation_vapour_pressure(T)
  qs = (eta * es) / (Pressure - es * (1.0 - eta))
  q = (RH / 100.0) * qs
  
  if scalar_input:
    return np.squeeze(q)
  return q
  
def specific_humidity_from_mixing_ratio(r, p):
  # derives specific humidity from mixing ratio
  # equation derived from Stull: Meteorology for Scientists and Engineers
  # input is:
  # r: mixing ratio [g_water_vapour / g_dry]    
  # p: pressure in hPa
  # output is specific humidity in [g/g]
  import numpy as np 
  epsilon = 0.622 #[g/g]

  r = np.asarray(r)
  p = np.asarray(p)

  scalar_input = False
  if r.ndim == 0:
    r = r[None]
    p = p[None]
    scalar_input = True
  
  e = (r*p)/(epsilon+r) 
  q = (epsilon*e)/(p-e*(1.0-epsilon))

  if scalar_input:
    return np.squeeze(q)
  return q

def mixing_ratio_from_specific_humidity(q,p):
  # derives vapour pressure from specific humidity
  # equation derived from Stull: Meteorology for Scientists and Engineers    
  # input is:
  # q: specific humidity [g_water_vapour / g_total]    
  # p: pressure in hPa
  # output is mixing ration in [g/g]
  import numpy as np
  
  q = np.asarray(q)
  p = np.asarray(p)

  scalar_input = False
  if q.ndim == 0:
    q = q[None]
    p = p[None]
    scalar_input = True
  
  e = vapour_pressure_from_specific_humidity(q,p)
  epsilon = 0.622 #[g/g]
  r = (epsilon*e)/(p-e)
  
  if scalar_input:
    return np.squeeze(r)  
  return r

def vapour_pressure_from_specific_humidity(q,p):
  # derives vapour pressure from specific humidity
  # equation derived from Stull: Meteorology for Scientists and Engineers  
  # input is:
  # q: specific humidity [g_water_vapour / g_total]    
  # p: pressure in hPa
  # output is vapour pressure in [hPa]
  import numpy as np
  
  q = np.asarray(q)
  p = np.asarray(p)

  scalar_input = False
  if q.ndim == 0:
    q = q[None]
    p = p[None]
    scalar_input = True
  
  epsilon = 0.622 #[g/g]  
  e = (q*p) / (epsilon - q*(1.0 - epsilon))

  if scalar_input:
    return np.squeeze(e)
  return e

def dewpoint_from_mixing_ratio_and_pres(mr,p):
  # derives dew point temperature from mixing ratio and pressure                                                                                                                                              
  # equation deruved from Stull: Meteorology for Scientists and Engineers (Eq. 5.3 and 5.7)                                                                                                                   
  # input is:
  # mr: mixing ratio [g_water_vapour / g_dry_air]                                                                                                                                           
  # p:  pressure [hPa]                                                                                                                                                                      
  # output is dewpoint temperature in [K]
  import numpy as np

  epsilon = 0.622 #[g/g]                                                                                                                                                                    
  T0 = 273.15 #[K]                                                                                                                                                                          
  RvLv = 1.844*10.0**(-4) # [K**-1]                                                                                                                                                         
  e0 = 0.611 # [kPa]                                                                                                                                                                        

  mr = np.asarray(mr)
  p = np.asarray(p)
  
  scalar_input = False
  if mr.ndim == 0:
    mr = mr[None]
    p = p[None]
    scalar_input = True
  
  vapour_pressure = (mr * p)/(epsilon + mr)
  dewpoint = (1.0/T0 - RvLv * np.log((vapour_pressure(10.0)/e0))**(-1.0) + T0

  if scalar_input:
    return np.squeeze(dewpoint)
  return dewpoint            
                                         
end function

