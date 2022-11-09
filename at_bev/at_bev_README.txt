# at_bev_README.txt

The files in this section result from the conversion of datasets originating
from [Austria Bundesamt für Eich- und Vermessungswessen](www.bev.gv.at)

## Included grids

### Austria: MGI -> ETRS89

*Source*: [BEV](http://www.bev.gv.at/portal/page?_pageid=713,2157075&_dad=portal&_schema=PORTAL)  
*Format*: GeoTIFF converted from NTv2  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)

Grid from 2014 with 0.0125 x 0.0083333 degree resolution:
* at_bev_AT_GIS_GRID.tif

Grid from 2021 with 0.00194444 x 0.00138889 degree resolution:
* at_bev_AT_GIS_GRID_2021_09_28.tif

### Austria :GHA height -> EVRF2000 Austria height

*Source*: [BEV](http://www.bev.gv.at/portal/page?_pageid=713,2601281&_dad=portal&_schema=PORTAL)  
*Format*: GeoTIFF converted from original GeoTIFF  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)  
*Source CRS*: EPSG:5778 (GHA height)  
*Target CRS*: EPSG:9274 (EVRF2000 Austria height)  
*Interpolation CRS*: EPSG:4312 (MGI)  
*Used by*: [EPSG:9275 Transformation](https://www.epsg-registry.org/export.htm?gml=urn:ogc:def:coordinateOperation:EPSG::9275)

* at_bev_GV_Hoehengrid_V1.tif

### Austria :ETRS89 -> EVRF2000 Austria height

*Source*: [BEV](http://www.bev.gv.at/portal/page?_pageid=713,2601285&_dad=portal&_schema=PORTAL)  
*Format*: GeoTIFF converted from original CSV file GEOID_GRS80_Oesterreich.csv from http://www.bev.gv.at/pls/portal/docs/PAGE/BEV_PORTAL_CONTENT_ALLGEMEIN/0200_PRODUKTE/UNENTGELTLICHE_PRODUKTE_DES_BEV/GV_GEOID_Oesterreich.zip  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)  
*Source CRS*: EPSG:4937 (ETRS89)  
*Target CRS*: EPSG:9274 (EVRF2000 Austria height)  
*Used by*: [EPSG:9276 Transformation](https://www.epsg-registry.org/export.htm?gml=urn:ogc:def:coordinateOperation:EPSG::9276)

* at_bev_GEOID_GRS80_Oesterreich.tif

### Austria :MGI -> EVRF2000 Austria height

*Source*: [BEV](http://www.bev.gv.at/portal/page?_pageid=713,2601285&_dad=portal&_schema=PORTAL)  
*Format*: GeoTIFF converted from original CSV file GEOID_BESSEL_Oesterreich.csv from http://www.bev.gv.at/pls/portal/docs/PAGE/BEV_PORTAL_CONTENT_ALLGEMEIN/0200_PRODUKTE/UNENTGELTLICHE_PRODUKTE_DES_BEV/GV_GEOID_Oesterreich.zip  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)  
*Source CRS*: EPSG:9267 (MGI)  
*Target CRS*: EPSG:9274 (EVRF2000 Austria height)  
*Used by*: [EPSG:9277 Transformation](https://www.epsg-registry.org/export.htm?gml=urn:ogc:def:coordinateOperation:EPSG::9277)

* at_bev_GEOID_BESSEL_Oesterreich.tif

### Austria :ETRS89 -> GHA Austria height

*Source*: [BEV](http://www.bev.gv.at/portal/page?_pageid=713,2823796&_dad=portal&_schema=PORTAL)  
*Format*: GeoTIFF converted from original GeoTIFF  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)  
*Source CRS*: EPSG:4937 (ETRS89)  
*Target CRS*: EPSG:5778 (GHA Austria height)  
*Used by*: [EPSG:9278 Transformation](https://www.epsg-registry.org/export.htm?gml=urn:ogc:def:coordinateOperation:EPSG::9278)

* at_bev_GV_Hoehengrid_plus_Geoid_V2.tif
