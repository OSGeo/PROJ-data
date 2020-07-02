# us_noaa_README.txt

The files in this section result from the conversion of datasets originating
from [US NOAA](https://www.ngs.noaa.gov)

## Included grids

### USA: NAD27 and older CRS -> NAD83

*Source*: [.los/.las files coming from NOAA](https://www.ngs.noaa.gov/PC_PROD/NADCON/NADCON.zip)  
*Format*: GeoTIFF converted from CTable2  
*License*: Public Domain

* us_noaa_alaska.tif - Alaska
* us_noaa_conus.tif - Conterminous U.S.
* us_noaa_hawaii.tif - Hawaii. Old Hawaiian (EPSG:4135) to NAD83
* us_noaa_prvi.tif - Puerto Rico, Virgin Is. Puerto Rico (EPSG:4139) to NAD83
* us_noaa_stgeorge.tif - St. George Is, Alaska. St. George Island (EPSG:4138) to NAD83
* us_noaa_stlrnc.tif - St. Lawrence Is., Alaska. St. Lawrence Island (EPSG:4136) to NAD83
* us_noaa_stpaul.tif - St. Paul Is., Alaska. St. Paul Island (EPSG:4137) to NAD83

### USA: NAD83 -> NAD83 (HARN/HPGN)

*Source*: [.los/.las files coming from NOAA](https://www.ngs.noaa.gov/PC_PROD/NADCON/NADCON.zip)  
*Format*: GeoTIFF converted from NTv2  
*License*: Public Domain

Grid data for high precision conversion of geographic coordinates from
the original NAD83 (1986) (EPSG:4269) to NAD83 High Precision Geodetic Networks
(HPGNs) (EPSG:4152), also referred to as High Accuracy Reference Networks (HARNs).
NAD 83 coordinates based on the HPGN/HARN surveys changed approximately 0.2
to 1.0 meter relative to the original NAD 83 (1986) adjustment.

Those files have been converted to NTv2 grids with the
[build_nad83_harn.sh](https://raw.githubusercontent.com/OSGeo/proj-datumgrid/master/north-america/build_nad83_harn.sh) script.

* us_noaa_*hpgn.tif (51 files)

Also include a few files which are duplicate of *hpgn.tif files, for historic reasons:

* us_noaa_FL.tif - Florida
* us_noaa_MD.tif - Maryland
* us_noaa_TN.tif - Tennessee
* us_noaa_WI.tif - Wisconsin
* us_noaa_WO.tif - Washington, Oregon, N. California

### Continental USA VERTCON: NGVD (19)29 height to NAVD (19)88 height

*Source*: converted from [NOAA VERTCON .94 grids](https://www.ngs.noaa.gov/PC_PROD/VERTCON/)  
*Converter*: vertcon_94_to_gtx.py  
*Format*: GeoTIFF converted from GTX  
*License*: Public Domain

Transform NGVD (19)29 height to NAVD (19)88 height. The .tif files contain
the offset to add to NGVD 29 heights to get NAVD 88 heights.

The horizontal grid coordinates may be referenced to NAD27 or NAD83

* us_noaa_vertconc.tif
* us_noaa_vertcone.tif
* us_noaa_vertconw.tif

### USA GEOID1999 model (superseded): NAVD88 height to NAD83

*Source*: converted from [NOAA NGS .bin grids](https://geodesy.noaa.gov/GEOID/GEOID99/)  
*Converter*: build_g1999.sh  
*Format*: GeoTIFF converted from GTX  
*License*: Public Domain

The GEOID99 model is known as a hybrid geoid model, combining
gravimetric information with GPS ellipsoid heights on leveled bench marks.
The GEOID99 model was developed to support direct conversion between
NAD 83 GPS ellipsoidal heights and NAVD 88 orthometric heights.

It is superseded by later GEOIDxx models

* us_noaa_g1999u01.tif to g1999u08.tif : Conterminous US
* us_noaa_g1999a01.tif to g1999a04.tif : Alaska
* us_noaa_g1999h01.tif : Hawaii
* us_noaa_g1999p01.tif : Puerto Rico

### USA GEOID2003 model (superseded): NAVD88 height to NAD83

*Source*: converted from [NOAA NGS .bin grids](https://geodesy.noaa.gov/GEOID/GEOID03/)  
*Converter*: build_g2003.sh  
*Format*: GeoTIFF converted from GTX  
*License*: Public Domain

The GEOID03 model is known as a hybrid geoid model, combining
gravimetric information with GPS ellipsoid heights on leveled bench marks.
The GEOID03 model was developed to support direct conversion between
NAD 83 GPS ellipsoidal heights and NAVD 88 orthometric heights.

It is superseded by later GEOIDxx models

* us_noaa_geoid03_conus.tif : Conterminous US
* us_noaa_g2003a01.tif to g2003a04.tif : Alaska
* us_noaa_g2003h01.tif : Hawaii
* us_noaa_g2003p01.tif : Puerto Rico

### USA GEOID2006 model (superseded): NAVD88 height to NAD83 (Alaska only)

*Source*: converted from [NOAA NGS .bin grids](https://geodesy.noaa.gov/GEOID/GEOID06/)  
*Converter*: build_g2006.sh  
*Format*: GeoTIFF converted from GTX  
*License*: Public Domain

GEOID06 is a refined hybrid geoid model for Alaska only.

GEOID06 converts between the U.S. ellipsoidal datum, NAD 83, and the U.S.
vertical datum, NAVD 88. GEOID06 is built largely on the USGG2003 gravimetric geoid.

It is superseded by later GEOIDxx models

* us_noaa_geoid06_ak.tif : Alaska

### USA GEOID2009 model (superseded): NAVD88/PRVD02/VIVD09/GUVD04 height to NAD83

*Source*: converted from [NOAA NGS .bin grids](https://www.ngs.noaa.gov/GEOID/GEOID09/)  
*Converter*: build_g2009.sh  
*Format*: GeoTIFF converted from GTX  
*License*: Public Domain

The GEOID09 model is known as a hybrid geoid model, as it is modified
from a gravimetric model to fit GPS ellipsoid heights on leveled bench marks.
The GEOID09 model refers to a GRS-80 shaped ellipsoid,
centered at the NAD83 origin.  It supports direct conversion between
NAD83 GPS ellipsoidal heights and NAVD88, GUVD04 and ASVD03 orthometric heights,
and will support future vertical datums PRVD02 nad VIVD09.

* us_noaa_geoid09_conus.tif : Conterminous US.
* us_noaa_geoid09_ak.tif : Alaska.
* us_noaa_g2009h01.tif : Hawaii
* us_noaa_g2009g01.tif : Guam and Northern Mariana Islands.
* us_noaa_g2009s01.tif : American Samoa.
* us_noaa_g2009p01.tif : Puerto Rico / U.S. Vigin Islands.

### USA GEOID12B model (partial superseded): NAVD88/PRVD02/VIVD09/GUVD04/NMVD03/ASVD02 height to NAD83(2011)/NAD83(MA11)/NAD83(PA11)

*Source*: converted from [NOAA NGS .bin grids](https://www.ngs.noaa.gov/GEOID/GEOID12B/)  
*Converter*: build_g2012.sh  
*Format*: GeoTIFF converted from GTX  
*License*: Public Domain

GEOID12B is a hybrid geoid height model that can transform between the relevant
vertical datum for each region to a NAD 83 ellipsoid height
See https://www.ngs.noaa.gov/GEOID/GEOID12B/faq_2012B.shtml for more details.

* us_noaa_g2012bu0.tif : Conterminous US, referenced to NAD83(2011). Vertical datum: NAVD88
* us_noaa_g2012ba0.tif : Alaska, referenced to NAD83(2011). Vertical datum: NAVD88
* us_noaa_g2012bh0.tif : Hawaii, referenced to NAD83(PA11). Vertical datum: identical to that of USGG2012, which is offset by 50-60 cm from some Local Tidal bench mark values. 
* us_noaa_g2012bg0.tif : Guam and Northern Mariana Islands, referenced to NAD83(PA11). Vertical datum: GUVD04/NMVD03
* us_noaa_g2012bs0.tif : American Samoa, referenced to NAD83 (PA11). Vertical datum: ASVD02
* us_noaa_g2012bp0.tif : Puerto Rico / U.S. Vigin Islands, referenced to NAD83(2011). Vertical datum: PRVD02 and VIVD09

The us_noaa_g2012bu0.tif and us_noaa_g2012bp0.tif grids are superseded by the
us_noaa_g2018p0.tif and us_noaa_g2018p0.tif grids of GEOID18.

### USA GEOID18 model: NAVD88/PRVD02 height to NAD83(2011)

*Source*: converted from [NOAA NGS .bin grids](https://www.ngs.noaa.gov/GEOID/GEOID18/)  
*Converter*: build_g2018.sh  
*Format*: GeoTIFF converted from GTX  
*License*: Public Domain

GEOID18 is intended for use with coordinates in the North American Datum of 1983 (2011)
[NAD 83 (2011) epoch 2010.00]. It provides orthometric heights consistent with the
North American Vertical Datum of 1988 (NAVD 88), the Puerto Rico Vertical Datum of
2002 (PRVD02), or the Virgin Islands Vertical Datum of 2009 (VIVD09).

GEOID18 covers CONUS, Puerto Rico, and the U.S. Virgin Islands and supersedes
GEOID12B in these regions. GEOID18 does NOT cover Alaska, Hawaii, Guam and the
Commonwealth of the Northern Mariana Islands (CNMI) where users should continue
to use GEOID12B.

* us_noaa_g2018u0.tif : Conterminous US, referenced to NAD83(2011). Vertical datum: NAVD88
* us_noaa_g2018p0.tif : Puerto Rico / U.S. Vigin Islands, referenced to NAD83(2011). Vertical datum: PRVD02 and VIVD09
