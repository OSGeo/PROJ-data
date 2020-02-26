#!/bin/sh

rm -rf build_tmp
mkdir build_tmp
cd build_tmp

wget http://www.bev.gv.at/pls/portal/docs/PAGE/BEV_PORTAL_CONTENT_ALLGEMEIN/0200_PRODUKTE/UNENTGELTLICHE_PRODUKTE_DES_BEV/Hoehen-Grid_GeoTIFF.zip
unzip -o Hoehen-Grid_GeoTIFF.zip
python3 ../../grid_tools/vertoffset_grid_to_gtiff.py  --type VERTICAL_TO_VERTICAL --source-crs EPSG:5778 --target-crs EPSG:9274 --interpolation-crs EPSG:4312 --copyright "Derived from work by BEV. Creative Commons Attribution 4.0 https://creativecommons.org/licenses/by/4.0/" --description "GHA height (EPSG:5778) to EVRF2000 Austria height (EPSG:9274). Converted from GV_Hoehengrid_V1.tif" --area-of-use Austria GV_Hoehengrid_V1.tif ../at_bev_GV_Hoehengrid_V1.tif

wget "http://www.bev.gv.at/pls/portal/docs/PAGE/BEV_PORTAL_CONTENT_ALLGEMEIN/0200_PRODUKTE/UNENTGELTLICHE_PRODUKTE_DES_BEV/GV_Hoehengrid_plus_Geoid_V2(GeoTIFF).zip"
unzip -o "GV_Hoehengrid_plus_Geoid_V2(GeoTIFF).zip"
python3 ../../grid_tools/vertoffset_grid_to_gtiff.py  --type GEOGRAPHIC_TO_VERTICAL --source-crs EPSG:4937 --target-crs EPSG:5778  --copyright "Derived from work by BEV. Creative Commons Attribution 4.0 https://creativecommons.org/licenses/by/4.0/" --description "ETRS89 (EPSG:4937) to GHA Austria height (EPSG:5778). Converted from GV_Hoehengrid_plus_Geoid_V2.tif" --area-of-use Austria GV_Hoehengrid_plus_Geoid_V2.tif ../at_bev_GV_Hoehengrid_plus_Geoid_V2.tif

wget http://www.bev.gv.at/pls/portal/docs/PAGE/BEV_PORTAL_CONTENT_ALLGEMEIN/0200_PRODUKTE/UNENTGELTLICHE_PRODUKTE_DES_BEV/GV_GEOID_Oesterreich.zip
unzip -o GV_GEOID_Oesterreich.zip 

ogr2ogr GEOID_GRS80_Oesterreich.gpkg GEOID_GRS80_Oesterreich.csv -oo Y_POSSIBLE_NAMES=BREITE -oo X_POSSIBLE_NAMES=LAENGE
gdal_grid GEOID_GRS80_Oesterreich.gpkg GEOID_GRS80_Oesterreich.tif -zfield UNDULATION -ot Float32 -txe 9.4791666666666667 17.270833333333333 -tye 49.0875 46.3125 -outsize 187 111 -a nearest:radius1=0.001:radius2=0.001:nodata=-32768 
python3 ../../grid_tools/vertoffset_grid_to_gtiff.py  --type GEOGRAPHIC_TO_VERTICAL --source-crs EPSG:4937 --target-crs EPSG:9274 --copyright "Derived from work by BEV. Creative Commons Attribution 4.0 https://creativecommons.org/licenses/by/4.0/" --description "ETRS89 (EPSG:4937) to EVRF2000 Austria height (EPSG:9274). Converted from GEOID_GRS80_Oesterreich.csv" --area-of-use Austria GEOID_GRS80_Oesterreich.tif ../at_bev_GEOID_GRS80_Oesterreich.tif

ogr2ogr GEOID_BESSEL_Oesterreich.gpkg GEOID_BESSEL_Oesterreich.csv -oo Y_POSSIBLE_NAMES=BREITE -oo X_POSSIBLE_NAMES=LAENGE
gdal_grid GEOID_BESSEL_Oesterreich.gpkg GEOID_BESSEL_Oesterreich.tif -zfield UNDULATION -ot Float32 -txe 9.4791666666666667 17.270833333333333 -tye 49.0875 46.3125 -outsize 187 111 -a nearest:radius1=0.001:radius2=0.001:nodata=-32768 
python3 ../../grid_tools/vertoffset_grid_to_gtiff.py  --type GEOGRAPHIC_TO_VERTICAL --source-crs EPSG:9267 --target-crs EPSG:9274 --copyright "Derived from work by BEV. Creative Commons Attribution 4.0 https://creativecommons.org/licenses/by/4.0/" --description "MGI (EPSG:9267) to EVRF2000 Austria height (EPSG:9274). Converted from GEOID_BESSEL_Oesterreich.csv" --area-of-use Austria GEOID_BESSEL_Oesterreich.tif ../at_bev_GEOID_BESSEL_Oesterreich.tif

cd ..
rm -rf build_tmp

