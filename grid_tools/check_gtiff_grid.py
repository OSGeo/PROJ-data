#!/usr/bin/env python
###############################################################################
# $Id$
#
#  Project:  PROJ
#  Purpose:  Check that a GeoTIFF grid meets the requirements/recommendation of RFC4
#  Author:   Even Rouault <even.rouault at spatialys.com>
#
###############################################################################
#  Copyright (c) 2019, Even Rouault <even.rouault at spatialys.com>
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included
#  in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
###############################################################################

from osgeo import gdal
from osgeo import osr
import argparse
import datetime
import re
import sys


def get_args():
    parser = argparse.ArgumentParser(
        description='Check a PROJ GeoTIFF.')
    parser.add_argument('filename',
                        help='GeoTIFF file')

    return parser.parse_args()


def get_srs(ds, epsg_code_key, wkt_key, is_first_subds, infos, warnings, errors):

    epsg_code = ds.GetMetadataItem(epsg_code_key)
    wkt = None
    if epsg_code:
        try:
            epsg_code = int(epsg_code)
        except ValueError:
            epsg_code = None
            warnings.append('%s=%s is not a valid EPSG code' %
                            (epsg_code_key, epsg_code))
    else:
        wkt = ds.GetMetadataItem(wkt_key)
        if not wkt and is_first_subds:
            warnings.append('Missing %s / %s' % (epsg_code_key, wkt_key))

    srs = None
    if epsg_code:
        srs = osr.SpatialReference()
        if srs.ImportFromEPSG(epsg_code) != 0:
            errors.append('%s=%s is not a valid EPSG code' %
                          (epsg_code_key, str(epsg_code)))
    elif wkt:
        srs = osr.SpatialReference()
        if srs.ImportFromWkt(wkt) != 0:
            errors.append('%s=%s is invalid' % (wkt_key, wkt))

    return srs


def validate_horizontal_offset(ds, is_first_subds):

    infos = []
    warnings = []
    errors = []

    target_crs = get_srs(ds, 'target_crs_epsg_code', 'target_crs_wkt',
                         is_first_subds, infos, warnings, errors)
    if target_crs:
        if not target_crs.IsGeographic():
            warnings.append("target_crs found, but not a Geographic CRS")

    if ds.RasterCount < 2:
        return infos, warnings, ["TYPE=HORIZONTAL_OFFSET should have at least 2 bands"]

    lat_offset_idx = 0
    lon_offset_idx = 0
    lat_accuracy_idx = 0
    lon_accuracy_idx = 0
    for i in range(ds.RasterCount):
        b = ds.GetRasterBand(i+1)
        desc = b.GetDescription()
        if desc == 'latitude_offset':
            if lat_offset_idx > 0:
                return infos, warnings, ["At least, 2 bands are tagged with Description = latitude_offset"]
            lat_offset_idx = i+1
        elif desc == 'longitude_offset':
            if lon_offset_idx > 0:
                return infos, warnings, ["At least, 2 bands are tagged with Description = longitude_offset"]
            lon_offset_idx = i+1
        elif desc == 'latitude_offset_accuracy':
            lat_accuracy_idx = i+1
        elif desc == 'longitude_offset_accuracy':
            lon_accuracy_idx = i+1
        elif desc:
            infos.append('Band of type %s not recognized by PROJ' % desc)

    if lat_offset_idx > 0 and lon_offset_idx > 0:
        if lat_offset_idx != 1 or lon_offset_idx != 2:
            infos.append(
                'Usually the first band should be latitude_offset and the second longitude_offset.')
    elif lat_offset_idx > 0 or lon_offset_idx > 0:
        return infos, warnings, ["One of the band is tagged with Description = latitude_offset/longitude_offset but not the other one"]
    else:
        if is_first_subds:
            warnings.append(
                'No explicit bands tagged with Description = latitude_offset and longitude_offset. Assuming first one is latitude_offset and second one longitude_offset')
        lat_offset_idx = 1
        lon_offset_idx = 2

    for idx in (lat_offset_idx, lon_offset_idx):
        band = ds.GetRasterBand(idx)
        if band.GetNoDataValue():
            warnings.append(
                "One of latitude_offset/longitude_offset band has a nodata setting. Nodata for horizontal shift grids is ignored by PROJ")
        units = band.GetUnitType()
        if not units:
            if is_first_subds:
                warnings.append(
                    "One of latitude_offset/longitude_offset band is missing units description. arc-second will be assumed")
        elif units not in ('arc-second', 'arc-seconds per year', 'degree', 'radians'):
            errors.append(
                "One of latitude_offset/longitude_offset band is using a unit not supported by PROJ")

    positive_value = ds.GetRasterBand(
        lon_offset_idx).GetMetadataItem('positive_value')
    if not positive_value:
        if is_first_subds:
            warnings.append(
                "The latitude_offset band should include a positive_value=west/east metadata item, to avoid any ambiguity w.r.t NTv2 original convention. 'east' will be assumed")
    elif positive_value not in ('west', 'east'):
        errors.append("positive_value=%s not supported by PROJ" %
                      positive_value)

    if lat_accuracy_idx > 0 and lon_accuracy_idx > 0:
        if lat_accuracy_idx != 3 or lon_accuracy_idx != 4:
            infos.append(
                'Usually the third band should be latitude_offset_accuracy and the fourth longitude_offset_accuracy.')
    elif lat_accuracy_idx > 0 or lon_accuracy_idx > 0:
        warnings.append(
            "One of the band is tagged with Description = latitude_offset_accuracy/longitude_offset_accuracy but not the other one")
    elif ds.RasterCount >= 4:
        lat_accuracy_idx = 3
        lon_accuracy_idx = 4

    if lat_accuracy_idx > 0 and lon_accuracy_idx > 0:
        for idx in (lat_accuracy_idx, lon_accuracy_idx):
            if idx == 0:
                continue
            units = ds.GetRasterBand(idx).GetUnitType()
            if not units:
                if is_first_subds:
                    warnings.append(
                        "One of latitude_offset_accuracy/longitude_offset_accuracy band is missing units description.")
            elif units not in ('arc-second', 'arc-seconds per year', 'degree', 'radians', 'metre', 'unknown'):
                errors.append(
                    "One of latitude_offset_accuracy/longitude_offset_accuracy band is using a unit not supported by PROJ")

    return infos, warnings, errors


