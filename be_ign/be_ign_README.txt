# be_ign_README.txt

The files in this section result from the conversion of datasets originating
from [IGN Belgium](http://www.ngi.be)

## Included grids

### Belgium: BD72 -> ETRS89

Grid transformation from Belgium Datum 72 to ETRS89 in Belgium.

*Source*: [IGN](http://www.ngi.be/Common/Lambert2008/NTv2.zip)
*Format*: GeoTIFF converted from NTv2
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)
*Credit*: (c)2014-2016 Grid created by Nicolas SIMON.

It provides an accuracy better than 5mm in 99.6% of validation points and a
worst case of 1.3 cm outside the border.
Recommended to transform from Belgian Lambert 72 (EPSG:31370) to Belgian Lambert 2008 (EPSG:3812)
Documentation in French: (http://www.ngi.be/FR/FR2-1-7.shtm)
Documentation in Dutch:  (http://www.ngi.be/NL/NL2-1-7.shtm)

* be_ign_bd72lb72_etrs89lb08.tif

### Belgium vertical grid:

*Source*: [IGN](https://www.ngi.be/website/wp-content/uploads/2020/07/hBG18_fr.zip)
*Format*: GeoTIFF converted from 'XYZ ASCII Grid'
*License*: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)
*Credit*: C. Slobbe, R. Klees, H.H. Farahani, L. Huisman, B. Alberts, P. Voet, F. De Doncker (2018). The Belgian hybrid quasi-geoid: hBG18. V. 1.0. GFZ Data Services. http://doi.org/10.5880/isg.2018.003  
*Horizontal CRS*: EPSG:4937 (ETRS89)

Vertical transformation for Geoid model hGB18. Used to make the transitions 
from heights in vertical CRS (EPSG:5710 - Ostend height) to heights above the ellipsoid in ETRS89 (EPSG:4937).

* be_ign_hBG18.tif
