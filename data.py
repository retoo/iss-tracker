import ephem, utils

def load_tles(filename):
    d = {}
    for a, b, c in utils.chunk(file(filename), 3):
        name = a.strip()
        d[name] = ephem.readtle(a, b, c)
    return d
        
crafts = load_tles("sts.txt")
iss = crafts["ISS (ZARYA)"]

reto = ephem.Observer() 

reto.lat = "47:24:10" 
reto.long = "8:7:40"
reto.elevation = 350