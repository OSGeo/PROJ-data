# pt_dgt_README.txt

The files in this section result from the conversion of datasets originating
from [DG Territorio](http://www.dgterritorio.pt/)

## Included grids

### Portugal: Lisbon Datum -> ETRS89

Grid transformation from Portuguese Lisbon Datum to ETRS89 in Portugal.

*Source*: [DGT](http://www.dgterritorio.pt/cartografia_e_geodesia/geodesia/transformacao_de_coordenadas/grelhas_em_ntv2/)  
*Format*: GeoTIFF converted from NTv2  
*License*: [Creative Commons Attribution 4.0](http://creativecommons.org/licenses/by/4.0/)  
*Credit*: (c)2019 Directorate-General for the Territorial Development.

Derived from 1129 common stations in the national geodetic network. 
Residuals at 130 further test points average 0.09m, maximum 0.30m.
Recommended to transform from Portuguese Lisbon Datum (EPSG:20790) to ETRS89 in Portugal (EPSG:3763).

* pt_dgt_DLx_ETRS89_geo.tif

### Portugal: Datum 73 -> ETRS89

Grid transformation from Portuguese Datum 73 to ETRS89 in Portugal.

*Source*: [DGT](http://www.dgterritorio.pt/cartografia_e_geodesia/geodesia/transformacao_de_coordenadas/grelhas_em_ntv2/)  
*Format*: GeoTIFF converted from NTv2  
*License*: [Creative Commons Attribution 4.0](http://creativecommons.org/licenses/by/4.0/)  
*Credit*: (c)2019 Directorate-General for the Territorial Development.

Derived from 1129 common stations in the national geodetic network. 
Residuals at 130 further test points average 0.06m, maximum 0.16m.
Recommended to transform from Portuguese Datum 73 (EPSG:27493) to ETRS89 in Portugal (EPSG:3763).

* pt_dgt_D73_ETRS89_geo.tif

### Portugal: Vertical grid GeodPT08

*Source*: [DGT](https://www.dgterritorio.gov.pt/geodesia/modelo-geoide)  
*Format*: GeoTIFF converted from XYZ (adjusted)  
*License*: [Creative Commons Attribution 4.0](http://creativecommons.org/licenses/by/4.0/)  
*Credit*: (c)2024 Geoid for Portugal Mainland by DGT+FCUL  
*Horizontal CRS*: EPSG:4258 (ETRS89)  
*Accuracy*: 0.04 m

Built based on the ICAGM07 gravimetric geoid model using 137 leveling marks and 1020 geodetic vertices.
Estimated global accuracy of 4 cm, determined with reference to the continent's geodetic vertex and geometric leveling networks.

Vertical transformation (EPSG:10544) for Geoid model GeodPT08.
Used to make the transition from heights in vertical CRS Cascais height (EPSG:5780)
to heights abobe the ellipsoid in ETRS89 (EPSG:4937)

* pt_dgt_GeodPT08.tif
