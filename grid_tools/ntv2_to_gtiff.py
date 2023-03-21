#!/usr/bin/env python
###############################################################################
# $Id$
#
#  Project:  PROJ
#  Purpose:  Convert a NTv2 file into an optimized GTiff
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

# python ./ntv2_to_gtiff.py --copyright "Derived from work by IGN France. Open License https://www.etalab.gouv.fr/wp-content/uploads/2014/05/Open_Licence.pdf" --source-crs EPSG:4275 --target-crs EPSG:4171 /home/even/proj/proj-datumgrid/ntf_r93.gsb ntf_r93.tif
# python ./ntv2_to_gtiff.py --copyright "Derived from work by LGL-BW.DE. Data licence Germany - attribution - version 2.0: https://www.govdata.de/dl-de/by-2-0"  --source-crs EPSG:4314 --target-crs EPSG:4258 /home/even/proj/proj-datumgrid/europe/BWTA2017.gsb BWTA2017.tif --do-not-write-accuracy-samples
# python ./ntv2_to_gtiff.py --copyright "Derived from work by Natural Resources Canada. Open Government Licence - Canada: http://open.canada.ca/en/open-government-licence-canada" --source-crs EPSG:4267 --target-crs EPSG:4269 /home/even/proj/proj-datumgrid/north-america/ntv2_0.gsb ntv2_0.tif
# python ./ntv2_to_gtiff.py --copyright "Derived from work by ICSM. Creative Commons Attribution 4.0: https://creativecommons.org/licenses/by/4.0/" --source-crs EPSG:4283  --target-crs EPSG:7844 /home/even/proj/proj-datumgrid/oceania/GDA94_GDA2020_conformal.gsb GDA94_GDA2020_conformal.tif


from osgeo import gdal
from osgeo import osr
from cloud_optimize_gtiff import generate_optimized_file
import argparse
import datetime
import math
import os
import struct


def get_args():
    parser = argparse.ArgumentParser(
        description='Convert NTv2 grid into PROJ GeoTIFF.')
    parser.add_argument('source',
                        help='Source NTv2 file')
    parser.add_argument('dest',
                        help='Destination GeoTIFF file')

    parser.add_argument('--source-crs', dest='source_crs', required=True,
                        help='Source CRS as EPSG:XXXX or WKT')

    parser.add_argument('--target-crs', dest='target_crs', required=True,
                        help='Target CRS as EPSG:XXXX or WKT')

    parser.add_argument('--copyright', dest='copyright', required=True,
                        help='Copyright info')

    parser.add_argument('--description', dest='description',
                        help='Description')

    parser.add_argument('--do-not-write-accuracy-samples', dest='do_not_write_accuracy_samples',
                        action='store_true')

    parser.add_argument('--positive-longitude-shift-value',
                        dest='positive_longitude_shift_value',
                        choices=['east', 'west'],
                        default='east',
                        help='Whether positive values in the longitude_offset channel should be shift to the east or the west')

    parser.add_argument('--uint16-encoding', dest='uint16_encoding',
                        action='store_true',
                        help='Use uint16 storage with linear scaling/offseting')

    parser.add_argument('--datetime', dest='datetime',
                        help='Value for TIFF DateTime tag as YYYY:MM:DD HH:MM:SS, or "NONE" to not write it. If not specified, current date time is used')

    parser.add_argument('--accuracy-unit', dest='accuracy_unit',
                        choices=['arc-second', 'metre', 'unknown'],
                        help='Unit of accuracy channels')

    parser.add_argument('--area-of-use', dest='area_of_use',
                        help='Area of use')

    return parser.parse_args()


