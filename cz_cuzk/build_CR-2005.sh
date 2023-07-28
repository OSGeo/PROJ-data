#!/bin/bash -e

# https://geoportal.cuzk.cz/(S(dxlr1cfbjo0sj0my5vzaa22h))/Default.aspx?mode=TextMeta&side=sit.trans&text=souradsystemy
# Download https://geoportal.cuzk.cz/dokumenty/CR2005.GTX.zip

# Usage:
# PROJ_DATA_DIR=/path/to/PROJ-data ./build_CR-2005.sh

orig=CR2005_AAIGrid.asc
input=$orig
output=cz_cuzk_CR-2005.tif

docker run --user $(id -u):$(id -g) --workdir $PWD \
            --rm -v /home:/home ghcr.io/osgeo/gdal:alpine-normal-latest \
            sh -c " \
            # Call vertoffset_grid_to_gtiff-script
            python3 ${PROJ_DATA_DIR}/grid_tools/vertoffset_grid_to_gtiff.py \
            --type GEOGRAPHIC_TO_VERTICAL \
            --parameter-name geoid_undulation \
            --source-crs \"EPSG:4937\" \
            --target-crs \"EPSG:8357\" \
            --description \"ETRS89 (EPSG:4937) to Baltic 1957 height (EPSG:8357). Converted from $orig\" \
            --area-of-use \"Czechia\" \
            --copyright \"Derived from work by ČÚZK Czechia. CC-BY-4.0 https://creativecommons.org/licenses/by/4.0/\" \
            ./$input ./$output && \
            # Run check_gtiff_grid-script
            python3 ${PROJ_DATA_DIR}/grid_tools/check_gtiff_grid.py ./$output \
            # Show info
            gdalinfo ./$output "
