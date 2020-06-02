#!/bin/sh

if [ "$#" -lt 2 ]; then
	echo "Usage: $(basename $0) source_file.txt output_file.tif"
	exit 1
fi

SOURCE_FILE=$1
TARGET_FILE=$2

ETRS89_BRITISH_NAT_GRID='PROJCS["ETRS89 / British National Grid",
    GEOGCS["ETRS89",
        DATUM["European_Terrestrial_Reference_System_1989",
            SPHEROID["GRS 1980",6378137,298.257222101,
                AUTHORITY["EPSG","7019"]],
            AUTHORITY["EPSG","6258"]],
        PRIMEM["Greenwich",0,
            AUTHORITY["EPSG","8901"]],
        UNIT["degree",0.0174532925199433,
            AUTHORITY["EPSG","9122"]],
        AUTHORITY["EPSG","4258"]],
    PROJECTION["Transverse_Mercator"],
    PARAMETER["latitude_of_origin",49],
    PARAMETER["central_meridian",-2],
    PARAMETER["scale_factor",0.9996012717],
    PARAMETER["false_easting",400000],
    PARAMETER["false_northing",-100000],
    UNIT["metre",1,
        AUTHORITY["EPSG","9001"]],
    AXIS["Easting",EAST],
    AXIS["Northing",NORTH]]
'
RES_LAT=0.008983192446931791	# RES_NORTHING/(PI*GRS80_RAD/180)
RES_LONG=0.015839681746927323	# RES_LAT/cos(MID_AREA_LAT)
# RMSE = 0.0007570669375634179m
# MAX_ERROR = 0.0019630308326981094m

NO_DATA_VALUE="-32768"

tail -n +2 ${SOURCE_FILE} | awk 'BEGIN {FS=","; OFS=" "} {print $2, $3, $6}' > osgm15_temp


gdalwarp -r bilinear -dstnodata ${NO_DATA_VALUE} -tr ${RES_LONG} ${RES_LAT} -s_srs "${ETRS89_BRITISH_NAT_GRID}" -t_srs EPSG:4937 osgm15_temp osgm15_temp.tif
gdal_translate -mo "AREA_OR_POINT=Point" osgm15_temp.tif ${TARGET_FILE}

rm ./osgm15_temp ./osgm15_temp.tif

# Add metadata with grid_tools of PROJ-data repository
# ./grid_tools/vertoffset_grid_to_gtiff.py \
# --description "ETRS89 (EPSG:4937) to ODN height (EPSG:5701). Converted from OSTN15_OSGM15_DataFile.txt" \
# --type "GEOGRAPHIC_TO_VERTICAL" \
# --copyright "Derived from work by Ordnance Survey. The 2-Clause BSD License https://opensource.org/licenses/bsd-license.php" \
# --area-of-use "Great Britain mainland onshore" \
# --source-crs "EPSG:4937" \
# --target-crs "EPSG:5701" \
# ${TARGET_FILE} uk_os_OSGM15_GB.tif
