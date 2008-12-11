#!/usr/bin/python3.0
# -*- coding: utf-8 -*-

import itertools
import unittest
import ephem

localtime = ephem.localtime

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

def rad2deg(rad):
    return rad * 360 / (2*ephem.pi)

def format(str):

    str = str.replace(":", "°", 1)
    str = str.replace(":", "'", 1)
    str = str.replace(":", '"', 1)
    
    return str

def displa_coord(lat, long):
    x  = format(str(lat) + ": N" if lat >= 0 else str(-lat) + ": S")
    x += ", " 
    x += format(str(long) + ": E" if long >= 0 else str(-long) + ": W")
    return x


if __name__ == "__main__":
    class ChunkTest(unittest.TestCase):
        def testNormal(self):
            g = chunk(range(0, 7), 3, 0)
            i = iter(g)
            self.assertEquals(next(i), [0, 1, 2])
            self.assertEquals(next(i), [3, 4, 5])
            self.assertEquals(next(i), [6, 0, 0])


    unittest.main()
