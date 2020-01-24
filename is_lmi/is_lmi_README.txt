# is_lmi_README.txt

The files in this section result from the conversion of datasets originating
from [National Land Survey of Iceland](https://atlas.lmi.is/LmiData/index.php?id=626468364600)

## Included grids

### Iceland: ISN93 -> ISN2016

2D geodetic transformation from Iceland Datum ISN93 to Iceland Datum ISN2016

*Source*: [National Land Survey of Iceland](https://atlas.lmi.is/LmiData/index.php?id=626468364600)  
*Format*: GeoTIFF converted from NTv2  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)  
*Credit*: (c)2017-2019 Grid created by Guðmundur Valsson.

The transformation is designed so that the ISN2016 points should fit within 1-2 cm accuracy, but in the area around the earthquake area in the South and North of Vatnajökull the accuracy is worse.

Recommended to transform from ISN93 2D geodetic (EPSG:4659) to ISN2016 2D geodetic (EPSG:8086), also this transformation has code in EPSG Dataset (EPSG:9232)

* is_lmi_ISN93_ISN2016.tif

### Iceland: ISN2004 -> ISN2016

2D geodetic transformation from Iceland Datum ISN2004 to Iceland Datum ISN2016

*Source*: [National Land Survey of Iceland](https://atlas.lmi.is/LmiData/index.php?id=626468364600)  
*Format*: GeoTIFF converted from NTv2  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)  
*Credit*: (c)2017-2019 Grid created by Guðmundur Valsson.

The transformation is designed so that the ISN2016 points should fit within 1-2 cm accuracy, but in the area around the earthquake area in the South and North of Vatnajökull the accuracy is worse.

Recommended to transform from ISN2004 2D geodetic (EPSG:5324) to ISN2016 2D geodetic (EPSG:8086), also this transformation has code in EPSG Dataset (EPSG:9233)

* is_lmi_ISN2004_ISN2016.tif

### Iceland: ISN2004 ellipsoidal height  -> ISH2004 vertical datum

*Source*: [National Land Survey of Iceland](https://atlas.lmi.is/LmiData/index.php?id=626468364600)  
*Format*: GeoTIFF converted from GTX  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)  
*Credit*: (c)2017-2019 Grid created by Guðmundur Valsson.

Geoid created in cooperation between the National Land Survey of Iceland and DTU Space in  December 2010. 
A gravimetric geoid was fitted to National Height System ISH2004 (EPSG:8089) with over 300 GNSS levelling points
with ellipsoidal height in ISN2004 (EPSG:5323). The std. of the fit was 1.7 cm.

Grid to convert from ISN2004 ellipsoidal height (EPSG:5323) to national vertical datum ISH2004 (EPSG:8089)
The horizontal grid coordinates are referenced to ISN2004

See the `ISL` init-file for examples of use.

* is_lmi_Icegeoid_ISN2004.tif 

### Iceland: ISN93 ellipsoidal height  -> ISH2004 vertical datum

*Source*: [National Land Survey of Iceland](https://atlas.lmi.is/LmiData/index.php?id=626468364600)  
*Format*: GeoTIFF converted from GTX  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)  
*Credit*: (c)2017-2019 Grid created by Guðmundur Valsson.

Icegeoid_ISN2004.tif plus corrections for vertical difference between ISN93(EPSG:4945) and ISN2004 (EPSG:5323).

Grid to convert from ISN93 ellipsoidal height (EPSG:4945) to national vertical datum ISH2004 (EPSG:8089)
The horizontal grid coordinates are referenced to ISN93

See the `ISL` init-file for examples of use.

* is_lmi_Icegeoid_ISN93.tif

### Iceland: ISN2016 ellipsoidal height  -> ISH2004 vertical datum

*Source*: [National Land Survey of Iceland](https://atlas.lmi.is/LmiData/index.php?id=626468364600)  
*Format*: GeoTIFF converted from GTX  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)  
*Credit*: (c)2017-2019 Grid created by Guðmundur Valsson.

Icegeoid_ISN2004.tif plus corrections for vertical difference between ISN2016(EPSG:8085) and ISN2004 (EPSG:5323).

Grid to convert from ISN2016 ellipsoidal height (EPSG:8085) to national vertical datum ISH2004 (EPSG:8089)
The horizontal grid coordinates are referenced to ISN2016

See the `ISL` init-file for examples of use.

* Icegeoid_ISN2016.tif

### Iceland: Velocity Model

*Source*: [National Land Survey of Iceland](https://atlas.lmi.is/LmiData/index.php?id=626468364600)  
*Format*: GeoTIFF converted from CTable2 and GTX  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)  
*Credit*: (c)2017-2019 Grid created by Guðmundur Valsson.

Used in transformations between ISN2016 and global reference frame realisation ITRF2014 with different epochs, 
also transformation between different epochs within ITRF2014 frame.

See the `ISL` init-file for examples of use.

* is_lmi_ISN_vel_beta.tif

## Included init-files

### Iceland: System definitions

*Source*: [National Land Survey of Iceland](https://atlas.lmi.is/LmiData/index.php?id=626468364600)  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)  

Init file with various transformations and conversions of relevance in Iceland.

* ISL
