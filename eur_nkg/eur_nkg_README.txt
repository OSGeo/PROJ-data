# eur_nkg_README.txt

The files in this section result from the conversion of datasets originating
from [Nordic Geodetic Commission](https://github.com/NordicGeodesy/NordicTransformations)  

## Included grids

### Nordic+Baltic countries: 2003 Deformation model

*Source*: [The Nordic Geodetic Commission](https://github.com/NordicGeodesy/NordicTransformations)  
*Format*: GeoTIFF file converted from CTable2 and GTX  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)

Deformation model covering the Nordic and Baltic countries. Used in
transformations between global reference frames and the local realisations
of ETRS89 in the Nordic and Baltic countries. See the `NKG` init-file for
examples of use.

* eur_nkg_nkgrf03vel_realigned.tif

### Nordic+Baltic countries: 2017 Deformation model

*Source*: [The Nordic Geodetic Commission](https://http://www.nordicgeodeticcommission.com/)  
*Format*: GeoTIFF file  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)

Deformation model covering the Nordic and Baltic countries. Used in
transformations between global reference frames and the local realisations
of ETRS89 in the Nordic and Baltic countries.

* eur_nkg_nkgrf17vel.tif

## Included init-files

### Nordic+Baltic countries: ITRFxx -> Local ETRS89 realizations

*Source*: [The Nordic Geodetic Commission](https://github.com/NordicGeodesy/NordicTransformations)  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)

Transformations to and from the common Nordic referenc frame NKG_ETRF00.
This init-file describes transformations between global reference frames
and NKG_ETRF00 as well as transformations from NKG_ERTF00 to the local
realisations of ETRS89 in each of the countries involved with NKG.

All transformations in this init-file uses the common Nordic frame as a
pivot datum. Exempt from this dogma are transformations with labels
starting with ``_``. Those transformations are "private" to this file and are
only used as steps in more complicated transformations.

* NKG
