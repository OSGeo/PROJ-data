# au_ga_README.txt

The files in this section result from the conversion of datasets originating
from [Geoscience Australia](http://www.ga.gov.au)

### Australia: AUSGeoid98: GDA94 -> AHD height

*Source*: [Geoscience Australia](http://www.ga.gov.au/ausgeoid/comp.html)  
*Format*: GeoTIFF converted from GTX  
*License*: [Creative Commons Attribution 4.0]  
*Converter*: gdal_translate -of GTX AUSGeoid98.gsb AUSGeoid98.gtx -b 1 

* au_ga_AUSGeoid98.tif

### Australia: AUSGeoid09: GDA94 -> AHD height

*Source*: [Geoscience Australia](http://www.ga.gov.au/ausgeoid/comp.html)  
*Format*: GeoTIFF converted from GTX  
*License*: [Creative Commons Attribution 4.0]  
*Converter*: gdal_translate -of GTX AUSGeoid09_V1.01.gsb AUSGeoid09_V1.01.gtx -b 1 

Uses AusGeoid09 model which uses bi-cubic interpolation; bi-linear interpolation
of the grid file will give results agreeing to within 1cm 99.97% of the time.

* au_ga_AUSGeoid09_V1.01.tif

### Australia: AUSGeoid2020: GDA2020 -> AHD height

*Source*: [Geoscience Australia](http://www.ga.gov.au/ausgeoid/comp.html)  
*Format*: GeoTIFF converted from GTX  
*License*: [Creative Commons Attribution 4.0]  
*Converter*: gdal_translate AUSGeoid2020_20180201.gsb tmp.tif -a_nodata -999 -b 1 && gdalwarp tmp.tif AUSGeoid2020_20180201.gtx -dstnodata -88.8888015747070312 -of GTX

Uses AusGeoid2020 model.

* au_ga_AUSGeoid2020_20180201.tif

### Australia: AGQG (version 20191107): GDA2020 -> AVWS height

*Removed*: in PROJ-data v1.7 (use v1.6 to get it). Superseded by au_ga_AGQG_20201120.tif

*Source*: [Geoscience Australia](https://www.icsm.gov.au/sites/default/files/2020-08/AVWS%20Technical%20Implementation%20Plan_V1.2.pdf)  
*Format*: GeoTIFF converted from source GeoTIFF  
*License*: [Creative Commons Attribution 4.0]  

* au_ga_AGQG_20191107.tif

### Australia: AGQG (version 20201120): GDA2020 -> AVWS height

*Source*: [Geoscience Australia](https://icsm.gov.au/sites/default/files/2020-12/AVWS%20Technical%20Implementation%20Plan_V1.3_0.pdf)  
*Format*: GeoTIFF converted from source GeoTIFF  
*License*: [Creative Commons Attribution 4.0]  

* au_ga_AGQG_20201120.tif


[Creative Commons Attribution 4.0]: https://creativecommons.org/licenses/by/4.0/
