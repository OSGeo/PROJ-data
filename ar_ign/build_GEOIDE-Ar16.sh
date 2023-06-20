#!/bin/bash -e 

# Usage:
# PROJ_DATA_DIR=/path/to/PROJ-data ./build.sh 

# Setup build directory
mkdir -p build

# Copy input file into build directory
wget https://dnsg.ign.gob.ar/apps/geoidear/documentos/GEOIDE-Ar16.gri -P ./build/
orig=GEOIDE-Ar16.gri
input=GEOIDE-Ar16.asc
output=ar_ign_GEOIDE-Ar16.tif
awk '/^ .*$/ {print "NCOLS "($4-$3)/$6+1 "\nNROWS "($2-$1)/$5+1 "\nXLLCENTER "$3 "\nYLLCENTER "$1  "\nCELLSIZE "$6} /^-?[0-9].*$/ {print $0}' ./build/$orig > ./build/$input
# produces this header
#NCOLS 1440
#NROWS 2220
#XLLCENTER -76.0000000000
#YLLCENTER -57.0007400000
#CELLSIZE 0.01666700000000000

head ./build/$input

docker run --user $(id -u):$(id -g) --workdir $PWD \
            --rm -v /home:/home osgeo/gdal:alpine-normal-latest \
            sh -c " \
            # Call vertoffset_grid_to_gtiff-script 
            python3 ${PROJ_DATA_DIR}/grid_tools/vertoffset_grid_to_gtiff.py \
            --type GEOGRAPHIC_TO_VERTICAL \
            --parameter-name geoid_undulation \
            --source-crs \"EPSG:5342\" \
            --target-crs \"EPSG:9255\" \
            --description \"POSGAR 2007 (EPSG:5342) to SRVN16 height (EPSG:9255). Converted from $orig\" \
            --area-of-use \"Argentina - onshore\" \
            --copyright \"Derived from work by IGN Argentina. CC-BY-4.0 https://creativecommons.org/licenses/by/4.0/\" \
            ./build/$input ./$output && \
            # Show info
            gdalinfo ./$output "

# Remove build directory
rm -rf build
