# us_nga_README.txt

The files in this section result from the conversion of datasets originating
from [US NGA](http://earth-info.nga.mil)

## Included grids

### Worldwide: EGM96 geoid model

*Source*: [NGA](http://earth-info.nga.mil/GandG/wgs84/gravitymod/egm96/egm96.html)  
*Format*: GeoTIFF converted from GTX  
*License*: Public Domain  

15 minute worldwide geoid undulation grid that transforms physical heights to WGS84 ellipsoidal heights.

* us_nga_egm96_15.tif

### Vertical grid: EGM2008 geoid model

*Source*: [NGA](http://earth-info.nga.mil/GandG/wgs84/gravitymod/egm2008/egm08_wgs84.html)  
*Format*: GeoTIFF converted from GTX
*License*: Public Domain

2.5 minute worldwide geoid undulation grid that transforms physical heights to WGS84 ellipsoidal heights.

This file has been produced by [GeographicLib](https://geographiclib.sourceforge.io/html/gravity.html)
using the EGM2008 gravity model and can be regenerated with the
[build_egm08_25_gtx.sh](https://raw.githubusercontent.com/OSGeo/proj-datumgrid/master/world/build_egm08_25_gtx.sh) script.

* us_nga_egm08_25.tif
