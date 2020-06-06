# sk_gku_README.txt

The files in this section result from the conversion of datasets originating
from [GKU](https://www.geoportal.sk/en/) (Geodetic and Cartographic Institute).

## Included grids

### Slovakia: JTSK03 -> JTSK

*Source*: [GKU](https://www.geoportal.sk/en/geodeticke-zaklady/download/)
*Format*: GeoTIFF converted from NTv2  
*License*: [Creative Commons Attribution 4.0](http://creativecommons.org/licenses/by/4.0/)
*Copyright*: 2013, GKU Bratislava
*Source CRS*: EPSG:8351 (S-JTSK [JTSK03])  
*Target CRS*: EPSG:4156 (S-JTSK)  
*Used by*: [EPSG:8364 Transformation](https://www.epsg-registry.org/export.htm?gml=urn:ogc:def:coordinateOperation:EPSG::8364)

This is digital datum shift model for horizontal coordinates transformation between JTSK03 and JTSK 
reference frames of S-JTSK coordinate refernce system in the territory of Slovakia.
Transformation shift model involves the vectors of coordinate differences defined
in the plane JTSK03 on 684 identical points. It is the same set of identical points, which
has been used for the computation of the 7 Helmert transformation parameters of the global transformation key.
The computed coordinate differences characterize systematic non-homogeneity of the JTSK frame, but
do not aptly describe detailed non-homogeneity of lesser localities on cm level.
For purposes of the unambiguous definition of transformation relation between the JTSK03 and JTSK
frames it was necessary to express coordinate differences in the form of a regular grid and to define
the interpolation method. For this purpose the coordinate differences between JTSK03 and JTSK
in the shape of ellipsoidal coordinates on Bessell1841 ellipsoid for individual axes have been
interpolated by the Surfer software kriging method into a regular grid with a step 0.0168 deg (latitude) x 0.025 deg (longitude).

For correct usage of those shift models always check your outputs with transformation service: https://zbgis.skgeodesy.sk/rts/en/Transform 

* sk_gku_JTSK03_to_JTSK.tif

### Slovakia: ETRS89 -> Baltic 1957 height

*Source*: [GKU](https://www.geoportal.sk/en/geodeticke-zaklady/download/)
*Format*: GeoTIFF converted from GTX  
*License*: [Creative Commons Attribution 4.0](http://creativecommons.org/licenses/by/4.0/)  
*Copyright*: 2005, GKU Bratislava  
*Source CRS*: EPSG:4937 (ETRS89)  
*Target CRS*: EPSG:8360 (ETRS89 + Baltic 1957 height)  
*Used by*: [EPSG:8361 Transformation](https://www.epsg-registry.org/export.htm?gml=urn:ogc:def:coordinateOperation:EPSG::8361)

Digital Vertical Reference Model - DVRM05
Model is intended for the transfer of ellipsoidal heights determined using GNSS
in the ETRS89 system to the system of normal heights Bpv.

* sk_gku_Slovakia_ETRS89h_to_Baltic1957.tif

### Slovakia: ETRS89 -> EVRF2007 height

*Source*: [GKU](https://www.geoportal.sk/en/geodeticke-zaklady/download/)
*Format*: GeoTIFF converted from GTX  
*License*: [Creative Commons Attribution 4.0](http://creativecommons.org/licenses/by/4.0/)  
*Copyright*: 2014, GKU Bratislava  
*Source CRS*: EPSG:4937 (ETRS89)  
*Target CRS*: EPSG:7423 (ETRS89 + EVRF2007 height)  
*Used by*: [EPSG:8362 Transformation](https://www.epsg-registry.org/export.htm?gml=urn:ogc:def:coordinateOperation:EPSG::8362)

This is the official differential height correction grid intended to be used for transformation ellipsoidal
height on GRS80 ellipsoid to EVRF2007 normal height in the territory of Slovakia.
Grid has a cell size 20 arcsec x 30 arcsec.

Slovakia_ETRS89h_to_EVRF2007.gtx grid represents the quasigeoid with the name DMQSK2014-E.
DMQSK2014-E uses the relation between Baltic1957 and EVRS (EVRF2007) on the basis of which
the DMRZ-H digital model of a residual component has been created using a selected set of 93
points. DMQSK2014-E has been subsequently obtained by simple subtracting of the model of this
residual component DMRZ-H from the DVRM05 quasigeoid model. On the basis of testing executed
on the independent points the standard deviation 1 sigma size 23 milimeters has been obtained.Hence it can
be said that the DMQSK2014-E precision is of precision comparable to DVRM05 i.e. it achieves
precision of technical levelling (obviously providing the high-quality determination of
ellipsoidal height). However, it should also be mentioned that the defined precision of the
DMQSK2014-E quasigeoid may be distorted by a low number of the test points.

* sk_gku_Slovakia_ETRS89h_to_EVRF2007.tif
