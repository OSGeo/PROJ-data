from osgeo import gdal, osr
import os
import requests

import sys
sys.path.append("../grid_tools")
from cloud_optimize_gtiff import generate_optimized_file

base_url = "https://geodesy.noaa.gov/pub/nadcon5/20160901release/Builds"

build_number = "20160901"
subdirs = ["as62.nad83_1993.as",
           "gu63.nad83_1993.guamcnmi",
           "nad27.nad83_1986.alaska",
           "nad27.nad83_1986.conus",
           "nad83_1986.nad83_1992.alaska",
           "nad83_1986.nad83_1993.hawaii",
           "nad83_1986.nad83_1993.prvi",
           "nad83_1986.nad83_harn.conus",
           "nad83_1992.nad83_2007.alaska",
           "nad83_1993.nad83_1997.prvi",
           "nad83_1993.nad83_2002.as",
           "nad83_1993.nad83_2002.guamcnmi",
           "nad83_1993.nad83_pa11.hawaii",
           "nad83_1997.nad83_2002.prvi",
           "nad83_2002.nad83_2007.prvi",
           "nad83_2002.nad83_ma11.guamcnmi",
           "nad83_2002.nad83_pa11.as",
           "nad83_2007.nad83_2011.alaska",
           "nad83_2007.nad83_2011.conus",
           "nad83_2007.nad83_2011.prvi",
           "nad83_fbn.nad83_2007.conus",
           "nad83_harn.nad83_fbn.conus",
           "ohd.nad83_1986.hawaii",
           "pr40.nad83_1986.prvi",
           #"sg1897.sg1952.stgeorge",
           "sg1952.nad83_1986.stgeorge",
           "sl1952.nad83_1986.stlawrence",
           #"sp1897.sp1952.stpaul",
           "sp1952.nad83_1986.stpaul",
           #"ussd.nad27.conus",
]

