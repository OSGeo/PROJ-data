#!/bin/bash -e

# Usage:
# PROJ_DATA_DIR=/path/to/PROJ-data ./build_geoid2021.sh

input=Model_quasi-geoidy-PL-geoid2021-PL-EVRF2007-NH.txt
output=pl_gugik_geoid2021-PL-EVRF2007-NH.tif

# Setup build directory
mkdir build

# Copy input file into build directory
cp $input ./build/$input

# Replace first line with a header to swap lat and long
sed -i '1cy x z' ./build/$input

docker run --user $(id -u):$(id -g) --workdir $PWD \
            --rm -v /home:/home ghcr.io/osgeo/gdal:alpine-normal-latest \
            sh -c " \
            # Convert to GeoTIFF
            gdal_translate -a_nodata 0 ./build/$input ./build/temp.tif && \
            # Set nodata to -32768 (this also makes sure that the output is "north-up" instead of "south-up")
            gdalwarp -srcnodata 0 -dstnodata -32768 ./build/temp.tif ./build/temp_nodata_corrected.tif && \
            # Call vertoffset_grid_to_gtiff-script 
            python3 ${PROJ_DATA_DIR}/grid_tools/vertoffset_grid_to_gtiff.py \
            --type GEOGRAPHIC_TO_VERTICAL \
            --parameter-name geoid_undulation \
            --source-crs \"EPSG:9701\" \
            --target-crs \"EPSG:9651\" \
            --description \"ETRF2000-PL (EPSG:9701) to EVRF2007-PL height (EPSG:9651). Converted from $input\" \
            --area-of-use \"Poland - onshore\" \
            --copyright \"Derived from work by GUGiK. CC-BY-4.0 https://creativecommons.org/licenses/by/4.0/\" \
            ./build/temp_nodata_corrected.tif ./$output && \
            # Run check_gtiff_grid-script
            python3 ${PROJ_DATA_DIR}/grid_tools/check_gtiff_grid.py ./$output \
            # Show info
            gdalinfo ./$output "

# Remove build directory
rm -rf build
