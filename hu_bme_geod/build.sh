#!/bin/bash

BUILD_DIR=./build
NTV2_TO_GTIFF_PATH=../grid_tools/ntv2_to_gtiff.py
AGENCY_PREFIX="hu_bme_geod"

ETRS2EOV_SOURCE_URL="https://raw.githubusercontent.com/OSGeoLabBp/eov2etrs/master/etrs2eov_notowgs.gsb"
ETRS2EOV_SOURCE_PATH=${ETRS2EOV_SOURCE_URL##*/}
ETRS2EOV_TARGET_PATH=${AGENCY_PREFIX}_${ETRS2EOV_SOURCE_PATH%gsb}tif
ETRS2EOV_SOURCE_CRS="EPSG:4237"
ETRS2EOV_TARGET_CRS="EPSG:4937"
ETRS2EOV_DESCRIPTION="Grid transformation from HD72 to ETRS89 (typically applied for transformations from projected CRS HD72/EOV (EPSG:23700) to ETRS89)."

COMMON_COPYRIGHT="Budapest University of Technology and Economics - Faculty of Civil Engineering. Creative Commons Attribution 4.0 https://creativecommons.org/licenses/by/4.0/"
COMMON_AREA_OF_USE="Hungary"

rm -rf ${BUILD_DIR}
mkdir ${BUILD_DIR}

curl ${ETRS2EOV_SOURCE_URL} --output ${BUILD_DIR}/${ETRS2EOV_SOURCE_PATH}
python3 \
	${NTV2_TO_GTIFF_PATH} \
	--source-crs "${ETRS2EOV_SOURCE_CRS}" \
	--target-crs "${ETRS2EOV_TARGET_CRS}" \
	--description "${ETRS2EOV_DESCRIPTION}" \
	--copyright "${COMMON_COPYRIGHT}" \
	--area-of-use "${COMMON_AREA_OF_USE}" \
	${BUILD_DIR}/${ETRS2EOV_SOURCE_PATH} \
	${ETRS2EOV_TARGET_PATH}

rm -rf ${BUILD_DIR}