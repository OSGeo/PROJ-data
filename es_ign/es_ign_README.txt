# es_ign_README.txt

The files in this section result from the conversion of datasets originating
from [IGN](https://www.ign.es/)

## Included grids

### Spanish (Spain - mainland and Balearic Islands) vertical grid: 

*Source*: [IGN Spain](ftp://ftp.geodesia.ign.es/geoide/ascii/)  
*Converter*: vertoffset_grid_to_gtiff.py  
*Format*: GeoTIFF convered from "Arc/Info ASCII Grid"
*License*: Derivated from Original IGN Data www.ign.es CC-BY 4.0. [Politica de datos](https://www.ign.es/web/ign/portal/politica-datos)
*Horizontal CRS*: EPSG:4937 (ETRS89)

Vertical transformation for Geoid model EGM08-REDNAP. Used to make the transitions 
from heights in vertical CRS (EPSG:5782) to heights above the ellipsoid in ETRS89 (EPSG:4937).

* es_ign_egm08-rednap.tif