def validate_vertical_offset_geographic_to_vertical(ds, is_first_subds):

    infos = []
    warnings = []
    errors = []

    target_crs = get_srs(ds, 'target_crs_epsg_code', 'target_crs_wkt',
                         is_first_subds, infos, warnings, errors)
    if target_crs:
        if not target_crs.IsVertical():
            errors.append("target_crs found, but not a Vertical CRS")

    offset_idx = 0
    for i in range(ds.RasterCount):
        b = ds.GetRasterBand(i+1)
        desc = b.GetDescription()
        if desc == 'geoid_undulation':
            if offset_idx > 0:
                return infos, warnings, ["At least, 2 bands are tagged with Description = geoid_undulation"]
            offset_idx = i+1
        elif desc:
            infos.append('Band of type %s not recognized by PROJ' % desc)

    if offset_idx == 0:
        if is_first_subds:
            warnings.append(
                'No explicit band tagged with Description = geoid_undulation. Assuming first one')
        offset_idx = 1

    units = ds.GetRasterBand(offset_idx).GetUnitType()
    if not units:
        if is_first_subds:
            warnings.append(
                "geoid_undulation band is missing units description. Metre will be assumed")
    elif units not in ('metre', ):
        errors.append(
            "geoid_undulation band is using a unit not supported by PROJ")

    return infos, warnings, errors


