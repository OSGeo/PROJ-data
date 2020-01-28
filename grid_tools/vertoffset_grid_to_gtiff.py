#!/usr/bin/env python
###############################################################################
# $Id$
#
#  Project:  PROJ
#  Purpose:  Convert a GTX or similar file into an optimized GTiff
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

# python vertoffset_grid_to_gtiff.py $HOME/proj/proj-datumgrid/egm96_15.gtx egm96_15.tif --type GEOGRAPHIC_TO_VERTICAL --source-crs EPSG:4326 --target-crs EPSG:5773 --copyright "Public Domain. Derived from work at http://earth-info.nga.mil/GandG/wgs84/gravitymod/egm96/egm96.html"
# python vertoffset_grid_to_gtiff.py $HOME/proj/proj-datumgrid/world/egm08_25.gtx egm08_25.tif --type GEOGRAPHIC_TO_VERTICAL --source-crs EPSG:4326 --target-crs EPSG:3855  --copyright "Public Domain. Derived from work at http://earth-info.nga.mil/GandG/wgs84/gravitymod/egm2008/egm08_wgs84.html"
# python vertoffset_grid_to_gtiff.py $HOME/proj/proj-datumgrid/north-america/vertcone.gtx vertcone.tif --type VERTICAL_TO_VERTICAL --source-crs EPSG:7968 --target-crs EPSG:5703 --interpolation-crs EPSG:4267 --copyright "Public Domain. Derived from work at https://www.ngs.noaa.gov/PC_PROD/VERTCON/"

from osgeo import gdal
from osgeo import osr
from cloud_optimize_gtiff import generate_optimized_file
import argparse
import datetime
import os
import struct


def get_args():
    parser = argparse.ArgumentParser(
        description='Convert a vertical offset grid into PROJ GeoTIFF.')
    parser.add_argument('source',
                        help='Source file')
    parser.add_argument('dest',
                        help='Destination GeoTIFF file')

    parser.add_argument('--type', dest='type', required=True,
                        choices=['GEOGRAPHIC_TO_VERTICAL',
                                 'VERTICAL_TO_VERTICAL'],
                        help='Type of grid')

    parser.add_argument('--source-crs', dest='source_crs', required=True,
                        help='Source CRS as EPSG:XXXX or WKT')

    parser.add_argument('--interpolation-crs', dest='interpolation_crs',
                        help='Interpolation CRS as EPSG:XXXX or WKT. Required for type=VERTICAL_TO_VERTICAL')

    parser.add_argument('--target-crs', dest='target_crs', required=True,
                        help='Target CRS as EPSG:XXXX or WKT')

    parser.add_argument('--copyright', dest='copyright', required=True,
                        help='Copyright info')

    parser.add_argument('--description', dest='description',
                        help='Description')

    parser.add_argument('--encoding',
                        dest='encoding',
                        choices=['float32', 'uint16', 'int32-scale-1-1000'],
                        default='float32',
                        help='Binary encoding. int32-scale-1-1000 is for for Canadian .byn')

    parser.add_argument('--ignore-nodata', dest='ignore_nodata',
                        action='store_true',
                        help='Whether to ignore nodata')

    parser.add_argument('--datetime', dest='datetime',
                        help='Value for TIFF DateTime tag as YYYY:MM:DD HH:MM:SS, or "NONE" to not write it. If not specified, current date time is used')

    parser.add_argument('--area-of-use', dest='area_of_use',
                        help='Area of use')

    return parser.parse_args()


