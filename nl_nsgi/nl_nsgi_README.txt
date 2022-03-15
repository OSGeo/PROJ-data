# nl_nsgi_README.txt

The files in this section originate from [NSGI](https://www.nsgi.nl/) with corrected metadata.


## Included grids

### Netherlands: RD and NAP -> ETRS89

*Source*: [NSGI](https://www.nsgi.nl/rdnaptrans)  
*Format*: GeoTIFF converted from NTv2 & GTX  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)  

Variant 1:

* nl_nsgi_rdcorr2018.tif
* nl_nsgi_nlgeo2018.tif

Recommended variant, applies the datum transformation as a separate step using
a 3D similarity transformation.

Variant 2:

* nl_nsgi_rdtrans2018.tif

Includes the datum transformation in the correction grid.

Refer to the [RDNAPTRANS™2018 documentation](https://www.nsgi.nl/rdnaptrans) for details.
