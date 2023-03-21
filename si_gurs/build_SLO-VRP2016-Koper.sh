#!/bin/bash

# Usage:
# PROJ_DATA_DIR=/path/to/PROJ-data ./build_SLO-VRP2016-Koper.sh SLOVRP2016-Koper.xyz si_gurs_SLO-VRP2016-Koper.tif

# Setup build directory
mkdir build

# Copy input file into build directory
cp $1 ./build/$1

docker run --user $(id -u):$(id -g) --workdir $PWD \
            --rm -v /home:/home osgeo/gdal:alpine-normal-latest \
            sh -c " \
            # Call vertoffset_grid_to_gtiff-script 
            python3 ${PROJ_DATA_DIR}/grid_tools/vertoffset_grid_to_gtiff.py \
            --type GEOGRAPHIC_TO_VERTICAL \
            --source-crs \"EPSG:4883\" \
            --target-crs \"EPSG:8690\" \
            --description \"Slovenia 1996 (EPSG:4883) to SVS2010 height (EPSG:8690). Converted from SLOVRP2016-Koper.xyz\" \
            --area-of-use \"Slovenia - onshore\" \
            --copyright \"Derived from work by GURS. CC-BY-4.0 https://creativecommons.org/licenses/by/4.0/\" \
            ./build/$1 ./$2 && \
            # Show info
            gdalinfo ./$2 "

# Remove build directory
rm -rf build
