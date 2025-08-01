#!/bin/bash

# Usage:
# PROJ_DATA_DIR=/path/to/PROJ-data ./build_SLO-VTP2024.sh SLO-VTP2024.xyz si_gurs_SLO-VTP2024.tif

# Setup build directory
mkdir build

# Copy input file into build directory
cp $1 ./build/$1

docker run --user $(id -u):$(id -g) --workdir $PWD \
            --rm -v /home:/home ghcr.io/osgeo/gdal:alpine-normal-latest \
            sh -c " \
            # Call vertoffset_grid_to_gtiff-script 
            python3 ${PROJ_DATA_DIR}/grid_tools/vertoffset_grid_to_gtiff.py \
            --type VERTICAL_TO_VERTICAL \
            --source-crs \"EPSG:5779\" \
            --target-crs \"EPSG:8690\" \
            --interpolation-crs \"EPSG:4765\" \
            --description \"SVS2000 (Trieste) height to SVS2010 (Koper) height. Converted from SLO-VTP2024.xyz\" \
            --area-of-use \"Slovenia - onshore\" \
            --copyright \"Derived from work by GURS. CC-BY-4.0 https://creativecommons.org/licenses/by/4.0/\" \
            ./build/$1 ./$2 && \
            # Show info
            gdalinfo ./$2 "

# Remove build directory
rm -rf build