def create_unoptimized_file(sourcefilename, tmpfilename, args):
    src_ds = gdal.Open(sourcefilename)
    subdatsets = src_ds.GetSubDatasets()
    if not subdatsets:
        subdatsets = [(sourcefilename, None)]

    src_basename = os.path.basename(args.source)
    nbands = 1

    compact_md = True if len(subdatsets) > 50 else False

    is_vertcon = src_basename in (
        'vertcone.gtx', 'vertconw.gtx', 'vertconc.gtx')

    for idx_ifd, subds in enumerate(subdatsets):
        src_ds = gdal.Open(subds[0])

        if args.encoding == 'int32-scale-1-1000':
            target_dt = gdal.GDT_Int32
        elif args.encoding == 'uint16':
            target_dt = gdal.GDT_UInt16
        else:
            target_dt = gdal.GDT_Float32
        tmp_ds = gdal.GetDriverByName('GTiff').Create('/vsimem/tmp',
                                                      src_ds.RasterXSize,
                                                      src_ds.RasterYSize,
                                                      nbands,
                                                      target_dt)
        interpolation_crs = osr.SpatialReference()
        if args.type == 'GEOGRAPHIC_TO_VERTICAL':
            interpolation_crs.SetFromUserInput(args.source_crs)
        else:
            interpolation_crs.SetFromUserInput(args.interpolation_crs)
        assert interpolation_crs.IsGeographic()
        tmp_ds.SetSpatialRef(interpolation_crs)
        tmp_ds.SetGeoTransform(src_ds.GetGeoTransform())
        tmp_ds.SetMetadataItem('AREA_OR_POINT', 'Point')

        if args.type == 'GEOGRAPHIC_TO_VERTICAL':
            tmp_ds.SetMetadataItem(
                'TYPE', 'VERTICAL_OFFSET_GEOGRAPHIC_TO_VERTICAL')
        else:
            tmp_ds.SetMetadataItem(
                'TYPE', 'VERTICAL_OFFSET_VERTICAL_TO_VERTICAL')

        src_crs = osr.SpatialReference()
        src_crs.SetFromUserInput(args.source_crs)
        if args.type == 'VERTICAL_TO_VERTICAL':
            assert src_crs.IsVertical()
            src_auth_name = src_crs.GetAuthorityName(None)
            src_auth_code = src_crs.GetAuthorityCode(None)
            if idx_ifd == 0 or not compact_md:
                if src_auth_name == 'EPSG' and src_auth_code:
                    tmp_ds.SetMetadataItem(
                        'source_crs_epsg_code', src_auth_code)
                else:
                    tmp_ds.SetMetadataItem(
                        'source_crs_wkt', src_crs.ExportToWkt(['FORMAT=WKT2_2018']))

        dst_crs = osr.SpatialReference()
        dst_crs.SetFromUserInput(args.target_crs)
        assert dst_crs.IsVertical()
        dst_auth_name = dst_crs.GetAuthorityName(None)
        dst_auth_code = dst_crs.GetAuthorityCode(None)
        if idx_ifd == 0 or not compact_md:
            if dst_auth_name == 'EPSG' and dst_auth_code:
                tmp_ds.SetMetadataItem('target_crs_epsg_code', dst_auth_code)
            else:
                tmp_ds.SetMetadataItem(
                    'target_crs_wkt', dst_crs.ExportToWkt(['FORMAT=WKT2_2018']))

        def is_false_positive_nodata(y, x):
            return src_basename == 'egm08_25.gtx' and y == 2277 and x == 6283

        if args.encoding == 'int32-scale-1-1000':
            assert src_ds.RasterCount == 1
            scale = 0.001
            nodata = None if args.ignore_nodata else src_ds.GetRasterBand(
                1).GetNoDataValue()
            data = src_ds.GetRasterBand(1).ReadAsArray()
            if nodata is None:
                data = data / scale
            else:
                dst_nodata = 9999000
                nodata_as_f = struct.pack('f', nodata)
                has_warned_nodata = False
                for y in range(src_ds.RasterYSize):
                    for x in range(src_ds.RasterXSize):
                        is_nodata = False
                        if struct.pack('f', data[y][x]) == nodata_as_f:
                            if is_false_positive_nodata(y, x):
                                pass
                            elif not has_warned_nodata:
                                print(
                                    'At least one value matches nodata (at %d,%d). Setting it' % (y, x))
                                tmp_ds.GetRasterBand(
                                    1).SetNoDataValue(dst_nodata)
                                has_warned_nodata = True
                                is_nodata = True
                            else:
                                is_nodata = True

                        if is_nodata:
                            data[y][x] = dst_nodata
                        else:
                            data[y][x] = data[y][x] / scale

            tmp_ds.GetRasterBand(1).WriteArray(data)
            tmp_ds.GetRasterBand(1).SetOffset(0)
            tmp_ds.GetRasterBand(1).SetScale(scale)
            if idx_ifd == 0 or not compact_md:
                tmp_ds.GetRasterBand(1).SetDescription(
                    'geoid_undulation' if args.type == 'GEOGRAPHIC_TO_VERTICAL' else 'vertical_offset')
                tmp_ds.GetRasterBand(1).SetUnitType('metre')

        elif args.encoding == 'uint16':
            for i in (1, ):
                min, max = src_ds.GetRasterBand(i).ComputeRasterMinMax()
                data = src_ds.GetRasterBand(i).ReadAsArray()
                if is_vertcon:  # in millimetres originally !
                    assert min < -100 or max > 100
                    min = min * 0.001
                    max = max * 0.001

                dst_nodata = 65535
                scale = (max - min) / 65534  # we use 65535 for nodata

                nodata = None if args.ignore_nodata else src_ds.GetRasterBand(
                    i).GetNoDataValue()
                if nodata is None:
                    if is_vertcon:  # in millimetres originally !
                        data = data * 0.001
                    data = (data - min) / scale
                else:
                    nodata_as_f = struct.pack('f', nodata)
                    has_warned_nodata = False
                    for y in range(src_ds.RasterYSize):
                        for x in range(src_ds.RasterXSize):
                            is_nodata = False
                            if struct.pack('f', data[y][x]) == nodata_as_f:
                                if is_false_positive_nodata(y, x):
                                    pass
                                elif not has_warned_nodata:
                                    print(
                                        'At least one value matches nodata (at %d,%d). Setting it' % (y, x))
                                    tmp_ds.GetRasterBand(
                                        i).SetNoDataValue(dst_nodata)
                                    has_warned_nodata = True
                                    is_nodata = True
                                else:
                                    is_nodata = True

                            if is_nodata:
                                data[y][x] = dst_nodata
                            else:
                                if is_vertcon:  # in millimetres originally !
                                    data[y][x] = (
                                        data[y][x] * 0.001 - min) / scale
                                else:
                                    data[y][x] = (data[y][x] - min) / scale

                tmp_ds.GetRasterBand(i).WriteArray(data)
                tmp_ds.GetRasterBand(i).SetOffset(min)
                tmp_ds.GetRasterBand(i).SetScale(scale)
                if idx_ifd == 0 or not compact_md:
                    tmp_ds.GetRasterBand(i).SetDescription(
                        'geoid_undulation' if args.type == 'GEOGRAPHIC_TO_VERTICAL' else 'vertical_offset')
                    tmp_ds.GetRasterBand(i).SetUnitType('metre')

        else:
            for i in (1,):
                data = src_ds.GetRasterBand(i).ReadRaster()

                nodata = None if args.ignore_nodata else src_ds.GetRasterBand(
                    i).GetNoDataValue()
                nvalues = src_ds.RasterXSize * src_ds.RasterYSize
                dst_nodata = -32768
                if nodata:
                    packed_src_nodata = struct.pack('f', nodata)
                    packed_dst_nodata = struct.pack('f', dst_nodata)
                    assert src_ds.GetRasterBand(1).DataType == gdal.GDT_Float32
                    has_warned_nodata = False
                    out_data = bytearray(data)
                    for idx in range(len(data)//4):
                        is_nodata = False
                        if data[idx*4:idx*4+4] == packed_src_nodata:
                            y = idx // src_ds.RasterXSize
                            x = idx % src_ds.RasterXSize
                            if is_false_positive_nodata(y, x):
                                pass
                            elif not has_warned_nodata:
                                print(
                                    'At least one value matches nodata (at idx %d,%d). Setting it' % (y, x))
                                tmp_ds.GetRasterBand(
                                    i).SetNoDataValue(dst_nodata)
                                has_warned_nodata = True
                                is_nodata = True
                            else:
                                is_nodata = True

                        if is_nodata:
                            out_data[idx*4:idx*4+4] = packed_dst_nodata

                    data = bytes(out_data)

                if is_vertcon:  # in millimetres originally !
                    min, max = src_ds.GetRasterBand(i).ComputeRasterMinMax()
                    assert min < -100 or max > 100
                    assert src_ds.GetRasterBand(1).DataType == gdal.GDT_Float32
                    out_data = b''
                    for v in struct.unpack('f' * nvalues, data):
                        out_data += struct.pack('f', v * 0.001 if v !=
                                                dst_nodata else dst_nodata)
                    data = out_data

                tmp_ds.GetRasterBand(i).WriteRaster(0, 0, src_ds.RasterXSize, src_ds.RasterYSize,
                                                    data)
                if idx_ifd == 0 or not compact_md:
                    tmp_ds.GetRasterBand(i).SetDescription(
                        'geoid_undulation' if args.type == 'GEOGRAPHIC_TO_VERTICAL' else 'vertical_offset')
                    tmp_ds.GetRasterBand(i).SetUnitType('metre')

        if idx_ifd == 0:
            desc = args.description
            if not desc:
                src_auth_name = src_crs.GetAuthorityName(None)
                src_auth_code = src_crs.GetAuthorityCode(None)

                desc = src_crs.GetName()
                if src_auth_name and src_auth_code:
                    desc += ' (' + src_auth_name + ':' + src_auth_code + ')'
                desc += ' to '
                desc += dst_crs.GetName()
                if dst_auth_name and dst_auth_code:
                    desc += ' (' + dst_auth_name + ':' + dst_auth_code + ')'
                desc += '. Converted from '
                desc += src_basename
                desc += ' (last modified at '
                desc += datetime.datetime.utcfromtimestamp(
                    os.stat(sourcefilename).st_mtime).strftime("%Y/%m/%d")
                desc += ')'

            tmp_ds.SetMetadataItem('TIFFTAG_IMAGEDESCRIPTION', desc)
            if args.copyright:
                tmp_ds.SetMetadataItem('TIFFTAG_COPYRIGHT', args.copyright)
            if args.datetime and args.datetime != 'NONE':
                tmp_ds.SetMetadataItem('TIFFTAG_DATETIME', args.datetime)
            if args.area_of_use:
                tmp_ds.SetMetadataItem('area_of_use', args.area_of_use)

        options = ['PHOTOMETRIC=MINISBLACK',
                   'COMPRESS=DEFLATE',
                   'PREDICTOR=3' if target_dt == gdal.GDT_Float32 else 'PREDICTOR=2',
                   'INTERLEAVE=BAND',
                   'GEOTIFF_VERSION=1.1']
        if tmp_ds.RasterXSize > 256 and tmp_ds.RasterYSize > 256:
            options.append('TILED=YES')
        else:
            options.append('BLOCKYSIZE=' + str(tmp_ds.RasterYSize))
        if gdal.VSIStatL(tmpfilename) is not None:
            options.append('APPEND_SUBDATASET=YES')

        assert gdal.GetDriverByName('GTiff').CreateCopy(tmpfilename, tmp_ds,
                                                        options=options)


def check(sourcefilename, destfilename, args):
    src_ds = gdal.Open(sourcefilename)
    src_subdatsets = src_ds.GetSubDatasets()
    if not src_subdatsets:
        src_subdatsets = [(sourcefilename, None)]

    dst_ds = gdal.Open(destfilename)
    dst_subdatsets = dst_ds.GetSubDatasets()
    if not dst_subdatsets:
        dst_subdatsets = [(destfilename, None)]

    assert len(src_subdatsets) == len(dst_subdatsets)
    for dst_subds in dst_subdatsets:
        dst_ds = gdal.Open(dst_subds[0])
        dst_ds.GetRasterBand(1).Checksum()
        assert gdal.GetLastErrorMsg() == ''


if __name__ == '__main__':

    args = get_args()

    tmpfilename = args.dest + '.tmp'
    gdal.Unlink(tmpfilename)

    if not args.datetime and args.datetime != 'NONE':
        args.datetime = datetime.date.today().strftime("%Y:%m:%d %H:%M:%S")

    create_unoptimized_file(args.source, tmpfilename, args)
    generate_optimized_file(tmpfilename, args.dest)
    check(args.source, args.dest, args)

    gdal.Unlink(tmpfilename)
