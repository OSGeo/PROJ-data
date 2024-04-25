# How to contribute to PROJ-data

Consult [PROJ CONTRIBUTING.md](https://github.com/OSGeo/PROJ/blob/master/CONTRIBUTING.md)
for general principles.

This document focuses on how to specifically contribute a new grid to PROJ-data

Preliminary:
* The grid must be in the
  [Geodetic TIFF grids (GTG)](https://github.com/OSGeo/PROJ/blob/master/docs/source/specifications/geodetictiffgrids.rst) format.
  The [grid_tools](grid_tools) directory contains tools to convert grids in other format such as NTv2 (.gsb) or GTX to GTG)
* The grid must be freely licensed as mentioned in [README.DATA](README.DATA).
* We consider that you are familiar with the basic [GitHub workflow to submit a pull request](https://help.github.com/en/articles/creating-a-pull-request)

Grids are organized by producing agencies, with a short identifier.
The short identifier is built as:
{two_letter_country_code_of_agency_nationality}_{short_name_for_agency}
For example `fr_ign`, for IGN France.
If a new agency has to be created:
1. Create a new directory whose name is based on the above naming scheme
2. Go in that directory
3. Create a {agency_id}_README.txt file whose content is inspired from similar existing files
4. Create a .github subdirectory
5. Create a symbolic link from the file created at 3. as README.md: ln -s ../{agency_id}_README.txt .github/README.md
6. Edit CMakeLists.txt at the root of the repository to package the new directory
7. Edit agency.json at the root of the repository to add the new agency (optionally also in README.DATA)

The steps for adding a GeoTIFF grid to an existing subdirectory are:
1. Make sure the naming convention for the grid is {agency_id}_{some_name}.tif
2. Add it into the directory
3. Edit the {agency_id}_README.txt file. You should mention its
   source/provenance, its license, its format (GTiff), the source and
   target coordinate reference systems of the grid, its accuracy when known,
   and all other relevant information.
   For a vertical shift grid, mention the horizontal CRS (interpolation CRS)
   to use.
   Replicating an existing entry will be the easiest.
4. Add the grid name in `travis/expected_main.lst`, sorted alphabetically.
5. Mention copyright & license information in copyright_and_licenses.csv
   Use [SPDX license identifiers](https://spdx.org/licenses/) where possible.
   Indicate the version added (look at https://github.com/OSGeo/PROJ-data/milestones)
6. Add to git the new and modified files
7. git commit
8. Run the regenerate_index_html.py file (requires Python 3 and GDAL Python bindings)
9. git commit
10. git push and issue the pull request

Adding a grid in a package of grids is not enough to make it directly and transparently
usable by PROJ. If the source and target coordinate reference systems are known of
the PROJ database (typically they have a EPSG code), a transformation for them using
the grid must be referenced in the PROJ database. Generally, the EPSG database will
already have an entry for the grid, sometimes with a slightly different name.
The relevant file to look into is [grid_transformation.sql](https://github.com/OSGeo/PROJ/blob/master/data/sql/grid_transformation.sql). 
If the grid is not yet registered in the EPSG database, you are *strongly* encouraged to
engage with EPSG to register it. This will make its addition to PROJ and its later maintenance
much easier. https://epsg.org/dataset-change-requests.html explains the procedure
to follow to submit a change request to EPSG.

You may find an entry like the following one:
```
INSERT INTO "grid_transformation" VALUES(
    'EPSG','15958',              -- transformation code
    'RGF93 to NTF (2)',          -- transformation name
    'Emulation using NTv2 method of transformation NTF to RGF93 (1), code 9327. Note that grid file parameters are of opposite sign. May be taken as approximate transformation to ETRS89 or WGS 84 - see tfm codes 15959 and 15960.', -- remarks
    'EPSG','9615','NTv2',        -- transformation method  
    'EPSG','4171',               -- source CRS
    'EPSG','4275',               -- target CRS
    1.0,                         -- accuracy
    'EPSG','8656','Latitude and longitude difference file','rgf93_ntf.gsb', -- grid name
    NULL,NULL,NULL,NULL,
    NULL,NULL,                   -- interpolation CRS 
    'ESRI-Fra 1m emulation',0);
    
INSERT INTO "usage" VALUES('EPSG','11969',             -- usage code
                           'grid_transformation',
                           'EPSG','15958',             -- transformation code
                           'EPSG','3694',              -- extent code (reference an entry in the "extent" table) 
                           'EPSG','1041'               -- scope code (reference an entry in the "scope" table) 
);
```
This is a transformation from EPSG:4171 (RGF93) to EPSG:4275 (NTF) using the rgf93_ntf.gsb grid.

Or for a vertical transformation
```
INSERT INTO "grid_transformation" VALUES(
    'EPSG','7001','ETRS89 to NAP height (1)',
    'Alternative to vertical component of official 3D RDNAPTRANS(TM)2008. The naptrans2008 correction grid incorporates the NLGEO2004 geoid model plus a fixed offset.',
    'EPSG','9665','Geographic3D to GravityRelatedHeight (US .gtx)',
    'EPSG','4937',
    'EPSG','5709',
    0.01,
    'EPSG','8666','Geoid (height correction) model file','naptrans2008.gtx',
    NULL,NULL,NULL,NULL,
    'EPSG','4289',              -- interpolation CRS has been manually added
    'RDNAP-Nld 2008',0);
    
INSERT INTO "usage" VALUES(
    'EPSG','9882',
    'grid_transformation',
    'EPSG','7001',
    'EPSG','1275',
    'EPSG','1133');
```

If the EPSG dataset does not include an entry, a custom entry may be added in the [grid_transformation_custom.sql](https://github.com/OSGeo/PROJ/blob/master/data/sql/grid_transformation_custom.sql) file.

For this grid to be completely known of PROJ, we must add an entry in the database to describe the grid.

This is done in the [grid_alternatives.sql](https://github.com/OSGeo/PROJ/blob/master/data/sql/grid_alternatives.sql) file.

```
INSERT INTO grid_alternatives(original_grid_name,
                              proj_grid_name,
                              old_proj_grid_name,
                              proj_grid_format,
                              proj_method,
                              inverse_direction,
                              package_name,
                              url, direct_download, open_license, directory)

VALUES ('rgf93_ntf.gsb',      -- grid name as in the grid_transformation.sql file.
        'fr_ign_ntf_r93.tif', -- PROJ grid name
        NULL,                 -- should be NULL for new grids
        'GTiff',              -- format. Should be GTiff
        'hgridshift',         -- one of hgridshift (for horizontal shift grids), vgridshift (for vertical<-->vertical adjustmenents) or geoid_like (for transformations between vertical and ellipsoidal heights)
        1,                    -- 0 in most cases. Here, 1 because of the inverse direction of that particular case
        NULL,                 -- should be NULL
        'https://cdn.proj.org/fr_ign_ntf_r93.tif', -- should be 'https://cdn.proj.org/' + proj_grid_format
        1,                    -- should be 1
        1,                    -- should be 1
        NULL                  -- should be NULL
);
```

After rebuilding the PROJ database (`make`), you can check the output of `src/projinfo -s EPSG:XXXX -t EPSG:YYYY --spatial-test intersects` if the grid is properly recognized.

## How to remove a file

* Edit copyright_and_licenses.csv to indicate the version in which it is removed
  in the "version_removed" column
* Open files.geojson, move the corresponding entry to files_removed.geojson,
  and add a "version_removed" property to the entry (identical to the one added
  in the "version_removed" column of the .csv file)
* Remove the grid name in `travis/expected_main.lst`