def get_year_month_day(src_date, src_basename):
    if len(src_date) == 4 and src_basename == 'GS7783.GSB':
        # CREATED=1991
        return int(src_date), 1, 1

    if len(src_date) == 7 and src_basename == 'NB2783v2.GSB':
        # CREATED=06/2011
        month = int(src_date[0:2])
        year = int(src_date[3:7])
        return year, month, 1

    assert len(src_date) == 8
    if (src_date[2] == '-' and src_date[5] == '-') or \
            (src_date[2] == '/' and src_date[5] == '/'):
        if src_basename.startswith('rdtrans') or \
           src_basename.startswith('rdcorr') or \
                src_basename.startswith('ntf_r93') or \
                src_basename.startswith('BWTA2017') or \
                src_basename.startswith('BETA2007') or \
                src_basename.startswith('D73_ETRS89_geo') or \
                src_basename.startswith('DLx_ETRS89_geo') or \
                src_basename.startswith('kanu_ntv2_'):
            # rdtrans2018.gsb has 22-11-18 &
            # ntf_r93.gsb has 31/10/07, hence D-M-Y
            day = int(src_date[0:2])
            month = int(src_date[3:5])
            year = int(src_date[6:8])
        else:
            # CHENyx06a.gsb has 09-07-22 & ntv2_0.gsb and
            # (other NRCan datasets) has 95-06-30, hence Y-M-D
            year = int(src_date[0:2])
            month = int(src_date[3:5])
            day = int(src_date[6:8])
        if year >= 90:
            year += 1900
        else:
            assert year <= 50
            year += 2000
    else:
        if src_basename in ('nzgd2kgrid0005.gsb',
                            'A66_National_13_09_01.gsb',
                            'National_84_02_07_01.gsb',
                            'AT_GIS_GRID.gsb',
                            'AT_GIS_GRID_2021_09_28.gsb',
                            '100800401.gsb',
                            'SPED2ETV2.gsb') or \
                src_basename.startswith('GDA94_GDA2020'):
            # nzgd2kgrid0005 has 20111999, hence D-M-Y
            day = int(src_date[0:2])
            month = int(src_date[2:4])
            year = int(src_date[4:8])
        elif src_basename == 'bd72lb72_etrs89lb08.gsb':
            # bd72lb72_etrs89lb08 has 20142308, hence Y-D-M
            year = int(src_date[0:4])
            day = int(src_date[4:6])
            month = int(src_date[6:8])
        else:
            year = int(src_date[0:4])
            month = int(src_date[4:6])
            day = int(src_date[6:8])
    return year, month, day


