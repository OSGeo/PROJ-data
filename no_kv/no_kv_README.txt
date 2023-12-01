# no_kv_README.txt

The files in this section result from the conversion of datasets originating
from [Kartverket](https://www.kartverket.no)

## Included grids

### Norway: NN2000 heights -> ETRS89 ellipsoidal heights

*Source*: [Kartverket](https://nedlasting.geonorge.no/geonorge/generell/71a73064-59a5-4f03-a0b8-fa5c649c3fc9.zip)  
*Format*: GeoTIFF converted from GTX  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)

Transform local height system NN2000 (EPSG:5941) to ETRS89 ellipsoidal heights (EPSG:4937).
The horizontal grid coordinates are referenced to ETRS89.

* no_kv_HREF2018B_NN2000_EUREF89.tif

### Norway: NN1954 heights -> ETRS89 ellipsoidal heights

*Source*: [Kartverket](https://nedlasting.geonorge.no/geonorge/generell/9219f396-b9e9-47e7-a8de-d7ea03e29e5e.zip)  
*Format*: GeoTIFF converted from GTX  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)

Transform local height system NN1954 (EPSG:5776) to ETRS89 ellipsoidal heights (EPSG:4937).
The horizontal grid coordinates are referenced to ETRS89.

* no_kv_href2008a.tif

### Norway: Geocentric translation correction grid NKG_ETRF14 epoch 2000.0 -> ETRF93 epoch 2000.0

*Format*: GeoTIFF  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)  
*Source CRS*: NKG:ETRF14  
*Target CRS*: EPSG:7922 (ETRF93)

* no_kv_NKGETRF14_EPSG7922_2000.tif

The correction grid is one of the steps in the transformation from EPSG:7789 to the norwegian 
EPSG:4936 (Extent EPSG:1352). The grid contains x-, y- and z-shifts between NKG:ETRF14 
and EPSG:7922 at epoch 2000.0, which are computed based on 7 parameter Helmert smoothed with 
Least Squares Collocation. Input to the computation is 189 points in the norwegian CORS network 
referred in NKG:ETRF14 and EPSG:7922.

### Norway: ETRS89 -> NGO1948

*Source*: [Kartverket](https://kartkatalog.geonorge.no/metadata/transformasjoner/352fba08-f25e-499d-8a80-a1f78e526641/)  
*Format*: JSON converted from text files  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)

Horizontal triangulation to transform coordinates from ETRS89 (EPSG:4258) to NGO1948 (EPSG:4273), with longitude/latitude order.

* no_kv_ETRS89NO_NGO48_TIN.json

### Norway: ETRS89 ellipsoidal heights -> CD Norway heights

*Format*: GeoTIFF converted from BIN  
*Source*: [Kartverket](https://kartkatalog.geonorge.no/metadata/middelvann-over-ellipsoiden/e857e50c-fce4-49dc-abf5-a135bad8f727)  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)  
*Source CRS*: EPSG:4937 (ETRS89 ellipsoidal heights)  
*Target CRS*: EPSG:9672 (Chart datum Norway heights)

* no_kv_CD_above_Ell_ETRS89_v2023b.tif

### Norway: ETRS89 ellipsoidal heights -> Svalbard 2006 heights

*Format*: GeoTIFF converted from GravSoft BIN  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)  
*Source CRS*: EPSG:4937 (ETRS89 ellipsoidal heights)  
*Target CRS*: EPSG:20000 (SVD2006 heights)

The grid transforms from ETRS89 ellipsoidal heights to SVD2006 heights (Svalbard heights).
The SVD2006 surface (arcgp-2006-sk) is the Arctic Gravity Project 2006
(arcgp-2006) surface adjusted to two benchmarks tied to the Ny-Ålesund tide gauge (arcgp-2006-sk = arcgp-2006 - 0.8986m).
The SVD2006 surface is defined by Mean Sea Level (MSL) at Ny-Ålesund.

* no_kv_arcgp-2006-sk.tif
