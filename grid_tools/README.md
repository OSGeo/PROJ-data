# Grid tools

This directory contains a set of Python scripts to convert grids to
the [Geodetic TIFF grids (GTG)](https://github.com/OSGeo/PROJ/blob/master/docs/source/specifications/geodetictiffgrids.rst),
and check them

## Requirements

GDAL >= 3.1 (currently master) is required to write geoid models with GeoTIFF 1.1
encoding of Geographic 3D CRS. Otherwise, GDAL 2.4/3.0 can be used to produce
horizontal shift grids.

The "osgeo/gdal:alpine-normal-latest" docker image documented at
https://github.com/OSGeo/gdal/tree/master/gdal/docker can be used for that purpose
(the default "osgeo/gdal" can also be used. It is larger, using a Ubuntu base, whereas
"osgeo/gdal" uses a smaller Alpine Linux base)

For Windows, the development version of [GisInternals builds](http://gisinternals.com/development.php)
can also be used. Or the "gdal-dev-python" package of [OSGeo4W](https://trac.osgeo.org/osgeo4w/)

Python 3 is suggested, but the scripts should still be compatible of Python 2.7

## Converting from NTv2 to GTG

With the [ntv2_to_gtiff.py](ntv2_to_gtiff.py) script.

Usage:
```
usage: ntv2_to_gtiff.py [-h] --source-crs SOURCE_CRS --target-crs TARGET_CRS
                        --copyright COPYRIGHT [--description DESCRIPTION]
                        [--do-not-write-accuracy-samples]
                        [--positive-longitude-shift-value {east,west}]
                        [--uint16-encoding] [--datetime DATETIME]
                        [--accuracy-unit {arc-second,metre,unknown}]
                        [--area-of-use AREA_OF_USE]
                        source dest
```

Options:

* --source-crs SOURCE_CRS: the source CRS, as a "EPSG:XXXX" value or a CRS WKT string. Mandatory. Must be a Geographic 2D CRS.
* --target-crs SOURCE_CRS: the target CRS, as a "EPSG:XXXX" value or a CRS WKT string. Mandatory. Must be a Geographic 2D CRS.
* --copyright COPYRIGHT: Attribution and license to be stored in the TIFF Copyright tag. Mandatory
* --area-of-use AREA_OF_USE: To specify a textual area of use for the grid. For example "France", "Germany - Saxony". Strongly recommended.
* --description DESCRIPTION: Text describing the grid. If not provided, a default value will be automatically set.
                             For example "NAD27 (EPSG:4267) to NAD83 (EPSG:4269). Converted from ntv2_0.gsb (last updated on 1995-07-05)"
* --do-not-write-accuracy-samples: To prevent accuracy samples from the NTv2 grid to be written in the output. Note: if it is detected that those samples are set to dummy values (negative values), they will automatically be discarded
* --positive-longitude-shift-value {east,west}: To force the convention for the longitude shift value. NTv2 uses a positive-is-west convention, that is confusing. By default, the script will negate the sign of the longitude shift values to output a positive-is-east convention. Setting this option to "west" will preserve the original convention. Not recommended
* --uint16-encoding: Whether values should be encoded on a 16-bit unsigned value, using a offset and scale floating point values. Default behaviour is to use Float32 encoding, which will preserve the binary values of the original NTv2 file
* --datetime DATETIME: to specify the value of the TIFF DateTime tag. Must be formatted as "YYYY:MM:DD HH:MM:SS" (note the use of colon as the separator for the Y-M-D part, as mandated by the TIFF specification). If not specified, the script will try to use the value from the corresponding NTv2 header
* --accuracy-unit {arc-second,metre,unknown}: to specify the unit of the accuracy samples. The NTv2 specification has been [historically interpreted in different ways regarding that](https://github.com/OSGeo/PROJ/wiki/Units-of-NTv2-accuracy-samples-%3F). Mandatory if accuracy samples are written (the script contains a few hardcoded rules for known datasets)

Example:

```
python3 ntv2_to_gtiff.py \
    --area-of-use "Canada" \
    --copyright "Derived from work by Natural Resources Canada. Open Government Licence - Canada: http://open.canada.ca/en/open-government-licence-canada" \
    --source-crs EPSG:4267 \
    --target-crs EPSG:4269 \
    ntv2_0.gsb ca_nrc_ntv2_0.tif
```

Using the Docker image:

```
docker run --rm -v /home:/home osgeo/gdal:alpine-normal-latest python3 $PWD/ntv2_to_gtiff.py  \
    --area-of-use "Canada" \
    --copyright "Derived from work by Natural Resources Canada. Open Government Licence - Canada: http://open.canada.ca/en/open-government-licence-canada" \
    --source-crs EPSG:4267 \
    --target-crs EPSG:4269 \
    $PWD/ntv2_0.gsb $PWD/ca_nrc_ntv2_0.tif
```

## Converting from GTX to GTG

With the [vertoffset_grid_to_gtiff.py](vertoffset_grid_to_gtiff.py) script.

Usage:
```
usage: vertoffset_grid_to_gtiff.py [-h] --type
                                   {GEOGRAPHIC_TO_VERTICAL,VERTICAL_TO_VERTICAL}
                                   --source-crs SOURCE_CRS
                                   [--interpolation-crs INTERPOLATION_CRS]
                                   --target-crs TARGET_CRS --copyright
                                   COPYRIGHT [--description DESCRIPTION]
                                   [--encoding {float32,uint16,int32-scale-1-1000}]
                                   [--ignore-nodata] [--datetime DATETIME]
                                   [--area-of-use AREA_OF_USE]
                                   source dest
```


Options:
* --type {GEOGRAPHIC_TO_VERTICAL,VERTICAL_TO_VERTICAL}: specify the type of the grid. GEOGRAPHIC_TO_VERTICAL is for geoid-like grids transforming between a vertical CRS and ellipsoid heights. The value in the grid must be the offset to add to the height in the vertical CRS to get an ellipsoidal height. VERTICAL_TO_VERTICAL is for transformations between 2 vertical CRS: the value in the grid must be the offset to add to heights in the source CRS to get heights in the target CRS.
* --source-crs SOURCE_CRS: the source CRS, as a "EPSG:XXXX" value or a CRS WKT string. Mandatory. For type=GEOGRAPHIC_TO_VERTICAL, this must be a Geographic 3D CRS. For type=VERTICAL_TO_VERTICAL, this must be a Vertical CRS.
* --interpolation-crs INTERPOLATION_CRS: the geographic CRS in which the grid is referenced to. This is ignored for type=GEOGRAPHIC_TO_VERTICAL (the interpolation CRS is the source CRS), but mandatory for type=VERTICAL_TO_VERTICAL
* --target-crs SOURCE_CRS: the target CRS, as a "EPSG:XXXX" value or a CRS WKT string. Mandatory. Must be a vertical CRS.
* --area-of-use AREA_OF_USE: To specify a textual area of use for the grid. For example "France", "Germany - Saxony". Strongly recommended.
* --description DESCRIPTION: Text describing the grid. If not provided, a default value will be automatically set.
                             For example "NAD27 (EPSG:4267) to NAD83 (EPSG:4269). Converted from ntv2_0.gsb (last updated on 1995-07-05)"
* --encoding {float32,uint16,int32-scale-1-1000}: How values should be encoded. Defaults to float32. If specifying uint16, values will be encoded on a 16-bit unsigned value, using a offset and scale floating point values. If specifying int32-scale-1-1000, values will be conded on a 32-bit signed integer with a scaling factor of 1000 (this is the encoding naturally used by the .byn format of Canadian vertical shift grids)
* --ignore-nodata: whether the nodata value from the source should be encoded. This might be useful because there is an ambiguity for the GTX format. In some circumstances, the -88.8888 value must be interpreted as a nodata value, in others as a valid value. If not specifying this option, the script will print a warning if encountering a grid value that matches the nodata value, so as to call for manual verification.
* --datetime DATETIME: to specify the value of the TIFF DateTime tag. Must be formatted as "YYYY:MM:DD HH:MM:SS" (note the use of column as the separator for the Y-M-D part, as mandated by the TIFF specification). If not specified, the script will use the modification date of the source file.

Example:

```
python3 vertoffset_grid_to_gtiff.py \
    --type GEOGRAPHIC_TO_VERTICAL \
    --area-of-use "World" \
    --source-crs EPSG:4326 \
    --target-crs EPSG:5773 \
    --copyright "Public Domain. Derived from work at http://earth-info.nga.mil/GandG/wgs84/gravitymod/egm96/egm96.html" \
    egm96_15.gtx us_nga_egm96_15.tif 
```

Using the Docker image:

```
docker run --rm -v /home:/home osgeo/gdal:alpine-normal-latest python3 $PWD/vertoffset_grid_to_gtiff.py \
    --type GEOGRAPHIC_TO_VERTICAL \
    --area-of-use "World" \
    --source-crs EPSG:4326 \
    --target-crs EPSG:5773 \
    --copyright "Public Domain. Derived from work at http://earth-info.nga.mil/GandG/wgs84/gravitymod/egm96/egm96.html" \
    $PWD/egm96_15.gtx $PWD/us_nga_egm96_15.tif
```

## Checking compliance of GeoTIFF files with the GTG specification

With the [check_gtiff_grid.py](check_gtiff_grid.py) script.

Usage:
```
usage: check_gtiff_grid.py [-h] filename
```

If the script outputs anything and return the success error code, then everything
is perfect.

Otherwise, it will messages among one of the three following categories:

* information: optional metadata missing, or extra metadata elements found. No corrective action is required
* warning: the file will probably be read correctly by PROJ, but corrective action may be required. Adressing those warnings is recommended
* error: the file will not be read correctly by PROJ. Corrective action is required. The return code of the script will be an error code.

Example of output on non-conformant file:
```
/home/even/gdal/git/gdal/gdal/byte.tif is NOT a valid PROJ GeoTIFF file.
The following errors were found (corrective action is required):
 - CRS found, but not a Geographic CRS
 - Datatype Byte of band 1 is not support

The following warnings were found (the file will probably be read correctly by PROJ, but corrective action may be required):
 - This file uses a RasterTypeGeoKey = PixelIsArea convention. While this will work properly with PROJ, a georeferencing using RasterTypeGeoKey = PixelIsPoint is more common.
 - Missing TYPE metadata item
 - GDAL area_of_use metadata item is missing. Typically used to capture plain text information about where the grid applies
 - TIFF tag ImageDescription is missing. Typically used to capture plain text information about what the grid does
 - TIFF tag Copyright is missing. Typically used to capture information on the source and licensing terms
 - TIFF tag DateTime is missing. Typically used to capture when the grid has been generated/converted
 - Image is uncompressed. Could potentially benefit from compression

The following informative message are issued (no corrective action required):
 - Metadata LAYER_TYPE=athematic on band 1 ignored
```

## Optimize an existing GeoTIFF file

With the [cloud_optimize_gtiff.py](cloud_optimize_gtiff.py) script.

Usage:
```
usage: cloud_optimize_gtiff.py [-h] source dest
```

This file takes an existing GeoTIFF file and optimize its layout, so that
headers are put at the beginning of the file. This is used internally by the
ntv2_to_gtiff.py and vertoffset_grid_to_gtiff.py script

This can be useful as the final step if preparing a file with the GDAL API / tools
such as [gdal_translate](https://gdal.org/programs/gdal_translate.html) or
[gdal_edit.py](https://gdal.org/programs/gdal_edit.html)

Note: this script will not compress data. This must be done in a prior step.
