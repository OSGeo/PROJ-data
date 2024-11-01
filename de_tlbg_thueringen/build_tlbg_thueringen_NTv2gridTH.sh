#!/bin/bash -e

# https://geoportal.thueringen.de/gdi-th/download-offene-geodaten/ntv2-gittertransformation

# Usage:
# PROJ_DATA_DIR=/path/to/PROJ-data ./build_tlbg_thueringen_NTv2gridTH.sh

orig=de_tlbg_thueringen_NTv2gridTH.gsb
input=$orig
output=de_tlbg_thueringen_NTv2gridTH.tif

docker run --user $(id -u):$(id -g) --workdir $PWD \
            --rm -v /home:/home ghcr.io/osgeo/gdal:alpine-normal-latest \
            sh -c " \
            python3 ${PROJ_DATA_DIR}/grid_tools/ntv2_to_gtiff.py \
            --source-crs \"EPSG:4746\" \
            --target-crs \"EPSG:4258\" \
            --accuracy-unit arc-second \
            --description \"PD/83 (EPSG:4746) to ETRS89 (EPSG:4258). Converted from $orig\" \
            --area-of-use \"Germany - Thuringen\" \
            --copyright \"Derived from work by TLGB Thueringen. CC-BY-4.0 https://creativecommons.org/licenses/by/4.0/\" \
            ./$input ./$output && \
            # Run check_gtiff_grid-script
            python3 ${PROJ_DATA_DIR}/grid_tools/check_gtiff_grid.py ./$output \
            # Show info
            gdalinfo ./$output "
