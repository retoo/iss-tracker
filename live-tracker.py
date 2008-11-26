import time, ephem, utils

from data import reto, iss

sat = iss
obs = reto

while True:
    obs.date = ephem.now()
    sat.compute(obs)
    
    print "Az: %f Alt: %f, Range: %i km, %s" % \
        (utils.displa_coord(sat.sublat, sat.sublong)
    break
    time.sleep(1.0 / 20)