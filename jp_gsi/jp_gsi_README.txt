# jp_gsi_README.txt

The files in this section result from the conversion of datasets originating
from [Geospatial Information Authority of Japan](http://www.gsi.go.jp/)

## Included grids

### JDG2011 (EPSG:6667) -> JDG2011 (vertical) height (EPSG:6695) - GSIGEO2011

*Source*: [Geospatial Information Authority of Japan](https://fgd.gsi.go.jp/download/geoid.php)
*Format*: GeoTIFF converted by `GSIGGEO2011.sh`
*License*: CC-BY 4.0.
*Horizontal CRS*: JDG2011 (EPSG:6667)

Hybrid geoid created by fitting a high-resolution gravimetric geoid model for Japan, “JGEOID2008” to GNSS/leveling geoid undulations at 971 sites by the Least-Squares Collocation method. The standard deviation of the model at the GNSS/leveling sites is 1.8 cm. The geoid height shown in this model is the height over the GRS80-compliant ellipsoid using latitude and longitude values in the Japan Geodetic System 2011 frame.

Note that this grid has a bounding box which is bigger than the declared area of use in its metadata, which is the area of use of JDG2011 (vertical) height. The grid files contains data for the Tokara, Amami, Okinawa, and Sakishima Islands in the Ryukyu Archipelago, the Daitö Islands and the Ogasawara Islands, which all fall out of the area covered by the JDG2011 height (in fact, there isn't any vertical CRS for them in the EPSG catalog).

The number of significant digits of the latitude resolution has been increased compared to the official documentation as it appears to provide better accuracy when results are validated using reference data from https://vldb.gsi.go.jp/sokuchi/surveycalc/geoid/calcgh/calcframe.html
For validation, a few points have been hand-picked from arbitrary locations more or less evenly distributed across
Japan mainland. The results are in the table below (the CRS is JDG2011):

    Lat     Lon      geoid h (m) reference error (mm)
    34.290  135.630  39.860122   39.8601   0.022
    36.103  140.087  40.181748   40.1817   0.048
    43.217  143.129  30.638869   30.6389   -0.031
    38.675  139.886  40.128091   40.1281   -0.009
    36.344  137.654  42.895648   42.8956   0.048
    33.179  130.063  32.303559   32.3036   -0.041
    39.801  141.322  41.886202   41.8862   0.002

The RMS of the error is 0.088 mm.

Derivative work based on gsigeo2011_ver2_1.asc, created with permission:「測量法に基づく国土地理院長承認(使用)R 2JHs 501」

*  jp_gsi_gsigeo2011.tif


### JDG2011 (EPSG:6667) -> JDG2011 (vertical) height (EPSG:6695) - JPGEO2024

*Source*: [Geospatial Information Authority of Japan](https://www.gsi.go.jp)
*Format*: GeoTIFF converted by `build_JPGEO2024.sh`
*License*: CC-BY 4.0.
*Horizontal CRS*: JDG2011 (EPSG:6667)

Vertical transformation for Geoid model JPGEO2024. Used to make the transitions
from heights in vertical CRS JDG2011 (vertical) height (EPSG:6695)
to heights above the ellipsoid in JDG2011 (EPSG:6667).
Official in Japan on 2025-04-01

The accuracy mentioned on the documentation is 3 cm.

Derivative work based on JPGEO2024.isg, created with permission: 測量法に基づく国土地理院長承認（使用）R 7JHs 5

*   jp_gsi_jpgeo2024.tif
