#!/bin/bash

# Usage:
# PROJ_DATA_DIR=/path/to/PROJ-data ./build_hBG18.sh hBG18.dat be_ign_hBG18.tif

# Setup build directory
mkdir build

# Copy input file into build directory
cp $1 ./build/$1

# Add header
sed -i '1i\y x z' ./build/$1

docker run --user $(id -u):$(id -g) --workdir $PWD \
            --rm -v /home:/home osgeo/gdal:alpine-normal-latest \
            sh -c " \
            # Show info input
            gdalinfo ./build/$1 \
            # Query input with some sample coordinates
            echo $'2 49\n4 49\n6 49\n2 50\n4 50\n6 50\n2 52\n4 52\n6 52' | gdallocationinfo -geoloc -valonly ./build/$1 \
            # Run gdalwarp to avoid warning about south-up image
            gdalwarp ./build/$1 ./build/temp.tif -overwrite -tr 0.015 0.010 -te 0.9925 48.495 7.0075 52.505 \
            # Call vertoffset_grid_to_gtiff-script 
            python3 ${PROJ_DATA_DIR}/grid_tools/vertoffset_grid_to_gtiff.py \
            --type GEOGRAPHIC_TO_VERTICAL \
            --source-crs \"EPSG:4937\" \
            --target-crs \"EPSG:5710\" \
            --description \"ETRS89 (EPSG:4937) to Ostend height (EPSG:5710). Converted from hBG18.dat\" \
            --area-of-use \"Belgium - onshore\" \
            --copyright \"Derived from work by IGN. CC-BY-4.0 https://creativecommons.org/licenses/by/4.0/\" \
            ./build/temp.tif ./$2 && \
            # Show info output
            gdalinfo ./$2 \
            # Query output with some sample coordinates
            echo $'2 49\n4 49\n6 49\n2 50\n4 50\n6 50\n2 52\n4 52\n6 52' | gdallocationinfo -geoloc -valonly ./$2 \
            # Run validation script
            python3 ${PROJ_DATA_DIR}/grid_tools/check_gtiff_grid.py ./$2 "

# Remove build directory
rm -rf build
