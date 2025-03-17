#!/bin/bash -e

# Download https://www.gsi.go.jp/butsuri/data/GSIGEO2024beta.zip

# Usage:
# PROJ_DATA_DIR=/path/to/PROJ-data ./build_GSIGEO2024.sh

def_data_dir=$(dirname $0)/..

PROJ_DATA_DIR="${PROJ_DATA_DIR:-$def_data_dir}"

orig=GSIGEO2024beta.isg
input=$orig

# Setup build directory
mkdir -p build

output=jp_gsi_gsigeo2024.tif

docker run --user $(id -u):$(id -g) --workdir $PWD \
            --rm -v /home:/home ghcr.io/osgeo/gdal:alpine-normal-latest \
            sh -c " \
            # Call vertoffset_grid_to_gtiff-script
            python3 ${PROJ_DATA_DIR}/grid_tools/vertoffset_grid_to_gtiff.py \
            --type GEOGRAPHIC_TO_VERTICAL \
            --parameter-name geoid_undulation \
            --source-crs \"EPSG:6667\" \
            --target-crs \"EPSG:6695\" \
            --description \"JDG2011 (EPSG:6667) to JGD2011 (vertical) height (EPSG:6695). Converted from $orig\" \
            --area-of-use \"Japan.\" \
            --copyright \"Derived from work by the Geospatial Information Authority of Japan.\" \
            ./$input ./$output && \
            # Run check_gtiff_grid-script
            python3 ${PROJ_DATA_DIR}/grid_tools/check_gtiff_grid.py ./$output \
            # Show info
            gdalinfo ./$output "

# Remove build directory
rm -rf build
