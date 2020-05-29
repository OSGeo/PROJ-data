# nz_linz_README.txt

The files in this section result from the conversion of datasets originating
from [Land Information New Zealand]

The New Zealand grids are
required for coordinate transformations between New Zealand geographic  
and vertical coordinate systems.

The New Zealand grids are sourced from [Land Information New Zealand]
and are also available from LINZ as a separate resource [proj-datumgrid-nz].

The New Zealand grids are published under the  
[Creative Commons Attribution 4.0 International licence].

## Included grids

### NZGD2000 to ITRF96 transformation

*Filename*: nz_linz_nzgd2000-(version).json
*Reference*: https://www.linz.govt.nz/data/geodetic-system/datums-projections-and-heights/geodetic-datums/new-zealand-geodetic-datum-2000-nzgd2000/nzgd2000-deformation-model

This is a set of deformation model files for each of the versions of the NZGD2000 datum.
Each version is identified by a nominal publication date in yyyymmdd date format (for example nz_linz_nzgd2000-20180701.json. 
The JSON files define the deformation model using a set of GeoTiff files, each of which is names with the prefix nz_linz_nzgd2000.
Note that the transformation from ITRF96 to other realisations such as ITRF2008 should use the NZ specific transformations, for example EPSG:9082 to transform
between between ITRF2008 and ITRF96.  These are documented in 
https://www.linz.govt.nz/file/itrftonzgd2000pdf.

Example of conversion from NZGD2000 to ITRF96 at epoch 2016.5

  echo '173 -41 0 2016.5' | \
     cct -t 2016.5 -d 8 +proj=defmodel +model=nz_linz_nzgd2000-20180701.json 

### NZGD1949 to NZGD2000 transformation  

*Filename*: nz_linz_nzgd2kgrid0005.tif  
*Reference*: https://www.linz.govt.nz/data/geodetic-system/coordinate-conversion/geodetic-datum-conversions/nzgd1949-nzgd2000

Distortion grid to convert New Zealand Geodetic Datum 1949 longitude and latitude  
to New Zealand Geodetic Datum 2000 longitude and latitude.

#### Usage

Conversion from NZGD1949 to NZGD2000 using proj strings
  
  echo '173 -41 0' | cs2cs -v -f %.8f +proj=longlat +ellps=intl +datum=nzgd49 +nadgrids=nzgd2kgrid0005.tif +to +proj=longlat +ellps=GRS80 +towgs84=0,0,0  

Conversion from NZGD1949 to NZGD2000 using EPSG codes.  Note that this uses  
EPSG specified coordinate order for coordinate systems (latitude/longitude in this case).

  echo '-41 173 0' | cs2cs -f %.8f EPSG:4272 EPSG:4167

### Quasigeoid grids

Two geoid grid files are included:

*Geoid*: New Zealand Quasigeoid 2009  
*Filename*: nz_linz_nzgeoid2009.tif  
*Reference*: https://www.linz.govt.nz/data/geodetic-system/datums-projections-and-heights/vertical-datums/new-zealand-quasigeoid-2009-nzgeoid2009

*Geoid*: New Zealand Quasigeoid 2016  
*Filename*: nz_linz_nzgeoid2016.tif  
*Reference*: https://www.linz.govt.nz/data/geodetic-system/datums-projections-and-heights/vertical-datums/new-zealand-quasigeoid-2016-nzgeoid2016

These grids define the height of the New Zealand Quasigeoid relative to the ellipsoidal  
height surface on which NZGD2000 is based (nominally a GRS80 ellipsoid aligned ITRF96  
at epoch 2000.0). See https://www.linz.govt.nz/nzgd2000 for more information on the  
NZGD2000 datum.  
The current NZGD2000 deformation model has this as the zero elevation of NZGD2000  
coordinates at the current epoch.  

These quasigeoids are the reference surfaces the New Zealand Vertical Datum 2009  
(NZVD2009) and New Zealand Vertical Datum 2016 (NZVD2016).  

#### Usage

To convert a NZGD2000 ellipsoidal height 100.0 to a NZVD2016 orthometric height at 173W 41S

   echo '173 -41 100.0' | cs2cs -v -f %.8f +proj=longlat +ellps=GRS80 +to +proj=longlat +ellps=GRS80 +geoidgrids=nzgeoid2016.tif

To convert a NZVD2016 orthometric height to a NZGD2000 ellipsoidal height

   echo '173 -41 100.0' | cs2cs -v -f %.8f +proj=longlat +ellps=GRS80 +geoidgrids=nzgeoid2016.tif +to +proj=longlat +ellps=GRS80

To convert a NZGD2000 ellipsoidal height 100.0 to a NZVD2016 height at 173W 41S using EPSG codes (requires proj > 6.2)

   echo '-41 173 100.0' | cs2cs -f %.8f EPSG:4167 EPSG:4167+7839


### Local vertical datum transformation grids

Thirteen grids are provided to transform heights between NZVD2016 and  
the [New Zealand local vertical datums].  

These grids represent the systematic errors in the local vertical datums.  
The local vertical datums are each based on levelling from a tide gauge.  
They include systematic errors from the levelling as well as a potential of the local  
tidal signal at the port from the global mean gravitational equipotential surface.  The  
NZVD2016 datum is based on gravity measurements from a national airborne gravity  
program and is much less prone to regional systematic errors.  The transformation grids  
are derived from comparing the benchmark heights at which both levelling data and GNSS  
(Global Navigation Satellite system) data are available.  

The height determined from the grid model is added to an NZVD2016 height to obtain
the corresponding local vertical datum shift.

The following grids are available:

*Local vertical datum*: Auckland 1946  
*Filename*: nz_linz_auckht1946-nzvd2016.tif

*Local vertical datum*: Bluff 1955  
*Filename*: nz_linz_blufht1955-nzvd2016.tif

*Local vertical datum*: Dunedin 1958  
*Filename*: nz_linz_duneht1958-nzvd2016.tif

*Local vertical datum*: Dunedin-Bluff 1960  
*Filename*: nz_linz_dublht1960-nzvd2016.tif

*Local vertical datum*: Gisborne 1926  
*Filename*: nz_linz_gisbht1926-nzvd2016.tif

*Local vertical datum*: Lyttelton 1937  
*Filename*: nz_linz_lyttht1937-nzvd2016.tif

*Local vertical datum*: Moturiki 1953  
*Filename*: nz_linz_motuht1953-nzvd2016.tif

*Local vertical datum*: Napier 1962  
*Filename*: nz_linz_napiht1962-nzvd2016.tif

*Local vertical datum*: Nelson 1955  
*Filename*: nz_linz_nelsht1955-nzvd2016.tif

*Local vertical datum*: One Tree Point 1964  
*Filename*: nz_linz_ontpht1964-nzvd2016.tif

*Local vertical datum*: Stewart Island 1977  
*Filename*: nz_linz_stisht1977-nzvd2016.tif

*Local vertical datum*: Taranaki 1970  
*Filename*: nz_linz_taraht1970-nzvd2016.tif

*Local vertical datum*: Wellington 1953  
*Filename*: nz_linz_wellht1953-nzvd2016.tif

#### Usage

To convert from a local vertical datum height to a NZVD2016 height.

   echo '175 -37 0' | cct +proj=vgridshift +inv +grids=auckht1946-nzvd2016.tif +multiplier=1

To convert from a NZVD2016 height to a local vertical datum height.

   echo '175 -37 0' | cct +proj=vgridshift +grids=auckht1946-nzvd2016.tif +multiplier=1

[Land Information New Zealand]: https://www.linz.govt.nz
[proj-datumgrid-nz]: https://www.geodesy.linz.govt.nz/download/proj-datumgrid-nz
[New Zealand local vertical datums]: https://www.linz.govt.nz/data/geodetic-system/datums-projections-and-heights/vertical-datums/vertical-datum-relationship-grids
[Creative Commons Attribution 4.0 International licence]: https://data.linz.govt.nz/license/attribution-4-0-international/
