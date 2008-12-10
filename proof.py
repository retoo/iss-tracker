import itertools
import ephem

def chunk(iterable, size, pad=None):
    """
    iterates over chunks of entries from an iterable. if necessary 
    entries are padded using the supploed pad
    
    Copied from somewhere in the internet
    """
    iterator = iter(iterable)
    padding = [pad]
    while True:
        chunk = list(itertools.islice(iterator, size))
        if chunk:
            yield chunk + (padding*(size-len(chunk)))
        else:
            break

# line1 = "ISS (ZARYA)"
# line2 = "1 25544U 98067A   08334.54218750  .00025860  00000-0  20055-3 0  7556"
# line3 = "2 25544 051.6425 248.8374 0006898 046.3246 303.9711 15.71618375574540594"
line1 = 'ISS (ZARYA)             \n'
line2 = '1 25544U 98067A   08334.54218750  .00025860  00000-0  20055-3 0  7556\n'
line3 = '2 25544 051.6425 248.8374 0006898 046.3246 303.9711 15.71618375574540594'
print("load")
ephem.readtle(line1, line2, line3)
print("load finished")
filename = "sts.txt"

for a, b, c in chunk(open(filename), 3):
    name = a.strip()
    print(repr(a), repr(b), repr(c))

    #d[name] = 
    ephem.readtle(line1, line2, line3)
    


