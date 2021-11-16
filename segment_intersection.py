import numpy as np
import matplotlib.pyplot as plt

f = np.random.uniform(size=(250,1))
g = np.random.uniform(size=(250,1))


## TO REMOVE COLINEAR ASSUMPTION 
## TODO: Just remove colinear lines before processing, then add the intersections they have with other points in post-processing 


## TO REMOVE SAME X-COORDINATE 
from poly_point_isect import isect_segments, isect_segments_include_segments

F = np.c_[np.repeat(0.0, len(f)), f]
G = np.c_[np.repeat(1.0, len(g)), g]


F = [(0.0, 0.0), (0.0, 1e-6), (0.0, 1e-6), (0.0, 0.1), (0.0, 0.1)]
G = [(1.0, 1e-6), (1.0, 0.0), (1.0, 0.0), (0.0, 0.1), (0.0, 0.1)]

S = isect_segments([(tuple(p), tuple(q)) for p,q in zip(F, G)], validate=True)

## This one might work
S = isect_segments_include_segments([(tuple(p), tuple(q)) for p,q in zip(F, G)], validate=True)


import shapely
from shapely.geometry import Point, LineString, MultiLineString
lines = [LineString([Point(*p), Point(*q)]) for p,q in zip(F, G)]

M = MultiLineString([(p,q)for p,q in zip(F, G)])
wut = M.intersection(M)

