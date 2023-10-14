#!/bin/bash -e

# Usage:
# PROJ_DATA_DIR=/path/to/PROJ-data ./build_GCG2016.sh [path/to/GCG2016.txt]

# Setup build directory
mkdir -p build

src="${1:-GCG2016.txt}"
dst="de_bkg_gcg2016.tif"
# Copy input file into build directory
cp $src ./build/GCG2016.txt

# Add header
sed -i '1i\y x z' ./build/GCG2016.txt

docker run  --pull=always --user $(id -u):$(id -g) --workdir $PWD \
            --rm -v /home:/home ghcr.io/osgeo/gdal:alpine-normal-latest \
            sh -c " \
            # Convert to GeoTIFF
            gdal_translate -a_nodata 999999 ./build/GCG2016.txt ./build/temp.tif && \
            # Set nodata to -32768
            gdalwarp -srcnodata 999999 -dstnodata -32768 ./build/temp.tif ./build/temp_nodata_corrected.tif && \
            # Call vertoffset_grid_to_gtiff-script
            python3 ${PROJ_DATA_DIR}/grid_tools/vertoffset_grid_to_gtiff.py \
            --type GEOGRAPHIC_TO_VERTICAL \
            --parameter-name geoid_undulation \
            --source-crs \"EPSG:10283\" \
            --target-crs \"EPSG:7837\" \
            --description \"ETRS89/DREF91/2016 (EPSG:10283) to DHHN2016 height (EPSG:7837). Converted from GCG2016.txt\" \
            --area-of-use \"Germany\" \
            --copyright \"Derived from work by BKG. CC-BY-4.0 https://creativecommons.org/licenses/by/4.0/\" \
            ./build/temp_nodata_corrected.tif ./$dst && \
            # Run check_gtiff_grid-script
            python3 ${PROJ_DATA_DIR}/grid_tools/check_gtiff_grid.py ./$dst \
            # Show info
            gdalinfo ./$dst "

# Remove build directory
rm -rf build
