# nl_nsgi_README.txt

The files in this section originate from [NSGI](https://www.nsgi.nl/) with corrected metadata.


## Included grids

### European Netherlands: RD and NAP -> ETRS89

*Source*: [NSGI](https://www.nsgi.nl/coordinatenstelsels-en-transformaties/coordinatentransformaties/rdnap-etrs89-rdnaptrans)  
*Format*: GeoTIFF converted from NTv2 & GTX  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)  

#### Variant 1:

* nl_nsgi_rdcorr2018.tif
* nl_nsgi_nlgeo2018.tif

Recommended variant, applies the datum transformation as a separate step using a 3D similarity transformation.

#### Variant 2:

N.A. only relevant for PROJ 4

#### Hybrid variant:

* nl_nsgi_rdtrans2018.tif
* nl_nsgi_nlgeo2018.tif

Includes the datum transformation in the correction grid.

Refer to the [RDNAPTRANS™2018 documentation](https://www.nsgi.nl/rdnaptrans) for details.


### European Netherlands: LAT -> ETRS89

*Source*: [NSGI](https://www.nsgi.nl/coordinatenstelsels-en-transformaties/coordinatentransformaties/nllat-nap-etrs89)  
*Format*: GeoTIFF converted from GTX  
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)  

* nl_nsgi_nllat2018.tif

Refer to the [NLLAT2018 documentation](https://www.defensie.nl/downloads/applicaties/2020/06/12/nllat2018) for details.


### Caribbean Netherlands: Bonaire height system KADpeil -> ITRS

*Source*: [NSGI](https://www.nsgi.nl/coordinatenstelsels-en-transformaties/coordinatentransformaties/dpnet-itrs-bestrans)  
*Format*: GeoTIFF converted from GTX  
*License*: Derived from work by NGA. Public Domain. 

* nl_nsgi_bongeo2004.tif

Refer to the [BESTRANS2020 documentation](https://www.nsgi.nl/coordinatenstelsels-en-transformaties/coordinatentransformaties/dpnet-itrs-bestrans) for details.
