#!/usr/bin/env python

import math
import os
import sys
import subprocess

os.environ['PROJ_LIB'] = os.path.realpath(
    os.path.dirname(__file__)) + ':' + os.environ['PROJ_LIB']

coords = [[34.290, 135.630],
          [36.103, 140.087],
          [43.217, 143.129],
          [38.675, 139.886],
          [36.344, 137.654],
          [33.179, 130.063],
          [39.801, 141.322]]
refs = [39.8601, 40.1817, 30.6389, 40.1281, 42.8956, 32.3036, 41.8862]

geoid_heights = []
for lat, lon in coords:
    output = subprocess.run(
        'echo %f %f 0 | cs2cs EPSG:6667 EPSG:6668+6695 -f "%%.6f"' % (lat, lon),
        encoding='ASCII', stdout=subprocess.PIPE, shell=True).stdout
    geoid_heights.append(-float(output.split()[2]))

print("    Lat     Lon      geoid h (m) reference error (mm)")
for latlon, height, ref in zip(coords, geoid_heights, refs):
    print("    %.03f  %.03f  %.06f   %.04f   %0.03f" % (
        latlon[0], latlon[1], height, ref, (height - ref) * 1000.0))

def rms(xs, ys):
    accum = 0.0
    for x, y in zip(xs, ys):
        accum += (x - y) ** 2.0
    return math.sqrt(accum)

print("RMS = %.03f mm" % (rms(refs, geoid_heights) * 1000.0))
