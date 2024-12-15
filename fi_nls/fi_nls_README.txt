# fi_nls_README.txt

The files in this section result from the conversion of datasets originating
from [National Land Survey of Finland](https://www.maanmittauslaitos.fi)  

## Triangulated models

### Finland: KKJ / Finland Uniform Coordinate System to ETRS35FIN

*Source*: [National Land Survey of Finland](https://www.maanmittauslaitos.fi)  
*Format*: JSON converted from text files  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)

Triangulation to transform coordinates from YKJ (EPSG:2393), with easting/northing order, to ETRS35FIN (EPSG:3067)

* fi_nls_ykj_etrs35fin.json

### Finland: N43 height -> N60 height

*Source*: [National Land Survey of Finland](https://www.maanmittauslaitos.fi)  
*Format*: JSON converted from text files  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)

Triangulation to transform N43 height (EPSG:8675) to N60 height (EPSG:5717), with interpolation CRS being YKJ (EPSG:2393), with easting/northing order

* fi_nls_n43_n60.json

### Finland: N60 height -> N2000 height

*Source*: [National Land Survey of Finland](https://www.maanmittauslaitos.fi)  
*Format*: JSON converted from text files  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)

Triangulation to transform N60 height (EPSG:5717) to N2000 height(EPSG:3900), with interpolation CRS being YKJ (EPSG:2393), with easting/northing order

* fi_nls_n60_n2000.json

### Finland: vertical grid FIN2000

*Source*: [National Land Survey of Finland](https://www.maanmittauslaitos.fi/kartat-ja-paikkatieto/asiantuntevalle-kayttajalle/koordinaattimuunnokset/fin2000-geoidimalli)  
*Format*: GeoTIFF converted from 'XYZ'  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)  
*Credit*: (c)  National Land Survey of Finland  
*Horizontal CRS*: EUREF-FIN (EPSG:10689)

Vertical transformation for Geoid model FIN2000. Used to make the transition
from heights in vertical CRS N60 height (EPSG:5717)
to heights above the ellipsoid in EUREF-FIN (EPSG:10689).

* fi_nls_fin2000.tif

### Finland: vertical grid FIN2005N00

*Source*: [National Land Survey of Finland](https://www.maanmittauslaitos.fi/kartat-ja-paikkatieto/asiantuntevalle-kayttajalle/koordinaattimuunnokset/fin2005n00-geoidimalli)  
*Format*: GeoTIFF converted from 'XYZ'  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)  
*Credit*: (c)  National Land Survey of Finland  
*Horizontal CRS*: EUREF-FIN (EPSG:10689)

Vertical transformation for Geoid model FIN2005N00. Used to make the transition
from heights in vertical CRS N2000 height (EPSG:3900)
to heights above the ellipsoid in EUREF-FIN (EPSG:10689).

* fi_nls_fin2005n00.tif

### Finland: vertical grid FIN2023N2000

*Source*: [National Land Survey of Finland](https://www.maanmittauslaitos.fi/kartat-ja-paikkatieto/koordinaatit-ja-paikannus/koordinaattimuunnokset/fin2023n2000-geoidimalli)  
*Format*: GeoTIFF converted from 'XYZ'  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)  
*Credit*: (c)  National Land Survey of Finland  
*Horizontal CRS*: EUREF-FIN (EPSG:10689)

Vertical transformation for Geoid model FIN2023N2000. Used to make the transition
from heights in vertical CRS N2000 height (EPSG:3900)
to heights above the ellipsoid in EUREF-FIN (EPSG:10689).

* fi_nls_fin2023n2000.tif