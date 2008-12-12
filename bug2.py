#-*- coding: UTF-8 -*-

import time
import ephem

def format(str):

    str = str.replace(":", "°", 1). \
              replace(":", "'", 1). \
              replace(":", '"', 1)
    
    return str

def displa_coord(lat, long):
    x  = format(str(lat) + ": N" if lat >= 0 else str(-lat) + ": S")
    x += ", " 
    x += format(str(long) + ": E" if long >= 0 else str(-long) + ": W")
    return x

def rad2deg(rad):
    return rad * 360 / (2*ephem.pi)


line1 = 'ISS (ZARYA)'
line2 = '1 25544U 98067A   08334.54218750  .00025860  00000-0  20055-3 0  7556'
line3 = '2 25544 051.6425 248.8374 0006898 046.3246 303.9711 15.71618375574540594'

iss = ephem.readtle(line1, line2, line3)

reto = ephem.Observer() 

reto.lat = "47:24:10" 
reto.long = "8:7:40"
reto.elevation = 350

obs = reto
sat = iss

obs.date = "2008/12/12 13:13:13"
sat.compute(obs)

print("Az: %f Alt: %f (%f, %f), Range: %i km, %s (%f, %f)" % \
    (rad2deg(sat.az), rad2deg(sat.alt), 
    sat.az, sat.alt, 
    int(sat.range / 1000), 
    displa_coord(sat.sublat, sat.sublong),
    sat.sublat, sat.sublong))

print("date", obs.date, "epoch", obs.epoch, "lat", obs.lat, "long",
      obs.long, "elevation", obs.elevation, "temp", obs.temp, "pressure",
      obs.pressure)

