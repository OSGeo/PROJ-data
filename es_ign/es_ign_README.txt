# es_ign_README.txt

The files in this section result from the conversion of datasets originating
from [IGN](https://www.ign.es/)

## Included grids

### Spanish (Spain - mainland and Balearic Islands) horizontal ED50 to ETRS89 grid: 

*Source*: [IGN Spain](https://www.fomento.gob.es/recursos_mfom/gridshift1.zip), actually retrieved from https://github.com/oscarfonts/geocalc/blob/master/src/main/resources/org/geotools/referencing/factory/gridshift/SPED2ETV2.gsb?raw=true  
*Format*: GeoTIFF converted from NTv2 (with Baleares grid put first to be used in priority for points falling into it)  
*License*: Derivated from Original IGN Data www.ign.es CC-BY 4.0. [Politica de datos](https://www.ign.es/web/ign/portal/politica-datos)  
*Source CRS*: EPSG:4230 (ED50)  
*Target CRS*: EPSG:4258 (ETRS89)  
*Used by*: [EPSG:15932 Transformation](https://www.epsg-registry.org/export.htm?gml=urn:ogc:def:coordinateOperation:EPSG::15932)

* es_ign_SPED2ETV2.tif

### Spanish (Spain - mainland and Balearic Islands) vertical grid: 

*Source*: [IGN Spain](ftp://ftp.geodesia.ign.es/geoide/ascii/)  
*Converter*: vertoffset_grid_to_gtiff.py  
*Format*: GeoTIFF convered from 'Arc/Info ASCII Grid'  
*License*: Derivated from Original IGN Data www.ign.es CC-BY 4.0. [Politica de datos](https://www.ign.es/web/ign/portal/politica-datos)  
*Horizontal CRS*: EPSG:4937 (ETRS89)  

Vertical transformation for Geoid model EGM08-REDNAP. Used to make the transitions 
from heights in vertical CRS (EPSG:5782) to heights above the ellipsoid in ETRS89 (EPSG:4937).

* es_ign_egm08-rednap.tif

### Spanish (Spain - Canary Islands) vertical grid: 

*Source*: [IGN Spain](ftp://ftp.geodesia.ign.es/geoide/ascii/)  
*Converter*: vertoffset_grid_to_gtiff.py  
*Format*: GeoTIFF convered from 'Arc/Info ASCII Grid'  
*License*: Derivated from Original IGN Data www.ign.es CC-BY 4.0. [Politica de datos](https://www.ign.es/web/ign/portal/politica-datos)  
*Horizontal CRS*: EPSG:4080 (REGCAN95)  

Vertical transformation for Geoid model EGM08-REDNAP_Canarias. Used to make the transitions 
from heights in vertical CRS (EPSG:9397 -Gran Canaria- and also the other Canary islands) 
to heights above the ellipsoid in REGCAN95 (EPSG:4080).

* es_ign_egm08-rednap-canarias.tif
