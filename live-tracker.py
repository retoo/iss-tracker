import time, ephem, utils

from utils import rad2deg

from data import reto, iss

sat = iss
obs = reto

while True:
    obs.date = ephem.now()
    sat.compute(obs)
    
    print "Az: %f Alt: %f, Range: %i km, %s" % \
        (rad2deg(sat.az), rad2deg(sat.alt), int(sat.range / 1000), utils.displa_coord(sat.sublat, sat.sublong))

    time.sleep(1.0)