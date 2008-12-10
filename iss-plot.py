import time, ephem, utils, tracker

from utils import rad2deg


from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

from data import reto, iss

lats = []
longs = []

start = ephem.now()
for date, o in tracker.sat_stepper(reto, iss,  start, start+ 1. /  24):
    lats.append(rad2deg(o.sublat))
    longs.append(rad2deg(o.sublong))



# set up orthographic map projection with
# perspective of satellite looking down at 50N, 100W.
# use low resolution coastlines.
# don't plot features that are smaller than 1000 square km.
map = Basemap(projection='robin',lat_0=50,lon_0=-100,
              resolution='l',area_thresh=1000.)
# draw coastlines, country boundaries, fill continents.
map.drawcoastlines()
map.drawcountries()
map.fillcontinents(color='coral')
# draw the edge of the map projection region (the projection limb)
map.drawmapboundary()
# draw lat/lon grid lines every 30 degrees.
map.drawmeridians(np.arange(0,360,30))
map.drawparallels(np.arange(-90,90,30))


# compute native map projection coordinates of lat/lon grid.
x, y = map(longs, lats)
# contour data over the map.
CS = map.plot(x, y)

plt.show()