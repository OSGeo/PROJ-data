#!/bin/bash

BUILD_DIR=./build
NTV2_TO_GTIFF_PATH=../grid_tools/ntv2_to_gtiff.py
VERTOFFSET_GRID_TO_GTIFF=../grid_tools/vertoffset_grid_to_gtiff.py
AGENCY_PREFIX="hu_bme_geod"

ETRS2EOV_SOURCE_URL="https://raw.githubusercontent.com/OSGeoLabBp/eov2etrs/master/etrs2eov_notowgs.gsb"
ETRS2EOV_SOURCE_PATH=${ETRS2EOV_SOURCE_URL##*/}
ETRS2EOV_TARGET_PATH=${AGENCY_PREFIX}_${ETRS2EOV_SOURCE_PATH%gsb}tif
ETRS2EOV_SOURCE_CRS="EPSG:4237"
ETRS2EOV_TARGET_CRS="EPSG:4937"
ETRS2EOV_DESCRIPTION="Grid transformation from HD72 to ETRS89 (typically applied for transformations from projected CRS HD72/EOV (EPSG:23700) to ETRS89)."

GEOID_EHT2014_SOURCE_URL="https://raw.githubusercontent.com/OSGeoLabBp/eov2etrs/master/geoid_eht2014.gtx"
GEOID_EHT2014_SOURCE_PATH=${GEOID_EHT2014_SOURCE_URL##*/}
GEOID_EHT2014_TARGET_PATH=${AGENCY_PREFIX}_${GEOID_EHT2014_SOURCE_PATH%gtx}tif
GEOID_EHT2014_SOURCE_CRS="EPSG:4937"
GEOID_EHT2014_TARGET_CRS="EPSG:8357"
GEOID_EHT2014_DESCRIPTION="ETRS89 ellipsoidal heights to baltic height system transformation."

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

curl ${GEOID_EHT2014_SOURCE_URL} --output ${BUILD_DIR}/${GEOID_EHT2014_SOURCE_PATH}
python3 \
	${VERTOFFSET_GRID_TO_GTIFF} \
	--type GEOGRAPHIC_TO_VERTICAL \
	--source-crs "${GEOID_EHT2014_SOURCE_CRS}" \
	--target-crs "${GEOID_EHT2014_TARGET_CRS}" \
	--description "${GEOID_EHT2014_DESCRIPTION}" \
	--copyright "${COMMON_COPYRIGHT}" \
	--area-of-use "${COMMON_AREA_OF_USE}" \
	${BUILD_DIR}/${GEOID_EHT2014_SOURCE_PATH} \
	${GEOID_EHT2014_TARGET_PATH}

rm -rf ${BUILD_DIR}