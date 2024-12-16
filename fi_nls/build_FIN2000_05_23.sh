#!/bin/bash -e

# Usage:
# PROJ_DATA_DIR=/path/to/PROJ-data ./build_FIN2000_05_23.sh

# Setup build directory
mkdir -p build
rm -f build/*

run_one () {
    vert_code=$1
    vert_name=$2
    orig=$3
    input=$3.xyz
    output=$4
    echo " lat lon z" > ./build/$input
    sed 's/ 0.000/ nan/g' $orig >> ./build/$input
    docker run --user $(id -u):$(id -g) --workdir $PWD \
            --rm -v /home:/home ghcr.io/osgeo/gdal:ubuntu-full-latest \
            sh -c " \
            # Call vertoffset_grid_to_gtiff-script
            python3 ${PROJ_DATA_DIR}/grid_tools/vertoffset_grid_to_gtiff.py \
            --type GEOGRAPHIC_TO_VERTICAL \
            --parameter-name geoid_undulation \
            --source-crs \"EPSG:10689\" \
            --target-crs \"$vert_code\" \
            --description \"EUREF-FIN (EPSG:10689) to $vert_name ($vert_code). Converted from $orig\" \
            --area-of-use \"Finland\" \
            --copyright \"Derived from work by National Land Survey of Finland. CC-BY-4.0 https://creativecommons.org/licenses/by/4.0/\" \
            ./build/$input ./$output && \
            # Run check_gtiff_grid-script
            python3 ${PROJ_DATA_DIR}/grid_tools/check_gtiff_grid.py ./$output \
            # Show info
            gdalinfo ./$output "
}

run_one "EPSG:3900" "N2000 height" "FIN2023N2000.lst" "fi_nls_fin2023n2000.tif"
run_one "EPSG:3900" "N2000 height" "FIN2005N00.lst" "fi_nls_fin2005n00.tif"
run_one "EPSG:5717" "N60 height" "FIN2000.lst" "fi_nls_fin2000.tif"
# Remove build directory
rm -rf build