d = {
    "as62.nad83_1993.as": {
        "source_crs": "EPSG:4169",
        "target_crs": "EPSG:4152",
        "area_of_use": "USA - American Samoa",
    },
    "gu63.nad83_1993.guamcnmi": {
        "source_crs": "EPSG:4675",
        "target_crs": "EPSG:4152",
        "area_of_use": "USA - Guam and the Commonwealth of the Northern Mariana Islands",
    },
    "nad27.nad83_1986.alaska": {
        "source_crs": "EPSG:4267",
        "target_crs": "EPSG:4269",
        "area_of_use": "USA - Alaska",
    },
    "nad27.nad83_1986.conus": {
        "source_crs": "EPSG:4267",
        "target_crs": "EPSG:4269",
        "area_of_use": "USA - Conterminous",
    },
    "nad83_1986.nad83_1992.alaska": {
        "source_crs": "EPSG:4269",
        "target_crs": "EPSG:4152",
        "area_of_use": "USA - Alaska",
    },
    "nad83_1986.nad83_1993.hawaii": {
        "source_crs": "EPSG:4269",
        "target_crs": "EPSG:4152",
        "area_of_use": "USA - Hawaii",
    },
    "nad83_1986.nad83_1993.prvi": {
        "source_crs": "EPSG:4269",
        "target_crs": "EPSG:4152",
        "area_of_use": "USA - Puerto Rico and the Virgin Islands",
    },
    "nad83_1986.nad83_harn.conus": {
        "source_crs": "EPSG:4269",
        "target_crs": "EPSG:4152",
        "area_of_use": "USA - Conterminous",
    },
    "nad83_1992.nad83_2007.alaska": {
        "source_crs": "EPSG:4152",
        "target_crs": "EPSG:4759",
        "area_of_use": "USA - Alaska",
    },
    "nad83_1993.nad83_1997.prvi": {
        "source_crs": "EPSG:4152",
        "target_crs": "EPSG:8545",
        "area_of_use": "USA - Puerto Rico and the Virgin Islands",
    },
    "nad83_1993.nad83_2002.as": {
        "source_crs": "EPSG:4152",
        "target_crs": "EPSG:8860",
        "area_of_use": "USA - American Samoa",
    },
    "nad83_1993.nad83_2002.guamcnmi": {
        "source_crs": "EPSG:4152",
        "target_crs": "EPSG:8860",
        "area_of_use": "USA - Guam and the Commonwealth of the Northern Mariana Islands",
    },
    "nad83_1993.nad83_pa11.hawaii": {
        "source_crs": "EPSG:4152",
        "target_crs": "EPSG:6322",
        "area_of_use": "USA - Hawaii",
    },
    "nad83_1997.nad83_2002.prvi": {
        "source_crs": "EPSG:8545",
        "target_crs": "EPSG:8860",
        "area_of_use": "USA - Puerto Rico and the Virgin Islands",
    },
    "nad83_2002.nad83_2007.prvi": {
        "source_crs": "EPSG:8860",
        "target_crs": "EPSG:4759",
        "area_of_use": "USA - Puerto Rico and the Virgin Islands",
    },
    "nad83_2002.nad83_ma11.guamcnmi": {
        "source_crs": "EPSG:8860",
        "target_crs": "EPSG:6325",
        "area_of_use": "USA - Guam and the Commonwealth of the Northern Mariana Islands",
    },
    "nad83_2002.nad83_pa11.as": {
        "source_crs": "EPSG:8860",
        "target_crs": "EPSG:6322",
        "area_of_use": "USA - American Samoaa",
    },
    "nad83_2007.nad83_2011.alaska": {
        "source_crs": "EPSG:4759",
        "target_crs": "EPSG:6318",
        "area_of_use": "USA - Alaska",
    },
    "nad83_2007.nad83_2011.conus": {
        "source_crs": "EPSG:4759",
        "target_crs": "EPSG:6318",
        "area_of_use": "USA - Conterminous",
    },
    "nad83_2007.nad83_2011.prvi": {
        "source_crs": "EPSG:4759",
        "target_crs": "EPSG:6318",
        "area_of_use": "USA - Puerto Rico and the Virgin Islands",
    },
    "nad83_fbn.nad83_2007.conus": {
        "source_crs": "EPSG:8860",
        "target_crs": "EPSG:4759",
        "area_of_use": "USA - Conterminous",
    },
    "nad83_harn.nad83_fbn.conus": {
        "source_crs": "EPSG:4152",
        "target_crs": "EPSG:8860",
        "area_of_use": "USA - Conterminous",
    },
    "ohd.nad83_1986.hawaii": {
        "source_crs": "EPSG:4135",
        "target_crs": "EPSG:4269",
        "area_of_use": "USA - Hawaii",
    },
    "pr40.nad83_1986.prvi": {
        "source_crs": "EPSG:4139",
        "target_crs": "EPSG:4269",
        "area_of_use": "USA - Puerto Rico and the Virgin Islands",
    },
    #"sg1897.sg1952.stgeorge",
    "sg1952.nad83_1986.stgeorge": {
        "source_crs": "EPSG:4138",
        "target_crs": "EPSG:4269",
        "area_of_use": "USA - Saint George Island",
    },
    "sl1952.nad83_1986.stlawrence": {
        "source_crs": "EPSG:4136",
        "target_crs": "EPSG:4269",
        "area_of_use": "USA - Saint Lawrence Island",
    },
    #"sp1897.sp1952.stpaul",
    "sp1952.nad83_1986.stpaul": {
        "source_crs": "EPSG:4137",
        "target_crs": "EPSG:4269",
        "area_of_use": "USA - Saint Lawrence Island",
    },
#"ussd.nad27.conus",
}

os.makedirs("nadcon5", exist_ok=True)

readme_txt = ""

