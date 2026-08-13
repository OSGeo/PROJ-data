#!/bin/bash -xe

# Usage:
# PROJ_DATA_DIR=/path/to/PROJ-data ./build_geoid2021.sh

input=Gravimetric_QGeoidCOL2023.txt
output=co_igac_QGeoidCOL2023.tif

# Setup build directory
mkdir -p build


# Remove first line, letting default lon lat z
tail -n +2 $input > ./build/$input

docker run --user $(id -u):$(id -g) --workdir $PWD \
            --rm -v /home:/home ghcr.io/osgeo/gdal:alpine-normal-latest \
            sh -c " \
            # Call vertoffset_grid_to_gtiff-script 
            python3 ${PROJ_DATA_DIR}/grid_tools/vertoffset_grid_to_gtiff.py \
            --type GEOGRAPHIC_TO_VERTICAL \
            --parameter-name geoid_undulation \
            --source-crs \"EPSG:20045\" \
            --target-crs \"EPSG:11513\" \
            --description \"MAGNA-SIRGAS 2018 (EPSG:20045) to COLGVD2023 height (EPSG:11513). Converted from $input\" \
            --area-of-use \"Colombia - mainland\" \
            --copyright \"Derived from work by IGAC. CC-BY-4.0 https://creativecommons.org/licenses/by/4.0/\" \
            ./build/$input ./$output && \
            # Run check_gtiff_grid-script
            python3 ${PROJ_DATA_DIR}/grid_tools/check_gtiff_grid.py ./$output \
            # Show info
            gdalinfo ./$output "

# Remove build directory
rm -rf build