def validate_vertical_offset_vertical_to_vertical(ds, is_first_subds):

    infos = []
    warnings = []
    errors = []

    source_crs = get_srs(ds, 'source_crs_epsg_code', 'source_crs_wkt',
                         is_first_subds, infos, warnings, errors)
    if source_crs:
        if not source_crs.IsVertical():
            errors.append("source_crs found, but not a Vertical CRS")

    target_crs = get_srs(ds, 'target_crs_epsg_code', 'target_crs_wkt',
                         is_first_subds, infos, warnings, errors)
    if target_crs:
        if not target_crs.IsVertical():
            errors.append("target_crs found, but not a Vertical CRS")

    offset_idx = 0
    for i in range(ds.RasterCount):
        b = ds.GetRasterBand(i+1)
        desc = b.GetDescription()
        if desc == 'vertical_offset':
            if offset_idx > 0:
                return infos, warnings, ["At least, 2 bands are tagged with Description = vertical_offset"]
            offset_idx = i+1
        elif desc:
            infos.append('Band of type %s not recognized by PROJ' % desc)

    if offset_idx == 0:
        if is_first_subds:
            warnings.append(
                'No explicit band tagged with Description = vertical_offset. Assuming first one')
        offset_idx = 1

    units = ds.GetRasterBand(offset_idx).GetUnitType()
    if not units:
        if is_first_subds:
            warnings.append(
                "vertical_offset band is missing units description. Metre will be assumed")
    elif units not in ('metre', ):
        errors.append(
            "vertical_offset band is using a unit not supported by PROJ")

    return infos, warnings, errors


def validate_geocentric_translation(ds, is_first_subds):

    infos = []
    warnings = []
    errors = []

    source_crs = get_srs(ds, 'source_crs_epsg_code', 'source_crs_wkt',
                         is_first_subds, infos, warnings, errors)
    if source_crs:
        if not source_crs.IsGeocentric():
            errors.append("source_crs found, but not a geocentric CRS")

    target_crs = get_srs(ds, 'target_crs_epsg_code', 'target_crs_wkt',
                         is_first_subds, infos, warnings, errors)
    if target_crs:
        if not target_crs.IsGeocentric():
            errors.append("target_crs found, but not a geocentric CRS")

    if ds.RasterCount < 3:
        return infos, warnings, ["TYPE=GEOCENTRIC_TRANSLATION should have at least 3 bands"]

    x_idx = 0
    y_idx = 0
    z_idx = 0
    for i in range(ds.RasterCount):
        b = ds.GetRasterBand(i+1)
        desc = b.GetDescription()
        if desc == 'x_translation':
            if x_idx > 0:
                return infos, warnings, ["At least, 2 bands are tagged with Description = x_translation"]
            x_idx = i+1
        elif desc == 'y_translation':
            if y_idx > 0:
                return infos, warnings, ["At least, 2 bands are tagged with Description = y_translation"]
            y_idx = i+1
        elif desc == 'z_translation':
            if z_idx > 0:
                return infos, warnings, ["At least, 2 bands are tagged with Description = z_translation"]
            z_idx = i+1
        elif desc:
            infos.append('Band of type %s not recognized by PROJ' % desc)

    if x_idx > 0 and y_idx > 0 and z_idx > 0:
        if x_idx != 1 or y_idx != 2 or z_idx != 3:
            infos.append(
                'Usually the first, second and third band should be respectively x_translation, y_translation, z_translation')
    elif x_idx > 0 or y_idx > 0 or z_idx > 0:
        return infos, warnings, ["Part of the bands are tagged with Description = x_translation/y_translation/z_translation but not all"]
    else:
        if is_first_subds:
            warnings.append('No explicit bands tagged with Description = x_translation/y_translation/z_translation. Assuming the first, second and third band are respectively x_translation, y_translation, z_translation')
        x_idx = 1
        y_idx = 2
        z_idx = 3

    for idx in (x_idx, y_idx, z_idx):
        if idx == 0:
            continue
        units = ds.GetRasterBand(idx).GetUnitType()
        if not units:
            if is_first_subds:
                warnings.append(
                    "One of x_translation/y_translation/z_translation band is missing units description. Metre will be assumed")
        elif units not in ('metre',):
            errors.append(
                "One of x_translation/y_translation/z_translation band is using a unit not supported by PROJ")

    return infos, warnings, errors


