# cz_cuzk_README.txt

The files in this section result from the conversion of datasets originating
from [ČÚZK](https://geoportal.cuzk.cz/)

## Included grids

### Czech horizontal grid:

*Source*: [ČÚZK](https://geoportal.cuzk.gov.cz/dokumenty/table_-y-x_3_v1710.tif.zip)  
*Format*: Geodetic TIFF Grid (GTG)  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)  
*Credit*: (c) ČÚZK - Czech Republic  
*Source CRS*: EPSG:5514 (S-JTSK / Krovak East North)  
*Target CRS*: EPSG:5516 ( S-JTSK/05 / Modified Krovak East North)

S-JTSK / Krovak East North (EPSG:5514) to S-JTSK/05 / Modified Krovak East North (EPSG:5516).
Note also that an extra offset of -5000000 in easting and northing must be applied

* cz_cuzk_table_-y-x_3_v1710.tif

### Czech vertical grid:

*Source*: [ČÚZK](https://geoportal.cuzk.cz/dokumenty/CR2005.GTX.zip)  
*Format*: GeoTIFF converted from 'AAIGrid'  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)  
*Credit*: (c) ČÚZK - Czech Republic  
*Horizontal CRS*: EPSG:4937 (ETRS89)

Vertical transformation for Geoid model CR-2005. Used to make the transition
from heights in vertical CRS Baltic 1957 height (EPSG:8357)
to heights above the ellipsoid in ETRS89 (EPSG:4937).

* cz_cuzk_CR-2005.tif

