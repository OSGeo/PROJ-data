#!/usr/bin/env python
###############################################################################
# $Id$
#
#  Project:  PROJ
#  Purpose:  Convert New Caledonia geocentric gr3dnc01b.mnt grid
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
import datetime
import struct

with open('gr3dnc01b.mnt', 'rt') as f:
    count_val_rows = 0
    line_no = 0
    for l in f.readlines():
        if l[-1] == '\n':
            l = l[0:-1]
        if l[-1] == '\r':
            l = l[0:-1]
        if not l:
            continue
        if line_no == 0:
            tokens = []
            for t in l.split(' '):
                if t:
                    tokens.append(t)
            assert len(tokens) >= 13
            minx = float(tokens[0])
            maxx = float(tokens[1])
            miny = float(tokens[2])
            maxy = float(tokens[3])
            resx = float(tokens[4])
            resy = float(tokens[5])
            assert minx < maxx
            assert miny < maxy
            assert resx > 0
            assert resy > 0
            cols = 1 + (maxx - minx) / resx
            assert cols - int(cols + 0.5) < 1e-10
            cols = int(cols + 0.5)
            rows = 1 + (maxy - miny) / resy
            assert rows - int(rows + 0.5) < 1e-10
            rows = int(rows + 0.5)
            ds = gdal.GetDriverByName('GTiff').Create(
                '/vsimem/gr3dnc01b.tif', cols, rows, 3, gdal.GDT_Float32)
            ds.SetMetadataItem(
                'TIFFTAG_COPYRIGHT', 'Derived from work by Service Topographique, DITTT, GNC. License unclear')
            ds.SetMetadataItem('TIFFTAG_IMAGEDESCRIPTION',
                               'Geocentric translation from IGN72 GRANDE TERRE (EPSG:4662) to RGNC91-93 (EPSG:4749). Converted from gr3dnc01b.mnt')
            datetime = datetime.date.today().strftime("%Y:%m:%d %H:%M:%S")
            ds.SetMetadataItem('TIFFTAG_DATETIME', datetime)
            ds.SetMetadataItem('AREA_OR_POINT', 'Point')
            ds.SetMetadataItem('TYPE', 'GEOCENTRIC_TRANSLATION')
            ds.SetMetadataItem('area_of_use', 'France')
            ds.SetMetadataItem('source_crs_code', '4662')
            ds.SetMetadataItem('target_crs_epsg_code', '4749')
            ds.SetGeoTransform(
                [minx - resx/2, resx, 0, maxy + resy/2, 0, -resy])
            ds.GetRasterBand(1).SetUnitType('metre')
            ds.GetRasterBand(1).SetDescription('x_translation')
            ds.GetRasterBand(2).SetUnitType('metre')
            ds.GetRasterBand(2).SetDescription('y_translation')
            ds.GetRasterBand(3).SetUnitType('metre')
            ds.GetRasterBand(3).SetDescription('z_translation')
            sr = osr.SpatialReference()
            sr.ImportFromEPSG(4749)
            ds.SetProjection(sr.ExportToWkt())
        else:
            tokens = []
            for t in l.split(' '):
                if t:
                    tokens.append(t)
            assert len(tokens) == 6
            lon = float(tokens[0])
            lat = float(tokens[1])
            dx = float(tokens[2])
            dy = float(tokens[3])
            dz = float(tokens[4])
            iy = (line_no - 1) % rows
            ix = (line_no - 1) // rows
            assert abs(lon - (minx + ix * resx)
                       ) < 1e-10, (line_no, lon, minx + ix * resx)
            assert abs(lat - (miny + iy * resy)
                       ) < 1e-10, (line_no, lat, miny + iy * resy)
            ds.GetRasterBand(1).WriteRaster(
                ix, rows - iy - 1, 1, 1, struct.pack('f', dx))
            ds.GetRasterBand(2).WriteRaster(
                ix, rows - iy - 1, 1, 1, struct.pack('f', dy))
            ds.GetRasterBand(3).WriteRaster(
                ix, rows - iy - 1, 1, 1, struct.pack('f', dz))
            count_val_rows += 1

        line_no += 1

    assert count_val_rows == rows * cols
    gdal.GetDriverByName('GTiff').CreateCopy('gr3dnc01b.tif', ds, options=[
        'COMPRESS=DEFLATE', 'PREDICTOR=3', 'INTERLEAVE=BAND'])
