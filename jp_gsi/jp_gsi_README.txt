# jp_gsi_README.txt

The files in this section result from the conversion of datasets originating
from [Geospatial Information Authority of Japan](http://www.gsi.go.jp/)

## Included grids

### JDG2011 (EPSG:6667) -> JDG2011 (vertical) height (EPSG:6695)

*Source*: [Geospatial Information Authority of Japan](https://fgd.gsi.go.jp/download/geoid.php)
*Format*: GeoTIFF converted by `GSIGGEO2011.sh`
*License*: CC-BY 4.0.
*Horizontal CRS*: JDG2011 (EPSG:6667)

Hybrid geoid created by fitting a high-resolution gravimetric geoid model for Japan, “JGEOID2008” to GNSS/leveling geoid undulations at 971 sites by the Least-Squares Collocation method. The standard deviation of the model at the GNSS/leveling sites is 1.8 cm. The geoid height shown in this model is the height over the GRS80-compliant ellipsoid using latitude and longitude values in the Japan Geodetic System 2011 frame.

This grid file is a crop of the original bounding box to a the minimal pixel area that covers the area of use of EPSG:6695: Japan - onshore mainland (EPSG:3263). The data for the Tokara, Amami, Okinawa, and Sakishima Islands in the Ryukyu Archipelago, the Daitö Islands and the Ogasawara Islands has been discarded due to the lack of a vertical coordinate reference system in the EPSG catalog.

Derivative work based on gsigeo2011_ver2_1.asc, created with permission:「測量法に基づく国土地理院長承認(使用)R 2JHs 501」

*  jp_gsi_gsigeo2011_mainland.tif
