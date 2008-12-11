#!/usr/local/bin/python3.0

import ephem 
def sat_stepper(obs, obj, time = ephem.now(), end = None, step = 1.0 / (24 * 60)):
    obs.date = time
    while end == None or obs.date < end:
        obs.date += step
        obj.compute(obs)
        yield obs.date, obj
