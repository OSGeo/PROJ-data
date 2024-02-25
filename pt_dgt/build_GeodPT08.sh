#!/bin/bash -e

# https://www.dgterritorio.gov.pt/geodesia/modelo-geoide
# Download https://www.dgterritorio.gov.pt/sites/default/files/ficheiros-geodesia/GeodPT08.dat

# Usage:
# PROJ_DATA_DIR=/path/to/PROJ-data ./build_GeodPT08.sh

def_data_dir=$(dirname $0)/..

PROJ_DATA_DIR="${PROJ_DATA_DIR:-$def_data_dir}"

orig=GeodPT08.dat

# Setup build directory
mkdir -p build

tmp=./build/GeodPT08.xyz
sort -s -n -k1,1 -k2,2r "$orig" > $tmp
input=$tmp
output=pt_dgt_GeodPT08.tif

docker run --user $(id -u):$(id -g) --workdir $PWD \
            --rm -v /home:/home ghcr.io/osgeo/gdal:alpine-normal-latest \
            sh -c " \
            # Call vertoffset_grid_to_gtiff-script
            python3 ${PROJ_DATA_DIR}/grid_tools/vertoffset_grid_to_gtiff.py \
            --type GEOGRAPHIC_TO_VERTICAL \
            --parameter-name geoid_undulation \
            --source-crs \"EPSG:4937\" \
            --target-crs \"EPSG:5780\" \
            --description \"ETRS89 (EPSG:4937) to Cascais height (EPSG:5780). Converted from $orig\" \
            --area-of-use \"Portugal - mainland - onshore.\" \
            --copyright \"Derived from work DGT+FCUL. CC-BY-4.0 https://creativecommons.org/licenses/by/4.0/\" \
            ./$input ./$output && \
            # Run check_gtiff_grid-script
            python3 ${PROJ_DATA_DIR}/grid_tools/check_gtiff_grid.py ./$output \
            # Show info
            gdalinfo ./$output "

# Remove build directory
rm -rf build