def validate_velocity(ds, is_first_subds):

    infos = []
    warnings = []
    errors = []

    if ds.RasterCount < 3:
        return infos, warnings, ["TYPE=VELOCITY should have at least 3 bands"]

    x_idx = 0
    y_idx = 0
    z_idx = 0
    for i in range(ds.RasterCount):
        b = ds.GetRasterBand(i+1)
        desc = b.GetDescription()
        if desc == 'east_velocity':
            if x_idx > 0:
                return infos, warnings, ["At least, 2 bands are tagged with Description = east_velocity"]
            x_idx = i+1
        elif desc == 'north_velocity':
            if y_idx > 0:
                return infos, warnings, ["At least, 2 bands are tagged with Description = north_velocity"]
            y_idx = i+1
        elif desc == 'up_velocity':
            if z_idx > 0:
                return infos, warnings, ["At least, 2 bands are tagged with Description = up_velocity"]
            z_idx = i+1
        elif desc and desc not in ('east_velocity_accuracy', 'north_velocity_accuracy', 'up_velocity_accuracy'):
            infos.append('Band of type %s not recognized by PROJ' % desc)

    if x_idx > 0 and y_idx > 0 and z_idx > 0:
        if x_idx != 1 or y_idx != 2 or z_idx != 3:
            infos.append(
                'Usually the first, second and third band should be respectively east_velocity, north_velocity, up_velocity')
    elif x_idx > 0 or y_idx > 0 or z_idx > 0:
        return infos, warnings, ["Part of the bands are tagged with Description = east_velocity/north_velocity/up_velocity but not all"]
    else:
        if is_first_subds:
            warnings.append('No explicit bands tagged with Description = east_velocity/north_velocity/up_velocity. Assuming the first, second and third band are respectively east_velocity, north_velocity, up_velocity')
        x_idx = 1
        y_idx = 2
        z_idx = 3

    for idx in (x_idx, y_idx, z_idx):
        if idx == 0:
            continue
        units = ds.GetRasterBand(idx).GetUnitType()
        if not units:
            if is_first_subds:
                warnings.append(
                    "One of east_velocity/north_velocity/up_velocity band is missing units description. Metre will be assumed")
        elif units not in ('millimetres per year',):
            errors.append(
                "One of east_velocity/north_velocity/up_velocity band is using a unit not supported by PROJ")

    return infos, warnings, errors