for subdir in subdirs:

    lat_filename = "nadcon5." + subdir + ".lat.trn." + build_number + ".b"
    out_filename = "nadcon5/" + lat_filename
    if not os.path.exists(out_filename):
        url = base_url + "/" + subdir + "/" + lat_filename
        print(f"Fetch {url}...")
        r = requests.get(url)
        open(out_filename, "wb").write(r.content)
        ds = gdal.Open(out_filename)
        assert ds.GetRasterBand(1).Checksum() >= 0

    lon_filename = "nadcon5." + subdir + ".lon.trn." + build_number + ".b"
    out_filename = "nadcon5/" + lon_filename
    if not os.path.exists(out_filename):
        url = base_url + "/" + subdir + "/" + lon_filename
        print(f"Fetch {url}...")
        r = requests.get(url)
        open(out_filename, "wb").write(r.content)
        ds = gdal.Open(out_filename)
        assert ds.GetRasterBand(1).Checksum() >= 0

    has_ellipsoidal_height_shift = ("nad83_2007" in subdir or "nad83_1997" in subdir or "nad83_2002" in subdir or "nad83_pa11" in subdir or "nad83_fbn" in subdir)
    if has_ellipsoidal_height_shift:
        eht_filename = "nadcon5." + subdir + ".eht.trn." + build_number + ".b"
        out_filename = "nadcon5/" + eht_filename
        if not os.path.exists(out_filename):
            url = base_url + "/" + subdir + "/" + eht_filename
            print(f"Fetch {url}...")
            r = requests.get(url)
            open(out_filename, "wb").write(r.content)
            ds = gdal.Open(out_filename)
            assert ds.GetRasterBand(1).Checksum() >= 0

    source_crs_code = d[subdir]["source_crs"]
    target_crs_code = d[subdir]["target_crs"]
    area_of_use = d[subdir]["area_of_use"]
    source_crs = osr.SpatialReference()
    source_crs.SetFromUserInput(source_crs_code)
    source_crs_name = source_crs.GetName()
    target_crs = osr.SpatialReference()
    target_crs.SetFromUserInput(target_crs_code)

    if has_ellipsoidal_height_shift:
        target_crs.PromoteTo3D()
        target_crs_code = "EPSG:" + target_crs.GetAuthorityCode(None)

    target_crs_name = target_crs.GetName()
    print(f"{subdir} -> {source_crs_code}({source_crs_name}) -> {target_crs_code}({target_crs_name}). {area_of_use}")

    lat_ds = gdal.Open("nadcon5/" + lat_filename)
    lon_ds = gdal.Open("nadcon5/" + lon_filename)
    eht_ds = gdal.Open("nadcon5/" + eht_filename) if has_ellipsoidal_height_shift else None
    assert lat_ds.RasterXSize == lon_ds.RasterXSize
    assert lat_ds.RasterYSize == lon_ds.RasterYSize
    lon_gt = lon_ds.GetGeoTransform()
    lat_gt = lat_ds.GetGeoTransform()
    assert lon_gt == lat_gt

    ellipsoidal_same_resolution = False
    if has_ellipsoidal_height_shift:
        if eht_ds.RasterXSize == lon_ds.RasterXSize and eht_ds.RasterYSize == lon_ds.RasterYSize:
            ellipsoidal_same_resolution = True
        elif eht_ds.RasterXSize == 1 + lon_ds.RasterXSize // 2 and eht_ds.RasterYSize == 1 + lon_ds.RasterYSize // 2:
            pass
        elif eht_ds.RasterXSize == 1 + lon_ds.RasterXSize // 3 and eht_ds.RasterYSize == 1 + lon_ds.RasterYSize // 3:
            pass
        elif eht_ds.RasterXSize == 1 + lon_ds.RasterXSize // 4 and eht_ds.RasterYSize == 1 + lon_ds.RasterYSize // 4:
            pass
        elif eht_ds.RasterXSize == 1 + lon_ds.RasterXSize // 5 and eht_ds.RasterYSize == 1 + lon_ds.RasterYSize // 5:
            pass
        elif lon_ds.RasterXSize == 1 + eht_ds.RasterXSize // 2 and lon_ds.RasterYSize == 1 + eht_ds.RasterYSize // 2:
            pass
        elif lon_ds.RasterXSize == 1 + eht_ds.RasterXSize // 3 and lon_ds.RasterYSize == 1 + eht_ds.RasterYSize // 3:
            pass
        elif lon_ds.RasterXSize - 1 == (eht_ds.RasterXSize - 1) * 6 // 10 and lon_ds.RasterYSize - 1 == (eht_ds.RasterYSize - 1) * 6 // 10:
            pass
        elif eht_ds.RasterXSize - 1 == (lon_ds.RasterXSize - 1) * 6 // 10 and eht_ds.RasterYSize - 1 == (lon_ds.RasterYSize - 1) * 6 // 10:
            pass
        else:
            assert False, eht_filename

        # Check spatial extent is same
        eht_gt = eht_ds.GetGeoTransform()
        assert lon_gt[0] + lon_gt[1] / 2 == eht_gt[0] + eht_gt[1] / 2
        assert (lon_ds.RasterXSize - 1) * lon_gt[1] == (eht_ds.RasterXSize - 1) * eht_gt[1]
        assert lon_gt[3] + lon_gt[5] / 2 == eht_gt[3] + eht_gt[5] / 2
        assert (lon_ds.RasterYSize - 1) * lon_gt[5] == (eht_ds.RasterYSize - 1) * eht_gt[5]


    mem_ds = gdal.GetDriverByName("MEM").Create("", lon_ds.RasterXSize, lon_ds.RasterYSize, 3 if ellipsoidal_same_resolution else 2, gdal.GDT_Float32)
    mem_ds.SetGeoTransform(lon_gt)
    mem_ds.SetSpatialRef(source_crs)

    mem_ds.GetRasterBand(1).WriteRaster(0, 0, lon_ds.RasterXSize, lon_ds.RasterYSize, lat_ds.ReadRaster())
    mem_ds.GetRasterBand(1).SetDescription("latitude_offset")
    mem_ds.GetRasterBand(1).SetUnitType("arc-second")

    mem_ds.GetRasterBand(2).WriteRaster(0, 0, lon_ds.RasterXSize, lon_ds.RasterYSize, lon_ds.ReadRaster())
    mem_ds.GetRasterBand(2).SetDescription("longitude_offset")
    mem_ds.GetRasterBand(2).SetMetadataItem("positive_value", "east")
    mem_ds.GetRasterBand(2).SetUnitType("arc-second")

    if ellipsoidal_same_resolution:
        mem_ds.GetRasterBand(3).WriteRaster(0, 0, lon_ds.RasterXSize, lon_ds.RasterYSize, eht_ds.ReadRaster())
        mem_ds.GetRasterBand(3).SetDescription("ellipsoidal_height_offset")
        mem_ds.GetRasterBand(3).SetUnitType("metre")

    mem_ds.SetMetadataItem("area_of_use", area_of_use)
    mem_ds.SetMetadataItem("AREA_OR_POINT", "Point")
    mem_ds.SetMetadataItem("target_crs_epsg_code", target_crs.GetAuthorityCode(None))
    mem_ds.SetMetadataItem("TIFFTAG_COPYRIGHT", "Derived from work by NOAA. Public Domain")
    mem_ds.SetMetadataItem("TIFFTAG_DATETIME", "2016:09:01 00:00:00")
    description = f"{source_crs_code} ({source_crs_name}) to {target_crs_code} ({target_crs_name}). Converted from {base_url}/{subdir}"
    mem_ds.SetMetadataItem("TIFFTAG_IMAGEDESCRIPTION", description)
    if not has_ellipsoidal_height_shift:
        mem_ds.SetMetadataItem("TYPE", "HORIZONTAL_OFFSET")
    elif ellipsoidal_same_resolution:
        mem_ds.SetMetadataItem("TYPE", "GEOGRAPHIC_3D_OFFSET")
    else:
        mem_ds.SetMetadataItem("TYPE", "HORIZONTAL_OFFSET")
        mem_ds.SetMetadataItem("auxiliary_data", "ellipsoidal_height_offset")
    mem_ds.SetMetadataItem("interpolation_method", "biquadratic")

    tiff_filename = "us_noaa_nadcon5_" + subdir.replace('.', '_') + ".tif"
    options = ["COMPRESS=DEFLATE", "PREDICTOR=3"]
    if mem_ds.RasterXSize > 256 or mem_ds.RasterYSize > 256:
        options += ["TILED=YES"]
    else:
        options += ["BLOCKYSIZE=" + str(mem_ds.RasterYSize)]
    assert gdal.GetDriverByName("GTiff").CreateCopy(tiff_filename + ".tmp", mem_ds,
                                                      options = options) is not None

    if has_ellipsoidal_height_shift and not ellipsoidal_same_resolution:

        mem_ds = gdal.GetDriverByName("MEM").Create("", eht_ds.RasterXSize, eht_ds.RasterYSize, 1, gdal.GDT_Float32)
        mem_ds.SetGeoTransform(eht_gt)
        mem_ds.SetSpatialRef(source_crs)
        mem_ds.GetRasterBand(1).WriteRaster(0, 0, eht_ds.RasterXSize, eht_ds.RasterYSize, eht_ds.ReadRaster())
        mem_ds.GetRasterBand(1).SetDescription("ellipsoidal_height_offset")
        mem_ds.GetRasterBand(1).SetUnitType("metre")

        mem_ds.SetMetadataItem("area_of_use", area_of_use)
        mem_ds.SetMetadataItem("AREA_OR_POINT", "Point")
        mem_ds.SetMetadataItem("target_crs_epsg_code", target_crs.GetAuthorityCode(None))
        mem_ds.SetMetadataItem("TIFFTAG_COPYRIGHT", "Derived from work by NOAA. Public Domain")
        mem_ds.SetMetadataItem("TIFFTAG_DATETIME", "2016:09:01 00:00:00")
        mem_ds.SetMetadataItem("TIFFTAG_IMAGEDESCRIPTION", description)
        mem_ds.SetMetadataItem("TYPE", "ELLIPSOIDAL_HEIGHT_OFFSET")
        mem_ds.SetMetadataItem("auxiliary_data", "horizontal_offset")
        mem_ds.SetMetadataItem("interpolation_method", "biquadratic")

        options = ["COMPRESS=DEFLATE", "PREDICTOR=3"]
        if mem_ds.RasterXSize > 256 or mem_ds.RasterYSize > 256:
            options += ["TILED=YES"]
        else:
            options += ["BLOCKYSIZE=" + str(mem_ds.RasterYSize)]
        assert gdal.GetDriverByName("GTiff").CreateCopy(tiff_filename + ".tmp", mem_ds,
                                                      options = options + ["APPEND_SUBDATASET=YES"]) is not None

    generate_optimized_file(tiff_filename + ".tmp", tiff_filename)
    gdal.Unlink(tiff_filename + ".tmp")

    out_ds = gdal.Open(tiff_filename)
    assert out_ds.GetRasterBand(1).ReadRaster() == lat_ds.ReadRaster()
    assert out_ds.GetRasterBand(2).ReadRaster() == lon_ds.ReadRaster()
    if ellipsoidal_same_resolution:
        assert out_ds.GetRasterBand(3).ReadRaster() == eht_ds.ReadRaster()
    if has_ellipsoidal_height_shift and not ellipsoidal_same_resolution:
        out_ds = gdal.Open("GTIFF_DIR:2:" + tiff_filename)
        assert out_ds.GetRasterBand(1).ReadRaster() == eht_ds.ReadRaster()

    readme_txt += f"### {area_of_use}: NADCON5: {source_crs_name} -> {target_crs_name}\n"
    readme_txt += "\n"
    readme_txt += "*Source*: [NADCON5 .b files coming from NOAA](%s)  \n" % (base_url + "/" + subdir)
    readme_txt += "*Format*: GeoTIFF converted with build_nadcon5.py script  \n"
    readme_txt += "*License*: Public Domain  \n"
    readme_txt += f"*Source CRS*: {source_crs_name} ({source_crs_code})  \n"
    readme_txt += f"*Target CRS*: {target_crs_name} ({target_crs_code})\n"
    readme_txt += "\n"
    if has_ellipsoidal_height_shift:
        readme_txt += "Includes ellipsoidal height offsets.\n\n"
    readme_txt += "* %s\n" % tiff_filename
    readme_txt += "\n"

open('README_nadcon5.txt', 'wt').write(readme_txt)
