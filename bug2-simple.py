#-*- coding: UTF-8 -*-

import time
import ephem

line1 = 'ISS (ZARYA)'
line2 = '1 25544U 98067A   08334.54218750  .00025860  00000-0  20055-3 0  7556'
line3 = '2 25544 051.6425 248.8374 0006898 046.3246 303.9711 15.71618375574540594%'

iss = ephem.readtle(line1, line2, line3)

reto = ephem.Observer() 

reto.lat = "47:24:10" 
reto.long = "8:7:40"
reto.elevation = 350

obs = reto
sat = iss

while True:
    obs.date = ephem.now()
    sat.compute(obs)
    
    print("Az, alt (%f, %f), Range: %i km (%f, %f)" % \
        (sat.az, sat.alt, 
        int(sat.range / 1000), 
        sat.sublat, sat.sublong))

    time.sleep(1.0)
