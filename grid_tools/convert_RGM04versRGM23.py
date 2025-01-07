#!/usr/bin/env python
###############################################################################
#  Project:  PROJ
#  Purpose:  Convert IGN France geocentric RGM04versRGM23.txt grid
#  Author:   Even Rouault <even.rouault at spatialys.com>
#
###############################################################################
#  Copyright (c) 2025, Even Rouault <even.rouault at spatialys.com>
#
# SPDX-License-Identifier: MIT
###############################################################################

from osgeo import gdal
from osgeo import osr
import datetime
import struct

# https://geodesie.ign.fr/contenu/fichiers/documentation/RGM04versRGM23.txt

with open('RGM04versRGM23.txt', 'rt') as f:
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
                               'Geocentric translation from RGM04 (EPSG:4468) to RGM23 (EPSG:10669). Converted from RGM04versRGM23.txt')
            datetime = datetime.date.today().strftime("%Y:%m:%d %H:%M:%S")
            ds.SetMetadataItem('TIFFTAG_DATETIME', datetime)
            ds.SetMetadataItem('AREA_OR_POINT', 'Point')
            ds.SetMetadataItem('TYPE', 'GEOCENTRIC_TRANSLATION')
            ds.SetMetadataItem('area_of_use', 'Mayotte')
            ds.SetMetadataItem('source_crs_epsg_code', '4468')
            ds.SetMetadataItem('target_crs_epsg_code', '10669')
            ds.SetGeoTransform(
                [minx - resx/2, resx, 0, maxy + resy/2, 0, -resy])
            ds.GetRasterBand(1).SetUnitType('metre')
            ds.GetRasterBand(1).SetDescription('x_translation')
            ds.GetRasterBand(2).SetUnitType('metre')
            ds.GetRasterBand(2).SetDescription('y_translation')
            ds.GetRasterBand(3).SetUnitType('metre')
            ds.GetRasterBand(3).SetDescription('z_translation')
            sr = osr.SpatialReference()
            sr.ImportFromEPSG(10671)  # RGM23
            ds.SetProjection(sr.ExportToWkt())
        elif line_no == 2:
            assert l.startswith(' GR3D2 ')
        elif line_no == 3:
            assert l.startswith(' GR3D3 ')
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
    gdal.GetDriverByName('GTiff').CreateCopy('fr_ign_RGM04versRGM23.tif', ds, options=[
        'COMPRESS=DEFLATE', 'PREDICTOR=3', 'INTERLEAVE=BAND'])
