# hu_bme_README.txt

The files in this section result from the conversion of datasets originating
from [Department of Geodesy and Surveying of Budapest University of Technology and Economics](https://geod.bme.hu/hirek?language=en)

## Included grids

### Hungary: ETRF2000 --> EOMA 1980 height

*Source*: [Department of Geodesy and Surveying of Budapest University of Technology and Economics](https://geod.bme.hu/geod/onlineszolgaltatasok)
*Format*: GeoTIFF converted from NTv2  
*License*: [Creative Commons Attribution 4.0 BY-SA](https://creativecommons.org/licenses/by-sa/4.0/)  
*Source CRS*: EPSG:7931 (ETRF2000)  
*Target CRS*: EPSG:5787 (EOMA)  
*Used by*: [EPSG:10666 Transformation](https://???:EPSG::10666)  

Recommended to transform from European reference frame ETRF2000 (EPSG:7931) 
to Hungarian EOMA 1980 heights (EPSG:5787).

* hu_bme_geoid2014.tif

### Hungary: ETRF2000 --> ETRF2000 + EOMA 1980 height

*Source*: [Department of Geodesy and Surveying of Budapest University of Technology and Economics](https://geod.bme.hu/geod/onlineszolgaltatasok)
*Format*: GeoTIFF converted from NTv2  
*License*: [Creative Commons Attribution 4.0 BY-SA](https://creativecommons.org/licenses/by-sa/4.0/)  
*Source CRS*: EPSG:7931 (ETRF2000)  
*Target CRS*: EPSG:10659 (Compound CRS: EPSG:9067 (ETRF2000) + EPSG:5787 (EOMA 1980 height))  
*Used by*: [EPSG:10667 Transformation](https://???:EPSG::10667)

Recommended to transform from European reference frame ETRF2000 (EPSG:7931)
to European reference frame ETRF2000 + Hungarian EOMA 1980 heights.

* hu_bme_geoid2014.tif

### Hungary: HD72 --> ETRF2000

*Source*: [Department of Geodesy and Surveying of Budapest University of Technology and Economics](https://geod.bme.hu/geod/onlineszolgaltatasok)
*Format*: GeoTIFF converted from NTv2  
*License*: [Creative Commons Attribution 4.0 BY-SA](https://creativecommons.org/licenses/by-sa/4.0/)  
*Source CRS*: EPSG:4237 (HD72)  
*Target CRS*: EPSG:9067 (ETRF2000)  
*Used by*: [EPSG:10668 Transformation](https://???:EPSG::10668)  

Recommended to transform from Hungarian Datum HD72 (EPSG:4237)
to European reference frame ETRF2000 (EPSG:9067).

* hu_bme_hd72corr.tif

