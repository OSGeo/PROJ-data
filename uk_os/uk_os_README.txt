# uk_os_README.txt

The files in this section result from the conversion of datasets originating
from [Ordnance Survey](https://www.ordnancesurvey.co.uk)

## Included grids

### Ireland: OSGM15 height, Malin head datum -> ETRS89 ellipsoidal heights

*Source*: [Ordnance Survey](https://www.ordnancesurvey.co.uk/business-and-government/help-and-support/navigation-technology/os-net/formats-for-developers.html)  
*Format*: GeoTIFF converted from GTX  
*License*: [The 2-Clause BSD License](https://opensource.org/licenses/bsd-license.php)  

Vertical transformation for Geoid model OSGM15, Malin head datum (EPSG:5731). Used in
transformation from OSGM15 orthometric heights to WGS84/ETRS89 ellipsoidal heights.
The Malin Head datum is used in the Republic of Ireland.

* uk_os_OSGM15_Malin.tif

### Northern Ireland: OSGM15 height, Belfast height -> ETRS89 ellipsoidal heights

*Source*: [Ordnance Survey](https://www.ordnancesurvey.co.uk/business-and-government/help-and-support/navigation-technology/os-net/formats-for-developers.html)  
*Format*: GeoTIFF converted from GTX  
*License*: [The 2-Clause BSD License](https://opensource.org/licenses/bsd-license.php)  

Vertical transformation for Geoid model OSGM15, Belfast datum (EPSG:5732). Used in
transformation from OSGM15 orthometric heights to WGS84/ETRS89 ellipsoidal heights.
The Belfast datum is used in the Northern Ireland.

* uk_os_OSGM15_Belfast.tif

### United Kingdom: OSGM15 height, ODN height -> ETRS89 ellipsoidal heights

*Source*: [Ordnance Survey](https://www.ordnancesurvey.co.uk/business-and-government/help-and-support/navigation-technology/os-net/formats-for-developers.html)
*Format*: GeoTIFF converted by `OSGM15_GB.sh`
*License*: [The 2-Clause BSD License](https://opensource.org/licenses/bsd-license.php)

Vertical transformation for Geoid model OSGM15, ODN height (EPSG:5701). Used in
transformation from OSGM15 orthometric heights to ETRS89 ellipsoidal heights.
The Belfast datum is used in the Great Britain mainland onshore.

Since the original transformation should have applied to projected coordinates, this geoid model
was reprojected to suit PROJ requirements in order to be able to apply it to geographic coordinates.
Due to this reprojection, slight inaccuracy in addition to the existing transformation inaccuracy can
appear.
Compared to the Ordnance Survey developer pack test data, the additional error is up to 0.002m
and RMSE is up to 0.00076m.

* uk_os_OSGM15_GB.tif

### United Kingdom: OSGB36 -> ETRS89

*Source*: [Ordnance Survey](https://www.ordnancesurvey.co.uk/business-and-government/help-and-support/navigation-technology/os-net/formats-for-developers.html)  
*Format*: GeoTIFF converted from NTv2  
*License*: [The 2-Clause BSD License](https://opensource.org/licenses/bsd-license.php)

OSTN15 is the definitive OSGB36/ETRS89 transformation. OSTN15 in combination with the ETRS89
coordinates of the OS Net stations, rather than the old triangulation network, define the National
Grid. This means that, for example, the National Grid coordinates of an existing OSGB36 point,
refixed using GNSS from OS Net and OSTN15, will be the correct ones. The original archived
OSGB36 National Grid coordinates of the point (if different) will be wrong, by definition, but the
two coordinates (new and archived) will agree on average to better than 0.1m (0.1m rmse, 68%
probability).

* uk_os_OSTN15_NTv2_OSGBtoETRS.tif