def create_unoptimized_file(sourcefilename, tmpfilename, args):
    src_ds = gdal.Open(sourcefilename)
    assert src_ds.GetDriver().ShortName in ('NTv2', 'NTv1', 'CTable2')
    subdatsets = [(sourcefilename, None)]
    subdatsets += src_ds.GetSubDatasets()

    if src_ds.GetDriver().ShortName in ('NTv1', 'CTable2'):
        args.do_not_write_accuracy_samples = True

    # Build a subgrids dict whose key is a parent grid name and the
    # value the list of subgrids
    subgrids = {}
    for subds in subdatsets:
        src_ds = gdal.Open(subds[0])
        parent_grid_name = src_ds.GetMetadataItem('PARENT')
        if parent_grid_name is None or parent_grid_name == 'NONE':
            continue
        grid_name = src_ds.GetMetadataItem('SUB_NAME')
        if parent_grid_name in subgrids:
            subgrids[parent_grid_name].append(grid_name)
        else:
            subgrids[parent_grid_name] = [grid_name]

    src_basename = os.path.basename(args.source)

    if args.do_not_write_accuracy_samples:
        nbands = 2
    else:
        _, max = src_ds.GetRasterBand(3).ComputeRasterMinMax()
        if max <= 0:
            print('Omitting accuracy bands which contain only <= 0 values')
            nbands = 2
            args.do_not_write_accuracy_samples = True
        else:
            if not args.accuracy_unit:
                if src_basename in ('rdtrans2008.gsb',
                                    'rdtrans2018.gsb',
                                    'bd72lb72_etrs89lb08.gsb',
                                    'ntv2_0.gsb',
                                    'MAY76V20.gsb',
                                    'ABCSRSV4.GSB',
                                    'BC_27_05.GSB',
                                    'BC_93_05.GSB',
                                    'CQ77SCRS.GSB',
                                    'CRD27_00.GSB',
                                    'CRD93_00.GSB',
                                    'GS7783.GSB',
                                    'NA27SCRS.GSB',
                                    'NA83SCRS.GSB',
                                    'NB2783v2.GSB',
                                    'NB7783v2.GSB',
                                    'NS778302.GSB',
                                    'NVI93_05.GSB',
                                    'ON27CSv1.GSB',
                                    'ON76CSv1.GSB',
                                    'ON83CSv1.GSB',
                                    'PE7783V2.GSB',
                                    'SK27-98.GSB',
                                    'SK83-98.GSB',
                                    'TO27CSv1.GSB',
                                    'rdcorr2018.gsb',):
                    args.accuracy_unit = 'metre'

                elif src_basename in ('ntf_r93.gsb',
                                      'nzgd2kgrid0005.gsb',
                                      'OSTN15_NTv2_OSGBtoETRS.gsb',
                                      'CHENyx06a.gsb',
                                      'CHENyx06_ETRS.gsb',
                                      'A66_National_13_09_01.gsb',
                                      'National_84_02_07_01.gsb',
                                      'GDA94_GDA2020_conformal_and_distortion.gsb',
                                      'DLx_ETRS89_geo.gsb',
                                      'D73_ETRS89_geo.gsb'):
                    args.accuracy_unit = 'arc-second'

                else:
                    raise Exception(
                        '--accuracy-unit=arc-second/metre should be specified')
            nbands = 4

    compact_md = True if len(subdatsets) > 50 else False

    for idx_ifd, subds in enumerate(subdatsets):
        src_ds = gdal.Open(subds[0])
        if src_ds.GetDriver().ShortName == 'NTv2':
            assert src_ds.GetMetadataItem('GS_TYPE') == 'SECONDS'

        tmp_ds = gdal.GetDriverByName('GTiff').Create('/vsimem/tmp',
                                                      src_ds.RasterXSize,
                                                      src_ds.RasterYSize,
                                                      nbands,
                                                      gdal.GDT_Float32 if not args.uint16_encoding else gdal.GDT_UInt16)
        src_crs = osr.SpatialReference()
        if src_crs.SetFromUserInput(args.source_crs) != 0:
            raise Exception('Invalid source crs')
        if not src_crs.IsGeographic():
            raise Exception('Source crs should be a geographic CRS')
        tmp_ds.SetSpatialRef(src_crs)
        tmp_ds.SetGeoTransform(src_ds.GetGeoTransform())
        tmp_ds.SetMetadataItem('AREA_OR_POINT', 'Point')

        grid_name = src_ds.GetMetadataItem('SUB_NAME')
        if grid_name:
            if src_basename == 'NVI93_05.GSB' and grid_name == 'NVIsib':
                grid_name = grid_name + str(idx_ifd+1)
                print('Fixing wrong SUB_NAME of NVI93_05.GSB to ' + grid_name)
            tmp_ds.SetMetadataItem('grid_name', grid_name)
        parent_grid_name = src_ds.GetMetadataItem('PARENT')
        if parent_grid_name is None or parent_grid_name == 'NONE':
            tmp_ds.SetMetadataItem('TYPE', 'HORIZONTAL_OFFSET')
        else:
            tmp_ds.SetMetadataItem('parent_grid_name', parent_grid_name)
        if grid_name in subgrids:
            tmp_ds.SetMetadataItem(
                'number_of_nested_grids', str(len(subgrids[grid_name])))

        if idx_ifd == 0 or not compact_md:
            # Indicates that positive shift values are corrections to the west !
            tmp_ds.GetRasterBand(2).SetMetadataItem('positive_value',
                                                    args.positive_longitude_shift_value)

        if args.uint16_encoding:
            assert src_ds.GetDriver().ShortName == 'NTv2'
            for i in (1, 2):
                min, max = src_ds.GetRasterBand(i).ComputeRasterMinMax()
                data = src_ds.GetRasterBand(i).ReadAsArray()
                scale = (max - min) / 65535
                if i == 2 and args.positive_longitude_shift_value == 'east':
                    data = -data
                data = (data - min) / scale
                tmp_ds.GetRasterBand(i).WriteArray(data)
                tmp_ds.GetRasterBand(i).SetOffset(min)
                tmp_ds.GetRasterBand(i).SetScale(scale)
                if idx_ifd == 0 or not compact_md:
                    tmp_ds.GetRasterBand(i).SetDescription(
                        'latitude_offset' if i == 1 else 'longitude_offset')
                    tmp_ds.GetRasterBand(i).SetUnitType('arc-second')

            if nbands == 4:
                for i in (3, 4):
                    min, max = src_ds.GetRasterBand(i).ComputeRasterMinMax()
                    data = src_ds.GetRasterBand(i).ReadAsArray()
                    scale = (max - min) / 65535
                    if scale == 0:
                        data = 0 * data
                    else:
                        data = (data - min) / scale
                    tmp_ds.GetRasterBand(i).WriteArray(data)
                    tmp_ds.GetRasterBand(i).SetOffset(min)
                    tmp_ds.GetRasterBand(i).SetScale(scale)
                    if idx_ifd == 0 or not compact_md:
                        tmp_ds.GetRasterBand(i).SetDescription(
                            'latitude_offset_accuracy' if i == 3 else 'longitude_offset_accuracy')
                        tmp_ds.GetRasterBand(i).SetUnitType(args.accuracy_unit)

        else:
            for i in (1, 2):
                data = src_ds.GetRasterBand(i).ReadRaster(
                    buf_type=gdal.GDT_Float32)

                if src_ds.GetDriver().ShortName == 'CTable2':
                    nvalues = src_ds.RasterXSize * src_ds.RasterYSize
                    # From radian to arc-seconds
                    data = b''.join(struct.pack('f', v / math.pi * 180.0 * 3600) for v in struct.unpack('f' * nvalues, data))
                if i == 2 and args.positive_longitude_shift_value == 'east':
                    nvalues = src_ds.RasterXSize * src_ds.RasterYSize
                    data = b''.join(struct.pack('f', -v) for v in struct.unpack('f' * nvalues, data))
                tmp_ds.GetRasterBand(i).WriteRaster(0, 0, src_ds.RasterXSize, src_ds.RasterYSize,
                                                    data)
                if idx_ifd == 0 or not compact_md:
                    tmp_ds.GetRasterBand(i).SetDescription(
                        'latitude_offset' if i == 1 else 'longitude_offset')
                    tmp_ds.GetRasterBand(i).SetUnitType('arc-second')

            if nbands == 4:
                for i in (3, 4):
                    data = src_ds.GetRasterBand(i).ReadRaster()
                    tmp_ds.GetRasterBand(i).WriteRaster(0, 0, src_ds.RasterXSize, src_ds.RasterYSize,
                                                        data)
                    if idx_ifd == 0 or not compact_md:
                        tmp_ds.GetRasterBand(i).SetDescription(
                            'latitude_offset_accuracy' if i == 3 else 'longitude_offset_accuracy')
                        tmp_ds.GetRasterBand(i).SetUnitType(args.accuracy_unit)

        dst_crs = osr.SpatialReference()
        if dst_crs.SetFromUserInput(args.target_crs) != 0:
            raise Exception('Invalid target crs')
        if not dst_crs.IsGeographic():
            raise Exception('Target crs should be a geographic CRS')
        dst_auth_name = dst_crs.GetAuthorityName(None)
        dst_auth_code = dst_crs.GetAuthorityCode(None)
        if idx_ifd == 0 or not compact_md:
            if dst_auth_name == 'EPSG' and dst_auth_code:
                tmp_ds.SetMetadataItem('target_crs_epsg_code', dst_auth_code)
            else:
                tmp_ds.SetMetadataItem(
                    'target_crs_wkt', dst_crs.ExportToWkt(['FORMAT=WKT2_2018']))

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

                extra_info = []
                version = src_ds.GetMetadataItem('VERSION')
                if version:
                    version = version.strip()
                    if version not in ('NTv2.0',):
                        extra_info.append('version ' + version)

                src_date = src_ds.GetMetadataItem('UPDATED')
                created_date = src_ds.GetMetadataItem('CREATED')
                if src_date:
                    src_date = src_date.strip()
                if created_date:
                    created_date = created_date.strip()
                    if not src_date:
                        src_date = created_date

                if created_date and src_date and len(src_date) < len(created_date):
                    # SK27-98.GSB
                    #  CREATED=00-02-04
                    #  UPDATED=0-15-00
                    # SK83-98.GSB
                    #  CREATED=98-12-18
                    #  UPDATED=0-15-06
                    src_date = created_date

                if src_date:
                    year, month, day = get_year_month_day(
                        src_date, src_basename)

                    # Various sanity checks
                    assert day >= 1 and day <= 31
                    assert month >= 1 and month <= 12
                    assert year >= 1980
                    assert year <= datetime.datetime.now().year
                    # assume agencies only work monday to friday...
                    # except in Belgium where they work on sundays
                    # and in NZ on saturdays
                    if src_basename not in ('nzgd2kgrid0005.gsb',
                                            'bd72lb72_etrs89lb08.gsb',
                                            'GS7783.GSB',
                                            'NB2783v2.GSB',
                                            'ON27CSv1.GSB',
                                            'ON76CSv1.GSB',
                                            ):
                        assert datetime.datetime(
                            year, month, day).weekday() <= 4

                    # Sanity check that creation_date <= last_updated_date
                    if created_date:
                        year_created, month_created, day_created = get_year_month_day(
                            created_date, src_basename)
                        assert year_created * 10000 + month_created * 100 + \
                            day_created <= year * 10000 + month * 100 + day

                    extra_info.append(
                        'last updated on %04d-%02d-%02d' % (year, month, day))

                if extra_info:
                    desc += ' (' + ', '.join(extra_info) + ')'

            tmp_ds.SetMetadataItem('TIFFTAG_IMAGEDESCRIPTION', desc)
            if args.copyright:
                tmp_ds.SetMetadataItem('TIFFTAG_COPYRIGHT', args.copyright)
            if args.datetime and args.datetime != 'NONE':
                tmp_ds.SetMetadataItem('TIFFTAG_DATETIME', args.datetime)
            if args.area_of_use:
                tmp_ds.SetMetadataItem('area_of_use', args.area_of_use)

        options = ['PHOTOMETRIC=MINISBLACK',
                   'COMPRESS=DEFLATE',
                   'PREDICTOR=3' if not args.uint16_encoding else 'PREDICTOR=2',
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
    assert src_ds.GetDriver().ShortName in ('NTv2', 'NTv1', 'CTable2')
    src_subdatsets = [(sourcefilename, None)]
    src_subdatsets += src_ds.GetSubDatasets()

    dst_ds = gdal.Open(destfilename)
    dst_subdatsets = dst_ds.GetSubDatasets()
    if not dst_subdatsets:
        dst_subdatsets = [(destfilename, None)]

    assert len(src_subdatsets) == len(dst_subdatsets)
    for src_subds, dst_subds in zip(src_subdatsets, dst_subdatsets):
        src_ds = gdal.Open(src_subds[0])
        dst_ds = gdal.Open(dst_subds[0])
        if not args.uint16_encoding:
            for i in range(min(src_ds.RasterCount, dst_ds.RasterCount)):
                data = src_ds.GetRasterBand(
                    i+1).ReadRaster(buf_type=gdal.GDT_Float32)

                if src_ds.GetDriver().ShortName == 'CTable2':
                    nvalues = src_ds.RasterXSize * src_ds.RasterYSize
                    # From radian to arc-seconds
                    data = b''.join(struct.pack('f', v / math.pi * 180.0 * 3600) for v in struct.unpack('f' * nvalues, data))

                if i+1 == 2 and args.positive_longitude_shift_value == 'east':
                    nvalues = src_ds.RasterXSize * src_ds.RasterYSize
                    data = b''.join(struct.pack('f', -v) for v in struct.unpack('f' * nvalues, data))
                assert dst_ds.GetRasterBand(i+1).ReadRaster() == data
        else:
            import numpy as np
            for i in range(min(src_ds.RasterCount, dst_ds.RasterCount)):
                src_data = src_ds.GetRasterBand(i+1).ReadAsArray()
                dst_data = dst_ds.GetRasterBand(i+1).ReadAsArray()
                offset = dst_ds.GetRasterBand(i+1).GetOffset()
                scale = dst_ds.GetRasterBand(i+1).GetScale()
                dst_data = dst_data * scale + offset
                if i+1 == 2 and args.positive_longitude_shift_value == 'east':
                    dst_data = -dst_data
                max_error = np.max(abs(dst_data - src_data))
                assert max_error <= 1.01 * scale / 2, (max_error, scale / 2)


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
