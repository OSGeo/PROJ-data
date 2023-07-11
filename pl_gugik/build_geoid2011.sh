#!/bin/bash

# Usage:
# PROJ_DATA_DIR=/path/to/PROJ-data ./build_geoid2011.sh gugik-geoid2011-PL-EVRF2007-NH.txt EPSG:9651 "EVRF2007-PL height" pl_gugik_geoid2011-PL-EVRF2007-NH.tif
# PROJ_DATA_DIR=/path/to/PROJ-data ./build_geoid2011.sh gugik-geoid2011-PL-KRON86-NH.txt EPSG:9650 "Baltic 1986 height" pl_gugik_geoid2011-PL-KRON86-NH.tif

# Setup build directory
mkdir build

# Copy input file into build directory
cp $1 ./build/$1

# Clean input file
sed -i '/^[^0-9]/d' ./build/$1

# Add header
sed -i '1i\y x z' ./build/$1

docker run --user $(id -u):$(id -g) --workdir $PWD \
            --rm -v /home:/home osgeo/gdal:alpine-normal-latest \
            sh -c " \
            # Convert to GeoTIFF
            gdal_translate -a_nodata 0 ./build/$1 ./build/temp.tif && \
            # Set nodata to -32768
            gdalwarp -srcnodata 0 -dstnodata -32768 ./build/temp.tif ./build/temp_nodata_corrected.tif && \
            # Call vertoffset_grid_to_gtiff-script 
            python3 ${PROJ_DATA_DIR}/grid_tools/vertoffset_grid_to_gtiff.py \
            --type GEOGRAPHIC_TO_VERTICAL \
            --source-crs \"EPSG:9701\" \
            --target-crs $2 \
            --description \"ETRF2000-PL (EPSG:9701) to $3 ($2). Converted from $1\" \
            --area-of-use \"Poland - onshore\" \
            --copyright \"Derived from work by GUGiK. CC-BY-4.0 https://creativecommons.org/licenses/by/4.0/\" \
            ./build/temp_nodata_corrected.tif ./$4 && \
            # Show info
            gdalinfo ./$4 "

# Remove build directory
rm -rf build
