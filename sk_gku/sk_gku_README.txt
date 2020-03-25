# sk_gku_README.txt

The files in this section result from the conversion of datasets originating
from [GKU](https://www.geoportal.sk/en/) (Geodetic and Cartographic Institute).

## Included grids

### Slovakia: JTSK03 -> JTSK

*Source*: [GKU](https://www.geoportal.sk/en/geodeticke-zaklady/download/)
*Format*: GeoTIFF converted from NTv2  
*License*: [Creative Commons Attribution 4.0](http://creativecommons.org/licenses/by/4.0/)

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
