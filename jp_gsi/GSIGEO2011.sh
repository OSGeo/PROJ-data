#!/bin/bash

SCRIPT="
import sys

south, west, north, east = map(float, sys.argv[1:5])

lines = sys.stdin.read().split('\n')

metadata = lines[0].strip().split()[0:6]
min_lat, min_lon, d_lat, d_lon = map(float, metadata[0:4])
nrows, ncols = map(int, metadata[4:6])

data = []
row = []
for line in lines[1:]:
    line = line.strip()
    if len(line) == 0:
       continue
    row += [v for v in map(float, line.split())]
    if len(row) == ncols:
        data.append(row)
        row = []
assert(len(data) == nrows)

for i, row in enumerate(data):

    lat = min_lat + d_lat * i

    if lat + d_lat < south or lat - d_lat > north:
        continue

    for j, value in enumerate(row):
        lon = min_lon + d_lon * j

        if lon + d_lon < west or lon - d_lon > east:
            continue

        print('%.12f %.12f %.12f' % (lon, lat, value))
"

SCRIPT_PATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

if [ "$#" -lt 1 ]; then
	echo "Usage: $(basename $0) source_file.txt"
	exit 1
fi

SOURCE_FILE=$1

RES_LAT=0.0166666666667
RES_LONG=0.0250

NO_DATA_VALUE="999.0000"

function generate_grid
{
    TARGET_FILE=$1
    SOUTH=${2:--90}
    WEST=${3:--180}
    NORTH=${4:-90}
    EAST=${5:-180}

    cat $SOURCE_FILE |
    python -c "$SCRIPT" $SOUTH $WEST $NORTH $EAST > input

    gdal_translate -mo "AREA_OR_POINT=Point" -r nearest -strict -a_nodata ${NO_DATA_VALUE} \
                   -tr ${RES_LONG} ${RES_LAT} -a_srs EPSG:6667 input ${TARGET_FILE}
    rm input
}

# Grid file for JGD2011 (vertical) height, Japan - onshore mainland, extended bounding box 20, 120, 50, 150
generate_grid jp_gsi_gsigeo2011_tmp.tif

gdalwarp jp_gsi_gsigeo2011_tmp.tif jp_gsi_gsigeo2011.tif -overwrite -tr $RES_LONG $RES_LAT
rm jp_gsi_gsigeo2011_tmp.tif

# Add metadata with grid_tools of PROJ-data repository
$SCRIPT_PATH/../grid_tools/vertoffset_grid_to_gtiff.py \
 --description "JDG2011 (EPSG:6667) to JGD2011 (vertical) height (EPSG:6695). Converted from gsigeo2011_ver2_1.asc" \
 --type "GEOGRAPHIC_TO_VERTICAL" \
 --copyright "Derived from work by the Geospatial Information Authority of Japan. CC-BY 4.0" \
 --area-of-use "Japan - onshore mainland" \
 --source-crs "EPSG:6667" \
 --target-crs "EPSG:6695" \
 jp_gsi_gsigeo2011.tif jp_gsi_gsigeo2011.tif

