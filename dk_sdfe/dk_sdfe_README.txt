# dk_sdfe_README.txt

The files in this section result from the conversion of datasets originating
from [Agency for Data Supply and Efficiency](https://github.com/NordicGeodesy/NordicTransformations)  

## Included grids

### Denmark: DVR90 heights -> ETRS89 ellipsoidal heights

*Source*: [Agency for Data Supply and Efficiency](https://github.com/NordicGeodesy/NordicTransformations)  
*Format*: GeoTIFF converted from GTX  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)

Transform local height system DVR90 (EPSG:5799) to ETRS89 ellipsoidal heights (EPSG:4937). The horizontal
grid coordinates are referenced to ETRS89.

* dk_sdfe_dnn.tif

### Faroe Islands: FVR09 heights -> ETRS89 ellipsoidal heights

*Source*: [Agency for Data Supply and Efficiency](https://github.com/NordicGeodesy/NordicTransformations)  
*Format*: GeoTIFF converted from GTX  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)

Transform local height system FVR09 (EPSG:5317) to ETRS89 ellipsoidal heights (EPSG:4937). The horizontal
grid coordinates are referenced to ETRS89.

* dk_sdfe_fvr09.tif

## Included init-files

### Denmark: System definitions related to ETRS89

*Source*: [Agency for Data Supply and Efficiency](https://github.com/NordicGeodesy/NordicTransformations)  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)

Init files with various transformations and conversions of relevance in
Denmark. All definitions in the init file uses the local ETRS89 reference
frame as a pivot datum. More information can be found in the
[NordicTransformations](https://github.com/NordicGeodesy/NordicTransformations)
repository. While the `.pol` files are init-files they are not supposed to be
by themselves. The exist purely as helper files for the `dk_sdfe_DK` init-file.
The `.pol` files holds polynomial constants used for transformations between
Danish legacy coordinate reference systems and ETRS89.

* DK
* dk_sdfe_DK_bornholm.pol
* dk_sdfe_DK_bridges.pol
* dk_sdfe_DK_general.pol
* dk_sdfe_DK_jutland.pol
* dk_sdfe_DK_zealand.pol

### The Faroe Islands: System definitions related to ETRS89

*Source*: [Agency for Data Supply and Efficiency](https://github.com/NordicGeodesy/NordicTransformations)  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)

Init file with various transformations and conversions of relevance in
The Faroe Islands. All definitions in the init file uses the local ETRS89
reference frame as a pivot datum. More information can be found in the
[NordicTransformations](https://github.com/NordicGeodesy/NordicTransformations)
repository.

* FO
