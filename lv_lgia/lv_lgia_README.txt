# lv_lgia_README.txt

The files in this section result from the conversion of datasets originating
from [Latvian Geospatial Information Agency](https://www.lgia.gov.lv/)

## Included grids

### LKS92 (EPSG:4949) -> Latvia 2000 height (EPSG:7700)

*Source*: [Latvian Geospatial Information Agency](https://www.lgia.gov.lv/en/latvian-quasi-geoid-model)
*Format*: GeoTIFF converted by standard GDAL functions and optimized by grid_tools scripts
*License*: CC-BY 4.0.
*Horizontal CRS*: LKS92 (EPSG:4949)

As of December 1, 2014, the Latvian Geospatial Information Agency (LGIA) released the new quasi-geoid model, LV′14.

The validation of this quasi-geoid model was carried out by comparing its empirical height anomalies with those obtained from field measurements. These elevation anomalies are critical for geodetic software when transitioning from geodetic (ellipsoidal) to normal heights, and they are used in both global positioning systems and data processing applications.

For validation, the 1st and 2nd class leveling network points, where global positioning was performed through post-processing, showed a standard deviation of height anomalies against the measured points within one sigma of up to 14 mm.

The maximum height anomaly difference at the reference points reached up to 53 mm.

For the leveling points in the validation network, where real-time global positioning measurements were taken, the maximum standard deviation within one sigma was up to 22 mm, with elevation anomaly differences reaching up to 65 mm.

The validation results in both post-processing and real-time modes indicate that the accuracy of the LV′14 quasi-geoid model is sufficient for acquiring fundamental geospatial data needed to support state and municipal functions and tasks.

*  lv_lgia_lv14.tif

### LKS-92 (EPSG:4661) -> LKS-2020 (EPSG:10305)

*Source*: [Latvian Geospatial Information Agency](https://www.lgia.gov.lv/en/node/1384)
*Format*: GTG converted using PROJ-data grid grid_tools
*License*: CC-BY 4.0

Transform coordinates from LKS-92 to LKS-2020.

*  lv_lgia_lks92to2020.tif