def validate_defmodel(ds, is_first_subds, first_subds):

    infos = []
    warnings = []
    errors = []

    displacement_type = ds.GetMetadataItem('DISPLACEMENT_TYPE')
    if not displacement_type:
        if is_first_subds:
            warnings.append("Missing DISPLACEMENT_TYPE metadata item")
        else:
            displacement_type = first_subds.GetMetadataItem('TYPE')
    elif displacement_type not in ('NONE',
                                   'HORIZONTAL',
                                   'VERTICAL',
                                   '3D'):
        warnings.append("DISPLACEMENT_TYPE=%s is not recognize by PROJ" % displacement_type)

    uncertainty_type = ds.GetMetadataItem('UNCERTAINTY_TYPE')
    if not displacement_type:
        if is_first_subds:
            warnings.append("Missing UNCERTAINTY_TYPE metadata item")
        else:
            uncertainty_type = first_subds.GetMetadataItem('TYPE')
    elif uncertainty_type not in ('NONE',
                                  'HORIZONTAL',
                                  'VERTICAL',
                                  '3D'):
        warnings.append("UNCERTAINTY_TYPE=%s is not recognize by PROJ" % uncertainty_type)

    if displacement_type == 'HORIZONTAL':
        min_expected_band_count = 2
    elif displacement_type == 'VERTICAL':
        min_expected_band_count = 1
    elif displacement_type == '3D':
        min_expected_band_count = 3
    else:
        return infos, warnings, errors

    if ds.RasterCount < min_expected_band_count:
        return infos, warnings, ["DISPLACEMENT_TYPE=%s should have at least %d bands" % (displacement_type, min_expected_band_count)]

    x_idx = 0
    y_idx = 0
    z_idx = 0
    for i in range(ds.RasterCount):
        b = ds.GetRasterBand(i+1)
        desc = b.GetDescription()
        if desc == 'east_offset':
            if x_idx > 0:
                return infos, warnings, ["At least, 2 bands are tagged with Description = east_offset"]
            x_idx = i+1
        elif desc == 'north_offset':
            if y_idx > 0:
                return infos, warnings, ["At least, 2 bands are tagged with Description = north_offset"]
            y_idx = i+1
        elif desc == 'vertical_offset':
            if z_idx > 0:
                return infos, warnings, ["At least, 2 bands are tagged with Description = vertical_offset"]
            z_idx = i+1
        elif desc and desc not in ('east_offset', 'north_offset', 'vertical_offset'):
            infos.append('Band of type %s not recognized by PROJ' % desc)

    if displacement_type == 'HORIZONTAL':
        if z_idx > 0:
            warnings.append('Band with Description = vertical_offset unexpectedly found for DISPLACEMENT_TYPE=HORIZONTAL')
        if x_idx > 0 and y_idx > 0:
            if x_idx != 1 or y_idx != 2:
                infos.append(
                    'Usually the first and second band should be respectively east_offset, north_offset for DISPLACEMENT_TYPE=HORIZONTAL')
        elif x_idx > 0 or y_idx > 0:
            errors.append("Part of the bands are tagged with Description = east_offset/north_offset but not all")
        else:
            if is_first_subds:
                warnings.append('No explicit bands tagged with Description = east_offset/north_offset. Assuming the first and second are respectively east_offset, north_offset')
            x_idx = 1
            y_idx = 2

    elif displacement_type == 'VERTICAL':
        if x_idx > 0:
            warnings.append('Band with Description = east_offset unexpectedly found for DISPLACEMENT_TYPE=VERTICAL')
        if y_idx > 0:
            warnings.append('Band with Description = north_offset unexpectedly found for DISPLACEMENT_TYPE=VERTICAL')
        if z_idx > 0:
            if z_idx != 1:
                infos.append(
                    'Usually the first band should be vertical_offset for DISPLACEMENT_TYPE=VERTICAL')
        else:
            if is_first_subds:
                warnings.append('No explicit bands tagged with Description = vertical_offset. Assuming this is the first band')
            z_idx = 1

    elif displacement_type == '3D':
        if x_idx > 0 and y_idx > 0 and z_idx > 0:
            if x_idx != 1 or y_idx != 2 or z_idx != 3:
                infos.append(
                    'Usually the first, second and third band should be respectively east_offset, north_offset, vertical_offset for DISPLACEMENT_TYPE=3D')
        elif x_idx > 0 or y_idx > 0 or z_idx > 0:
            return infos, warnings, ["Part of the bands are tagged with Description = east_offset/north_offset/vertical_offset but not all"]
        else:
            if is_first_subds:
                warnings.append('No explicit bands tagged with Description = east_offset/north_offset/vertical_offset. Assuming the first, second and third band are respectively east_velocity, north_velocity, north_offset')
            x_idx = 1
            y_idx = 2
            z_idx = 3

    for idx in (x_idx, y_idx, z_idx):
        if idx == 0:
            continue
        units = ds.GetRasterBand(idx).GetUnitType()
        if not units:
            if is_first_subds:
                warnings.append(
                    "One of east_offset/north_offset/vertical_offset band is missing units description.")
        elif units not in ('degree', 'metre'):
            errors.append(
                "One of east_offset/north_offset/vertical_offset band is using a unit not supported by PROJ")

    return infos, warnings, errors


class GlobalInfo(object):
    def __init__(self):
        self.map_grid_name_to_grid = {}
        self.map_grid_name_to_children = {}


def get_extent(ds):
    gt = ds.GetGeoTransform()
    xmin = gt[0] + gt[1] / 2
    ytop = gt[3] + gt[5] / 2
    xmax = gt[0] + gt[1] * ds.RasterXSize - gt[1] / 2
    ybottom = gt[3] + gt[5] * ds.RasterYSize - gt[5] / 2
    return xmin, min(ytop, ybottom), xmax, max(ytop, ybottom)


