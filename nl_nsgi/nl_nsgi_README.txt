# nl_nsgi_README.txt

The files in this section result from the conversion of datasets originating
from [NSGI](https://www.nsgi.nl/)

## Included grids

### Netherlands: RD and NAP -> ETRS89

*Source*: [NSGI](https://www.nsgi.nl/geodetische-infrastructuur/producten/coordinatentransformatie)  
*Format*: GeoTIFF converted from NTv2 & GTX  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)  

Variant 1:

* nl_nsgi_rdcorr2018.tif
* nl_nsgi_nlgeo2018.tif

Recommended variant, applies the datum transformation as a separate step using
a 3D similarity transformation.

Variant 2:

* nl_nsgi_rdtrans2018.tif
* nl_nsgi_naptrans2018.tif

Includes the datum transformation in the correction grid and a different
quasi-geoid grid for the height transformation.

Refer to the
[RDNAPTRANS™2018 documentation](https://salsa.debian.org/debian-gis-team/proj-rdnap/raw/upstream/2008+2018/RDNAPTRANS2018.pdf)
for details.
