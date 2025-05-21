#!/bin/sh

python ../grid_tools/ntv2_to_gtiff.py \
    --source-crs EPSG:4661 \
    --target-crs EPSG:10305 \
    --copyright "Derived from work by Latvian Geospatial Information Agency. CC-BY 4.0"\
    --description "LKS-92 (EPSG:4661) to LKS-2020 (EPSG:10305). Converted from LKS92to2020NTv2.gsb." \
    --area-of-use "Latvia - onshore and offshore" \
    LKS92to2020NTv2.gsb \
    lv_lgia_lks92to2020.tif