def validate_ifd(global_info, ds, is_first_subds, first_subds):

    infos = []
    warnings = []
    errors = []

    wkt = ds.GetProjectionRef()
    srs = None
    if wkt and not wkt.startswith('LOCAL_CS['):
        srs = osr.SpatialReference()
        if srs.ImportFromWkt(wkt) != 0:
            srs = None

    if not srs:
        if is_first_subds:
            errors.append("No CRS found in the GeoTIFF encoding")
    else:
        if not srs.IsGeographic() and ds.GetMetadataItem('TYPE') != 'DEFORMATION_MODEL':
            errors.append("CRS found, but not a Geographic CRS")

    if ds.GetMetadataItem('AREA_OR_POINT') != 'Point':
        warnings.append("This file uses a RasterTypeGeoKey = PixelIsArea convention. While this will work properly with PROJ, a georeferencing using RasterTypeGeoKey = PixelIsPoint is more common.")

    gt = ds.GetGeoTransform(can_return_null=True)
    if not gt:
        errors.append("No geotransform matrix found")
    else:
        if gt[2] != 0 or gt[4] != 0:
            errors.append("Geotransform with rotation terms not supported")
        if gt[1] < 0:
            errors.append(
                "Geotransform with a negative pixel width not supported")
        if gt[1] == 0:
            errors.append("Geotransform with a zero pixel width")
        if gt[5] > 0:
            warnings.append(
                "Geotransform with a positive pixel height, that is a south-up image, is supported, but a unusual formulation")
        if gt[5] == 0:
            errors.append("Geotransform with a zero pixel height")

    type = ds.GetMetadataItem('TYPE')
    if not type:
        if is_first_subds:
            warnings.append("Missing TYPE metadata item")
        else:
            type = first_subds.GetMetadataItem('TYPE')
    elif type not in ('HORIZONTAL_OFFSET',
                      'VERTICAL_OFFSET_GEOGRAPHIC_TO_VERTICAL',
                      'VERTICAL_OFFSET_VERTICAL_TO_VERTICAL',
                      'GEOCENTRIC_TRANSLATION',
                      'VELOCITY',
                      'DEFORMATION_MODEL',):
        warnings.append("TYPE=%s is not recognize by PROJ" % type)

    if is_first_subds:
        if not ds.GetMetadataItem('area_of_use'):
            warnings.append(
                "GDAL area_of_use metadata item is missing. Typically used to capture plain text information about where the grid applies")

        if not ds.GetMetadataItem('TIFFTAG_IMAGEDESCRIPTION'):
            warnings.append(
                "TIFF tag ImageDescription is missing. Typically used to capture plain text information about what the grid does")

        if not ds.GetMetadataItem('TIFFTAG_COPYRIGHT'):
            warnings.append(
                "TIFF tag Copyright is missing. Typically used to capture information on the source and licensing terms")

        dt = ds.GetMetadataItem('TIFFTAG_DATETIME')
        if not dt:
            warnings.append(
                "TIFF tag DateTime is missing. Typically used to capture when the grid has been generated/converted")
        else:
            m = re.match(
                r'^(\d\d\d\d):(\d\d):(\d\d) (\d\d):(\d\d):(\d\d)$', dt)
            wrong_dt_format = False
            if not m:
                wrong_dt_format = True
            else:
                year, month, day, hour, min, sec = (int(v) for v in m.groups())
                if not (year >= 1980 and year <= datetime.datetime.now().year):
                    wrong_dt_format = True
                else:
                    try:
                        datetime.datetime(year, month, day, hour, min, sec)
                    except:
                        wrong_dt_format = True

            if wrong_dt_format:
                warnings.append(
                    "TIFF tag DateTime malformed. Should be YYYY:MM:DD HH:MM:SS")

    compression = ds.GetMetadataItem('COMPRESSION', 'IMAGE_STRUCTURE')
    if not compression:
        warnings.append(
            'Image is uncompressed. Could potentially benefit from compression')
    elif compression not in ('LZW', 'DEFLATE'):
        warnings.append(
            'Image uses %s compression. Might cause compatibility problems' % compression)

    if type == 'HORIZONTAL_OFFSET':
        i, w, e = validate_horizontal_offset(ds, is_first_subds)
        infos += i
        warnings += w
        errors += e
    elif type == 'VERTICAL_OFFSET_GEOGRAPHIC_TO_VERTICAL':
        i, w, e = validate_vertical_offset_geographic_to_vertical(
            ds, is_first_subds)
        infos += i
        warnings += w
        errors += e
    elif type == 'VERTICAL_OFFSET_VERTICAL_TO_VERTICAL':
        i, w, e = validate_vertical_offset_vertical_to_vertical(
            ds, is_first_subds)
        infos += i
        warnings += w
        errors += e
    elif type == 'GEOCENTRIC_TRANSLATION':
        i, w, e = validate_geocentric_translation(ds, is_first_subds)
        infos += i
        warnings += w
        errors += e
    elif type == 'VELOCITY':
        i, w, e = validate_velocity(ds, is_first_subds)
        infos += i
        warnings += w
        errors += e
    elif type == 'DEFORMATION_MODEL':
        i, w, e = validate_defmodel(ds, is_first_subds, first_subds)
        infos += i
        warnings += w
        errors += e

    grid_name = ds.GetMetadataItem('grid_name')
    if grid_name:
        if grid_name in global_info.map_grid_name_to_grid:
            errors.append(
                'Several subgrids with grid_name=%s found' % grid_name)
        global_info.map_grid_name_to_grid[grid_name] = ds

    parent_grid_name = ds.GetMetadataItem('parent_grid_name')
    if parent_grid_name:
        if not grid_name:
            errors.append('Grid has parent_grid_name, but not grid_name')

        if parent_grid_name not in global_info.map_grid_name_to_children:
            global_info.map_grid_name_to_children[parent_grid_name] = [ds]
        else:
            global_info.map_grid_name_to_children[parent_grid_name].append(ds)

        if parent_grid_name not in global_info.map_grid_name_to_grid:
            errors.append(
                'Parent grid named %s not already encountered' % parent_grid_name)
        else:
            parent_ds = global_info.map_grid_name_to_grid[parent_grid_name]
            parent_xmin, parent_ymin, parent_xmax, parent_ymax = get_extent(
                parent_ds)
            xmin, ymin, xmax, ymax = get_extent(ds)
            if not (xmin+1e-10 >= parent_xmin and ymin+1e-10 >= parent_ymin and xmax-1e-10 <= parent_xmax and ymax-1e-10 <= parent_ymax):
                errors.append('Extent (%f,%f,%f,%f) of grid %s is not inside its parent %s extent (%f,%f,%f,%f)' % (
                    xmin, ymin, xmax, ymax, grid_name if grid_name else 'unknown', parent_grid_name, parent_xmin, parent_ymin, parent_xmax, parent_ymax))

    # Check for well kown metadata item names
    md = ds.GetMetadata_Dict()
    md_keys = md.keys()
    for key in md_keys:
        if key not in ('AREA_OR_POINT', 'TYPE',
                       'area_of_use',
                       'grid_name',
                       'parent_grid_name',
                       'source_crs_epsg_code', 'source_crs_wkt',
                       'target_crs_epsg_code', 'target_crs_wkt',
                       'interpolation_crs_wkt',
                       'recommended_interpolation_method',
                       'TIFFTAG_COPYRIGHT',
                       'TIFFTAG_DATETIME',
                       'TIFFTAG_IMAGEDESCRIPTION',
                       'number_of_nested_grids',
                       'UNCERTAINTY_TYPE',
                       'DISPLACEMENT_TYPE',
                       'UNCERTAINTY_TYPE',):
            infos.append('Metadata %s=%s ignored' % (key, md[key]))

    for i in range(ds.RasterCount):
        b = ds.GetRasterBand(i+1)
        md = b.GetMetadata_Dict()
        md_keys = md.keys()
        for key in md_keys:
            if key not in ('positive_value'):
                infos.append('Metadata %s=%s on band %d ignored' %
                             (key, md[key], i+1))

        if b.DataType not in (gdal.GDT_Int16, gdal.GDT_UInt16,
                              gdal.GDT_Int32, gdal.GDT_UInt32,
                              gdal.GDT_Float32, gdal.GDT_Float64):
            errors.append('Datatype %s of band %d is not support' %
                          (gdal.GetDataTypeName(b.DataType), i+1))

        if b.GetMetadataItem('NBITS'):
            errors.append('NBITS != native bit depth not supported')

        gdal.ErrorReset()
        b.Checksum()
        if gdal.GetLastErrorMsg() != '':
            errors.append('Cannot read values of band %d' % (i+1))

    block_width, block_height = ds.GetRasterBand(1).GetBlockSize()
    if ds.RasterYSize > 512:
        if block_width > 512 or block_height > 512:
            warnings.append(
                'Given image dimension, tiling could be appropriate')

    return infos, warnings, errors


