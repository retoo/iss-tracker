import criteria 
import itertools, ephem, sys, time, tracker
from utils import rad2deg, localtime

        
def calc_alt_func(obj, observer):
    def calculator(date):
        observer.date = date
        obj.compute(observer)
        return obj.alt

    return calculator
# 
# def above_horizon(iter):
#     for obj in iter:
#         if obj.alt > 0:
#             yield (obj)
#         

# 
# for obj in above_horizon(sat_stepper(r, iss, ephem.date("2008/11/18 16:35:34"))):
#     print r.date, obj.az, obj.alt, iss.range / 1000, displa_coord(iss.sublat, iss.sublong)
#     
#     f = calc_alt(obj, r)
#     print f(ephem.date(rising))
#     break
    
    

def risings(observer, obj, start_date = ephem.now(), end_date = None):
    alt_func = calc_alt_func(obj, observer)
    stepper = tracker.sat_stepper(observer, obj, start_date, end_date)
    
    # keep going until the sat has set (we ignore risings which already happened before the func got initialized)
    for date, obj in stepper:

        if obj.alt < 0:
            break
        print date, "wait for the sat to set", obj.alt 
    
    prev = None
    risen = False
    rise_date = set_date = None
    # step through the different steps and always look at two consecutive ones
    for date, obj in stepper:
        if prev != None:
            if risen:
                if obj.alt < 0:
                    set_date = ephem.date(ephem.newton(alt_func, prev, date))
                    risen = False
                    #print date, "set at ", set_date
                    
                    if set_date - rise_date > 60.0 / 86400:
                        yield rise_date, set_date
                    else:
                        # ignore
                        pass
                else:
                    pass
                    #print date, "still above horizon", obj.alt
            else:
                if obj.alt >= 0:
                    rise_date = ephem.date(ephem.newton(alt_func, prev, date))
                    risen = True
                    #print date, "rise at", rise_date
                else:
                    pass
                    #print date, "still below", obj.alt
            
        prev = date        




class Pass(object):
    shadow_crit = criteria.Criteria("in Shadow", 60, 10)
    max_alt_crit = criteria.Criteria("Max Alt", 10, 70)
    max_sun_alt_crit = criteria.Criteria("Max Alt Sun", 4, -5)
    
    def __init__(self, obj, observer, start, end):
        self.obj = obj
        self.observer = observer
        self.start = start
        self.end = end
        self.duration = (end * 86400 - start * 86400)

        self.evaluate()
        
    def evaluate(self):
        self.max_alt = 0 
        self.max_sun_alt = -2**30
        self.min_range = 2**30
        self.eclipsed  = 0
        self.measure_points = 0
        for date, obj in tracker.sat_stepper(self.observer, self.obj, self.start, self.end, 10.0 / 86400):
            sun.compute(self.observer)

            self.measure_points += 1
            
            if obj.eclipsed: 
                self.eclipsed += 1
            
            if obj.alt > self.max_alt:
                self.max_alt = obj.alt 
            if sun.alt > self.max_sun_alt:
                self.max_sun_alt = sun.alt
            if obj.range < self.min_range:
                self.min_range = obj.range 
            
        self.shadow_ratio = self.eclipsed * 100 / self.measure_points
        
        total = criteria.Score()
        
        total.add(Pass.shadow_crit, self.shadow_ratio)
        total.add(Pass.max_alt_crit, rad2deg(self.max_alt))
        total.add(Pass.max_sun_alt_crit, rad2deg(self.max_sun_alt))

        self.score = total.score()
    
    def shadow_ratio(self):
        return 

if __name__ == '__main__':
    from data import reto, iss
    sun = ephem.Sun()
    
    observer = reto
    sat = iss
           
    for start, end in risings(observer, sat, ephem.now(), ephem.now() + 14):
        p = Pass(sat, observer, start, end)
    
        if p.score > 70:
            start = localtime(p.start)
            end = localtime(p.end)
            print "%s - %s: sh=%i alt=%i sun=%i score=%i%%" % \
                (start.strftime("%Y-%m-%d %H:%M:%S"), end.strftime("%H:%M:%S"), \
                p.shadow_ratio, rad2deg(p.max_alt), rad2deg(p.max_sun_alt), p.score)
