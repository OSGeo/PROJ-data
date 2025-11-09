#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
#
# Project:  PROJ
# Purpose:  Convert a TIN JSON to a TIN GeoPackage
# Author:   Even Rouault <even.rouault at spatialys.com>
#
###############################################################################
# Copyright (c) 2025, Even Rouault <even.rouault at spatialys.com>
#
# SPDX-License-Identifier: MIT
###############################################################################

import argparse
import json
import struct

from osgeo import gdal, ogr, osr


def get_args():
    parser = argparse.ArgumentParser(
        description="Convert a TIN JSON to a TIN GeoPackage."
    )
    parser.add_argument("source", help="Source JSON file")
    parser.add_argument("dest", help="Destination GeoPackage file")
    return parser.parse_args()


def as_i32le_hex(v):
    return "".join(["%02X" % b for b in struct.pack("<i", v)])


def convert_json_to_gpkg(source, dest):

    j = json.loads(open(source, "rb").read())

    if "file_type" not in j:
        raise Exception(f"'file_type' missing in {source}")
    file_type = j["file_type"]
    if file_type != "triangulation_file":
        raise Exception(f"file_type={file_type} not handled")

    if "vertices" not in j or not isinstance(j["vertices"], list):
        raise Exception(f"'vertices' array missing in {source}")
    vertices = j["vertices"]

    if "vertices_columns" not in j or not isinstance(j["vertices_columns"], list):
        raise Exception(f"'vertices_columns' array missing in {source}")
    vertices_columns = j["vertices_columns"]
    idx_source_x = vertices_columns.index("source_x")
    idx_source_y = vertices_columns.index("source_y")

    if "triangles" not in j or not isinstance(j["triangles"], list):
        raise Exception(f"'triangles' array missing in {source}")
    triangles = j["triangles"]

    if "triangles_columns" not in j or not isinstance(j["triangles_columns"], list):
        raise Exception(f"'triangles_columns' array missing in {source}")
    triangles_columns = j["triangles_columns"]
    idx_vertex1 = triangles_columns.index("idx_vertex1")
    idx_vertex2 = triangles_columns.index("idx_vertex2")
    idx_vertex3 = triangles_columns.index("idx_vertex3")

    with gdal.config_options(
        {
            "OGR_SQLITE_PRAGMA": "page_size=1024",
            "CREATE_TRIGGERS": "NO",
            "CREATE_RASTER_TABLES": "NO",
        }
    ):
        ds = gdal.GetDriverByName("GPKG").CreateVector(dest)
    ds.StartTransaction()

    srs = None
    if "input_crs" in j:
        srs = osr.SpatialReference()
        srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
        srs.SetFromUserInput(j["input_crs"])

    metadata = {}
    for key, value in j.items():
        if key not in (
            "vertices_columns",
            "triangles_columns",
            "vertices",
            "triangles",
        ):
            metadata[key] = value

    if "target_x" in vertices_columns and "target_y" in vertices_columns:
        idx_target_x = vertices_columns.index("target_x")
        idx_target_y = vertices_columns.index("target_y")

        shift_x = [vertex[idx_target_x] - vertex[idx_source_x] for vertex in vertices]
        shift_y = [vertex[idx_target_y] - vertex[idx_source_y] for vertex in vertices]
        metadata["min_shift_x"] = min(shift_x)
        metadata["max_shift_x"] = max(shift_x)
        metadata["min_shift_y"] = min(shift_y)
        metadata["max_shift_y"] = max(shift_y)

    metadata["num_vertices"] = len(vertices)

    ds.ExecuteSQL(
        """CREATE TABLE gpkg_metadata (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  md_scope TEXT NOT NULL DEFAULT 'dataset',
  md_standard_uri TEXT NOT NULL,
  mime_type TEXT NOT NULL DEFAULT 'text/xml',
  metadata TEXT NOT NULL DEFAULT ''
)"""
    )
    ds.ExecuteSQL(
        """CREATE TABLE gpkg_metadata_reference (
  reference_scope TEXT NOT NULL,
  table_name TEXT,
  column_name TEXT,
  row_id_value INTEGER,
  timestamp DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
  md_file_id INTEGER NOT NULL,
  md_parent_id INTEGER,
  CONSTRAINT crmr_mfi_fk FOREIGN KEY (md_file_id) REFERENCES gpkg_metadata(id),
  CONSTRAINT crmr_mpi_fk FOREIGN KEY (md_parent_id) REFERENCES gpkg_metadata(id)
)"""
    )

    serialized_json = json.dumps(metadata).replace("'", "''")
    ds.ExecuteSQL(
        f"INSERT INTO gpkg_metadata (id, md_scope, md_standard_uri, mime_type, metadata) VALUES (1, 'dataset', 'https://proj.org', 'application/json', '{serialized_json}')"
    )
    ds.ExecuteSQL(
        "INSERT INTO gpkg_metadata_reference (reference_scope, table_name, column_name, row_id_value, md_file_id, md_parent_id) VALUES ('geopackage', NULL, NULL, NULL, 1, NULL)"
    )

    ds.ExecuteSQL("CREATE TABLE gpkg_extensions (table_name TEXT,column_name TEXT,extension_name TEXT NOT NULL,definition TEXT NOT NULL,scope TEXT NOT NULL,CONSTRAINT ge_tce UNIQUE (table_name, column_name, extension_name))")
    ds.ExecuteSQL("INSERT INTO gpkg_extensions VALUES('gpkg_metadata', NULL, 'gpkg_metadata', 'http://www.geopackage.org/spec120/#extension_metadata', 'read-write')")
    ds.ExecuteSQL("INSERT INTO gpkg_extensions VALUES('gpkg_metadata_reference', NULL, 'gpkg_metadata', 'http://www.geopackage.org/spec120/#extension_metadata', 'read-write')")

    lyr = ds.CreateLayer(
        "vertices",
        geom_type=ogr.wkbPoint,
        srs=srs,
        options=["SPATIAL_INDEX=NO", "GEOMETRY_NULLABLE=NO"],
    )

    ogr_to_vertices_column_idx = []
    for idx, col in enumerate(vertices_columns):
        if idx in (idx_source_x, idx_source_y):
            continue
        is_reserved_col = col in (
            "target_x",
            "target_y",
            "source_z",
            "target_z",
            "offset_z",
        )
        if isinstance(vertices[0][idx], float) or is_reserved_col:
            ogr_type = ogr.OFTReal
        elif isinstance(vertices[0][idx], int):
            ogr_type = ogr.OFTInteger
        else:
            ogr_type = ogr.OFTString
        fld_defn = ogr.FieldDefn(col, ogr_type)
        if is_reserved_col:
            fld_defn.SetNullable(False)
        lyr.CreateField(fld_defn)
        ogr_to_vertices_column_idx.append(idx)
    for fid, v in enumerate(vertices):
        f = ogr.Feature(lyr.GetLayerDefn())
        for ogr_idx, idx in enumerate(ogr_to_vertices_column_idx):
            f.SetField(ogr_idx, v[idx])
        p = ogr.Geometry(ogr.wkbPoint)
        p.SetPoint_2D(0, v[idx_source_x], v[idx_source_y])
        f.SetGeometryDirectly(p)
        f.SetFID(fid)
        lyr.CreateFeature(f)

    lyr = ds.CreateLayer("triangles_def", geom_type=ogr.wkbNone)
    other_fields = ""
    for idx, col in enumerate(triangles_columns):
        if isinstance(triangles[0][idx], float):
            ogr_type = ogr.OFTReal
        elif isinstance(triangles[0][idx], int):
            ogr_type = ogr.OFTInteger
        else:
            ogr_type = ogr.OFTString
        fld_defn = ogr.FieldDefn(col, ogr_type)
        if col in ("idx_vertex1", "idx_vertex2", "idx_vertex3"):
            fld_defn.SetNullable(False)
        lyr.CreateField(fld_defn)
        other_fields += ", "
        other_fields += col
    for fid, triangle in enumerate(triangles):
        f = ogr.Feature(lyr.GetLayerDefn())
        for idx in range(len(triangles_columns)):
            f.SetField(idx, triangle[idx])
        f.SetFID(fid)
        lyr.CreateFeature(f)

    with ds.ExecuteSQL(
        "SELECT srs_id FROM gpkg_contents WHERE table_name = 'vertices'"
    ) as sql_lyr:
        f = sql_lyr.GetNextFeature()
        srs_id = f["srs_id"]

    min_x = min([v[idx_source_x] for v in vertices])
    max_x = max([v[idx_source_x] for v in vertices])
    min_y = min([v[idx_source_y] for v in vertices])
    max_y = max([v[idx_source_y] for v in vertices])

    # We use a trick to generate GPKG polygon geometries from GPKG point geometries
    # of the vertices.
    srs_id_i32le = as_i32le_hex(srs_id)
    wkb_polygon_i32le = as_i32le_hex(3)
    number_rings_i32le = as_i32le_hex(1)
    number_vertices_i32le = as_i32le_hex(4)
    triangle_gpkg_prefix = f"47500001{srs_id_i32le}01{wkb_polygon_i32le}{number_rings_i32le}{number_vertices_i32le}"
    # 14 = GPKG_header_size_without_envelope (8) + WKB point header (5) + base_one_index (1)
    ds.ExecuteSQL(
        f"CREATE VIEW triangles AS SELECT triangles_def.fid AS OGC_FID{other_fields}, CAST(X'{triangle_gpkg_prefix}' || substr(v1.geom, 14) || substr(v2.geom, 14) || substr(v3.geom, 14) || substr(v1.geom, 14) AS BLOB) AS geom FROM triangles_def LEFT JOIN vertices v1 ON idx_vertex1 = v1.fid LEFT JOIN vertices v2 ON idx_vertex2 = v2.fid LEFT JOIN vertices v3 ON idx_vertex3 = v3.fid"
    )
    ds.ExecuteSQL(
        f"INSERT INTO gpkg_contents (table_name, identifier, data_type, srs_id, min_x, min_y, max_x, max_y) VALUES ('triangles', 'triangles', 'features', {srs_id}, {min_x}, {min_y}, {max_x}, {max_y})"
    )
    ds.ExecuteSQL(
        f"INSERT INTO gpkg_geometry_columns (table_name, column_name, geometry_type_name, srs_id, z, m) values ('triangles', 'geom', 'POLYGON', {srs_id}, 0, 0)"
    )

    ds.ExecuteSQL(
        "CREATE VIRTUAL TABLE rtree_triangles_geom USING rtree(id, minx, maxx, miny, maxy)"
    )
    for fid, triangle in enumerate(triangles):
        v1 = vertices[triangle[idx_vertex1]]
        v2 = vertices[triangle[idx_vertex2]]
        v3 = vertices[triangle[idx_vertex3]]
        tab_x = [v1[idx_source_x], v2[idx_source_x], v3[idx_source_x]]
        tab_y = [v1[idx_source_y], v2[idx_source_y], v3[idx_source_y]]
        minx = min(tab_x)
        miny = min(tab_y)
        maxx = max(tab_x)
        maxy = max(tab_y)
        ds.ExecuteSQL(
            f"INSERT INTO rtree_triangles_geom VALUES ({fid}, {minx}, {maxx}, {miny}, {maxy})"
        )

    ds.CommitTransaction()
    ds.ExecuteSQL("DELETE FROM sqlite_sequence")
    ds.ExecuteSQL("DROP TRIGGER trigger_insert_feature_count_vertices")
    ds.ExecuteSQL("DROP TRIGGER trigger_delete_feature_count_vertices")
    ds.ExecuteSQL("DROP TRIGGER trigger_insert_feature_count_triangles_def")
    ds.ExecuteSQL("DROP TRIGGER trigger_delete_feature_count_triangles_def")
    ds.ExecuteSQL("DROP TABLE gpkg_ogr_contents")
    ds.ExecuteSQL("VACUUM")
    ds.Close()

    # Check that the triangle coverage is OK (no overlaps)
    if gdal.VersionInfo(None) >= "3120000":
        with gdal.alg.vector.check_coverage(
            input=dest, output="", output_format="MEM", input_layer="triangles"
        ) as alg:
            out_ds = alg.Output()
            out_lyr = out_ds.GetLayer(0)
            if out_lyr.GetFeatureCount():
                print("Coverage of triangles has issues. Invalid edges:")
                for f in out_lyr:
                    f.DumpReadable()


if __name__ == "__main__":

    gdal.UseExceptions()
    args = get_args()
    convert_json_to_gpkg(args.source, args.dest)
