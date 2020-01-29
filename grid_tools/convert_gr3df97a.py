#!/usr/bin/env python
###############################################################################
# $Id$
#
#  Project:  PROJ
#  Purpose:  Convert IGN France geocentric gr3df97a.txt grid
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

# https://geodesie.ign.fr/contenu/fichiers/gr3df97a.txt

with open('gr3df97a.txt', 'rt') as f:
    count_val_rows = 0
    for line_no, l in enumerate(f.readlines()):
        if l[-1] == '\n':
            l = l[0:-1]
        if l[-1] == '\r':
            l = l[0:-1]
        if line_no == 0:
            assert l.startswith(' GR3D ')
        elif line_no == 1:
            assert l.startswith(' GR3D1 ')
            tokens = []
            for t in l.split(' '):
                if t:
                    tokens.append(t)
            assert len(tokens) == 7
            minx = float(tokens[1])
            maxx = float(tokens[2])
            miny = float(tokens[3])
            maxy = float(tokens[4])
            resx = float(tokens[5])
            resy = float(tokens[6])
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
                '/vsimem/gr3df97a.tif', cols, rows, 3, gdal.GDT_Float32)
            ds.SetMetadataItem(
                'TIFFTAG_COPYRIGHT', 'Derived from work by IGN France. Open License https://www.etalab.gouv.fr/wp-content/uploads/2014/05/Open_Licence.pdf')
            ds.SetMetadataItem('TIFFTAG_IMAGEDESCRIPTION',
                               'Geocentric translation from NTF (IGNF:NTF) to RGF93 (EPSG:4964). Converted from gr3df97a.txt')
            datetime = datetime.date.today().strftime("%Y:%m:%d %H:%M:%S")
            ds.SetMetadataItem('TIFFTAG_DATETIME', datetime)
            ds.SetMetadataItem('AREA_OR_POINT', 'Point')
            ds.SetMetadataItem('TYPE', 'GEOCENTRIC_TRANSLATION')
            ds.SetMetadataItem('area_of_use', 'France')
            ds.SetMetadataItem('source_crs_wkt', """GEODCRS["NTF cartesiennes",
    DATUM["Nouvelle Triangulation Francaise",
        ELLIPSOID["Clarke 1880 (IGN)",6378249.2,293.466021293627,
            LENGTHUNIT["metre",1]]],
    PRIMEM["Greenwich",0,
        ANGLEUNIT["degree",0.0174532925199433]],
    CS[Cartesian,3],
        AXIS["(X)",geocentricX,
            ORDER[1],
            LENGTHUNIT["metre",1]],
        AXIS["(Y)",geocentricY,
            ORDER[2],
            LENGTHUNIT["metre",1]],
        AXIS["(Z)",geocentricZ,
            ORDER[3],
            LENGTHUNIT["metre",1]],
    USAGE[
        SCOPE["unknown"],
        AREA["FRANCE METROPOLITAINE (CORSE COMPRISE)"],
        BBOX[41,-5.5,52,10]],
    ID["IGNF","NTF"]]""")
            ds.SetMetadataItem('target_crs_epsg_code', '4964')
            ds.SetGeoTransform(
                [minx - resx/2, resx, 0, maxy + resy/2, 0, -resy])
            ds.GetRasterBand(1).SetUnitType('metre')
            ds.GetRasterBand(1).SetDescription('x_translation')
            ds.GetRasterBand(2).SetUnitType('metre')
            ds.GetRasterBand(2).SetDescription('y_translation')
            ds.GetRasterBand(3).SetUnitType('metre')
            ds.GetRasterBand(3).SetDescription('z_translation')
            sr = osr.SpatialReference()
            sr.ImportFromEPSG(4171)  # RGF93
            ds.SetProjection(sr.ExportToWkt())
        elif line_no == 2:
            assert l.startswith(' GR3D2 ')
        elif line_no == 3:
            assert l.startswith(' GR3D3 ')
        else:
            assert l.startswith('00002 ')
            tokens = []
            for t in l.split(' '):
                if t:
                    tokens.append(t)
            assert len(tokens) == 8
            lon = float(tokens[1])
            lat = float(tokens[2])
            dx = float(tokens[3])
            dy = float(tokens[4])
            dz = float(tokens[5])
            iy = (line_no - 4) % rows
            ix = (line_no - 4) // rows
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

    assert count_val_rows == rows * cols
    gdal.GetDriverByName('GTiff').CreateCopy('gr3df97a.tif', ds, options=[
        'COMPRESS=DEFLATE', 'PREDICTOR=3', 'INTERLEAVE=BAND'])