def validate(filename):

    infos = []
    warnings = []
    errors = []
    ds = gdal.Open(filename)
    global_info = GlobalInfo()

    if not ds:
        return infos, warnings, ["Cannot open file"]

    if ds.GetDriver().ShortName != 'GTiff':
        return infos, warnings, ["Not a TIFF file"]

    subds_list = ds.GetSubDatasets()
    if not subds_list:
        subds_list = [(filename, None)]
    first_subds = None

    ifd_offset = int(ds.GetRasterBand(1).GetMetadataItem('IFD_OFFSET', 'TIFF'))
    if ifd_offset > 100:
        warnings.append(
            'Offset of first IFD is %d > 100. Not cloud friedly layout' % ifd_offset)
    last_ifd_offset = ifd_offset

    block_offsets = []

    # Iterate through IFDs
    for idx, subds_tuple in enumerate(subds_list):

        subds_name = subds_tuple[0]

        sub_ds = gdal.Open(subds_name)
        if not ds:
            return infos, warnings, ["Cannot open subdataset of IFD %d" % idx]

        sub_ds_infos, sub_ds_warnings, sub_ds_errors = validate_ifd(
            global_info, sub_ds, idx == 0, first_subds)

        ifd_offset = int(sub_ds.GetRasterBand(
            1).GetMetadataItem('IFD_OFFSET', 'TIFF'))
        if idx > 0 and ifd_offset < last_ifd_offset:
            warnings.append('Offset of IFD %d is %d, before offset of previous IFD' % (
                ifd_offset, last_ifd_offset))
        last_ifd_offset = ifd_offset
        block_offsets.append(int(sub_ds.GetRasterBand(
            1).GetMetadataItem('BLOCK_OFFSET_0_0', 'TIFF')))

        if len(subds_list) == 1:
            return sub_ds_infos, sub_ds_warnings, sub_ds_errors

        if sub_ds_infos:
            for i in sub_ds_infos:
                infos.append('IFD %d: %s' % (idx, i))

        if sub_ds_warnings:
            for w in sub_ds_warnings:
                warnings.append('IFD %d: %s' % (idx, w))

        if sub_ds_errors:
            for e in sub_ds_errors:
                errors.append('IFD %d: %s' % (idx, e))

        if first_subds is None:
            first_subds = gdal.Open(subds_name)

    for idx, offset in enumerate(block_offsets):
        if offset < last_ifd_offset:
            warnings.append(
                'Data for IFD %d is not located after the last IFD' % idx)

    # Check value of number_of_nested_grids metadata item
    for grid_name, children in global_info.map_grid_name_to_children.items():
        ds = global_info.map_grid_name_to_grid[grid_name]
        number_of_nested_grids = ds.GetMetadataItem('number_of_nested_grids')
        if not number_of_nested_grids:
            warnings.append('Grid %s missing number_of_nested_grids=%d' % (
                grid_name, len(children)))
        elif number_of_nested_grids != str(len(children)):
            warnings.append('Grid %s contains number_of_nested_grids=%s, but should be %d' % (
                grid_name, number_of_nested_grids, len(children)))

    return infos, warnings, errors


if __name__ == '__main__':

    args = get_args()

    infos, warnings, errors = validate(args.filename)

    if errors:
        print('%s is NOT a valid PROJ GeoTIFF file.' % args.filename)
        print('The following errors were found (corrective action is required):')
        for error in errors:
            print(' - ' + error)
        print('')

    if warnings:
        print('The following warnings were found (the file will probably be read correctly by PROJ, but corrective action may be required):')
        for warning in warnings:
            print(' - ' + warning)
        print('')

    if infos:
        print(
            'The following informative message are issued (no corrective action required):')
        for info in infos:
            print(' - ' + info)
        print('')

    sys.exit(1 if errors else 0)
