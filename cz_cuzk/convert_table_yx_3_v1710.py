#!/usr/bin/env python

# SPDX-License-Identifier: MIT
# Copyright 2024, Even Rouault <even.rouault at spatialys.com>
# Convert file table_yx_3_v1710.dat(https://www.cuzk.cz/Zememerictvi/Geodeticke-zaklady-na-uzemi-CR/GNSS/Nova-realizace-systemu-ETRS89-v-CR/table_yx_3_v1710.aspx)
# doing S-JTSK to S-JTSK/05 shifts (in projected units) to GTG.

import datetime
import os
from osgeo import gdal, osr

gdal.UseExceptions()

src_filename = "table_yx_3_v1710.dat"

assert os.path.exists(src_filename), "Download file table_yx_3_v1710.dat from https://www.cuzk.cz/Zememerictvi/Geodeticke-zaklady-na-uzemi-CR/GNSS/Nova-realizace-systemu-ETRS89-v-CR/table_yx_3_v1710.aspx"

ds = gdal.Open(src_filename)
delta_westing = ds.GetRasterBand(1).ReadAsArray()

tmp_tif_name = "table_yx_3_v1710_east_north_tmp.tif"
width = ds.RasterXSize
height = ds.RasterYSize
out_ds = gdal.GetDriverByName("GTiff").Create(tmp_tif_name,
                                              width,
                                              height,
                                              2, # number of bands
                                              gdal.GDT_Float32)
orig_gt = ds.GetGeoTransform()
horizontal_res = orig_gt[1]
vertical_res = orig_gt[5]
assert vertical_res > 0  # XYZ driver returns a "south-up" raster
# min_westing = orig_gt[0]
min_southing = orig_gt[3]
max_westing = orig_gt[0] + horizontal_res * width
# max_southing = orig_gt[3] + vertical_res * height

min_easting = -max_westing
max_northing = -min_southing
gt = [ min_easting, horizontal_res, 0, max_northing, 0, -vertical_res ]
out_ds.SetGeoTransform(gt)

srs = osr.SpatialReference()
srs.ImportFromEPSG(5514) # S-JTSK / Krovak East North
out_ds.SetSpatialRef(srs)

OFFSET_SJTSK_TO_SJTSK05 = -5000000

md = {}
md["area_of_use"] = "Czechia"
md["AREA_OR_POINT"] = "Point"
md["target_crs_epsg_code"] = "5516" # S-JTSK/05 / Modified Krovak East North
md["TIFFTAG_COPYRIGHT"] = "Derived from work by Czech Office of Surveying and Cadastre (CUZK). !!!LICENSE TO BE DEFINED!!!"
md["TIFFTAG_IMAGEDESCRIPTION"] = f"S-JTSK / Krovak East North (EPSG:5514) to S-JTSK/05 / Modified Krovak East North (EPSG:5516). Converted from {src_filename} by switching to easting/northing rather than original westing/southing. Note also that an extra offset of {OFFSET_SJTSK_TO_SJTSK05} in easting and northing must be applied"
md["TYPE"] = "HORIZONTAL_OFFSET"
md["TIFFTAG_DATETIME"] = datetime.date.today().strftime("%Y:%m:%d %H:%M:%S")
md["interpolation_method"] = "biquadratic"
out_ds.SetMetadata(md)

source_nodata = ds.GetRasterBand(1).GetNoDataValue()

target_nodata = -9999

# Transform delta_westing into delta_easting by negating the sign of the
# values, and flipping the array in horizontal direction.
delta_easting = -1.0 * delta_westing[...,::-1]
delta_easting[delta_easting == -source_nodata] = target_nodata
delta_easting_band = out_ds.GetRasterBand(1)
delta_easting_band.WriteArray(delta_easting)
delta_easting_band.SetDescription("easting_offset")
delta_easting_band.SetUnitType("metre")
delta_easting_band.SetMetadataItem("positive_value", "east")
delta_easting_band.SetMetadataItem("constant_offset", str(OFFSET_SJTSK_TO_SJTSK05))
delta_easting_band.SetNoDataValue(target_nodata)

tmp_dat_filename = src_filename + ".tmp"
with open(tmp_dat_filename, "wb") as f:
    # Do not be fooled by the labels... They are just for the purpose of
    # the GDAL XYZ driver. So the below X is actually a westing(Y in S-JTSK...),
    # Y a southing (X in S-JTSK...), the ignored column is the delta_westing,
    # and GDAL Z is delta_southing
    f.write(b"X,Y,ignored,Z\n")
    with open(src_filename, "rb") as src_f:
        f.write(src_f.read())

ds = gdal.Open(tmp_dat_filename)
delta_southing = ds.GetRasterBand(1).ReadAsArray()

# Transform delta_southing into delta_northing by negating the sign of the
# values, and flipping the array in horizontal direction.
delta_northing = -1.0 * delta_southing[...,::-1]
delta_northing[delta_northing == -source_nodata] = target_nodata
delata_northing_band = out_ds.GetRasterBand(2)
delata_northing_band.WriteArray(delta_northing)
delata_northing_band.SetDescription("northing_offset")
delata_northing_band.SetUnitType("metre")
delata_northing_band.SetMetadataItem("positive_value", "north")
delata_northing_band.SetMetadataItem("constant_offset", str(OFFSET_SJTSK_TO_SJTSK05))
delata_northing_band.SetNoDataValue(target_nodata)

del out_ds

gdal.Unlink(tmp_dat_filename)

# Generate final file
gdal.Translate("cz_cuzk_table_yx_3_v1710_east_north.tif",
               tmp_tif_name,
               creationOptions=["BLOCKYSIZE=" + str(height), "COMPRESS=LZW", "PREDICTOR=3"])

gdal.Unlink(tmp_tif_name)
