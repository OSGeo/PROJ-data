# ch_swisstopo_README.txt

The files in this section result from the conversion of datasets originating
from [Swisstopo](https://www.swisstopo.admin.ch)

## Included grids

### Switzerland: LV03 (system CH1903) -> LV95 (system CH1903+)

*Source*: [swisstopo](https://www.swisstopo.admin.ch/en/knowledge-facts/surveying-geodesy/reference-frames/transformations-position.html)  
*Format*: GeoTIFF converted from NTv2.0 (.gsb)  
*License*: [Creative Commons CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/legalcode)  
*Credit*: (c) 2007 swisstopo

Recommended to transform from Swiss reference frame LV03 (system CH1903, EPSG:21781) to Swiss reference frame LV95 (system CH1903+, EPSG:2056).
LV95 is aligned to ETRF93, but shifted by several 100 meters.
CH1903+ is the official reference system for federal surveying and for all national geobasis data regulated by federal law since 2017.
CHENyx06a.gsb gives corrections (distorsions between LV03 and LV95) in CH1903, CHENyx06_ETRS.gsb gives the corrections in ETRS.
Several transformation services are available on https://www.swisstopo.admin.ch/en/maps-data-online/calculation-services.html
(web forms and REST web geoservices) to support the exact transformation procedure between CH1903 and CH1903+
using the REFRAME algorithm (finite element transformation).
The difference between the grid and finite element transformation is on a level of below several millimeters.

* ch_swisstopo_CHENyx06a.tif
* ch_swisstopo_CHENyx06_ETRS.tif

### Switzerland vertical grid:

*Source*: [swisstopo](https://www.swisstopo.admin.ch/en/knowledge-facts/surveying-geodesy/geoid.html)
*Format*: GeoTIFF converted from 'Arc/Info ASCII Grid'
*License*: [Creative Commons CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/legalcode)  
*Credit*: (c) swisstopo
*Horizontal CRS*: EPSG:4937 (ETRS89)  

Two vertical transformations based on CHTRF95 for Geoid model CHGeo2004. Used to make the transitions 
from heights in vertical CRS (EPSG:5729 - LHN95 heigh) or (EPSG:5728 - LN02 height) 
to heights above the ellipsoid in ETRS89 (EPSG:4937).

* ch_swisstopo_chgeo2004_ETRS89_LHN95.tif
* ch_swisstopo_chgeo2004_ETRS89_LN02.tif
