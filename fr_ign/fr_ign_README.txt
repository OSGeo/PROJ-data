# fr_ign_README.txt

The files in this section result from the conversion of datasets originating
from [IGN](http://www.ign.fr/)

## Included grids

### France: NTF -> RGF93 (using geographic offset correction)

Grid transformation from NTF to RGF93 in France.

*Source*: [IGN](http://www.ign.fr/)  
*Format*: GeoTIFF converted from NTv2  
*License*: [License Ouverte (in French)](https://www.etalab.gouv.fr/wp-content/uploads/2017/04/ETALAB-Licence-Ouverte-v2.0.pdf) / [Open License (English translation)](https://www.etalab.gouv.fr/wp-content/uploads/2014/05/Open_Licence.pdf)

* fr_ign_ntf_r93.tif

### France: NTF -> RGF93 (using Geocentric correction)

Grid transformation from NTF to RGF93 in France.

*Source*: [IGN](http://www.ign.fr/)  
*Format*: GeoTIFF converted from gr3df97a.txt  
*License*: [License Ouverte (in French)](https://www.etalab.gouv.fr/wp-content/uploads/2017/04/ETALAB-Licence-Ouverte-v2.0.pdf) / [Open License (English translation)](https://www.etalab.gouv.fr/wp-content/uploads/2014/05/Open_Licence.pdf)

* fr_ign_gr3df97a.tif

### Mayotte: RGM04 -> RGM23 (using Geocentric correction)

Grid transformation from RGM04 to RGM23 in Mayotte.

*Source*: [IGN](http://www.ign.fr/)  
*Format*: GeoTIFF converted from https://geodesie.ign.fr/contenu/fichiers/documentation/RGM04versRGM23.txt  
*License*: [License Ouverte (in French)](https://www.etalab.gouv.fr/wp-content/uploads/2017/04/ETALAB-Licence-Ouverte-v2.0.pdf) / [Open License (English translation)](https://www.etalab.gouv.fr/wp-content/uploads/2014/05/Open_Licence.pdf)

* fr_ign_RGM04versRGM23.tif

### French vertical grids

*Source*: [IGN France](https://geodesie.ign.fr/index.php?page=grilles)  
*Converter*: build_french_vgrids.sh  
*Format*: GeoTIFF convered from GTX  
*License*: [License Ouverte (in French)](https://www.etalab.gouv.fr/wp-content/uploads/2017/04/ETALAB-Licence-Ouverte-v2.0.pdf) / [Open License (English translation)](https://www.etalab.gouv.fr/wp-content/uploads/2014/05/Open_Licence.pdf)

Grids to convert from national vertical datum to ellipsoidal height.

Continental France an Corsica:
* fr_ign_RAF09.tif: Continental France, NGF-IGN 1969 to RGF93 (ETRS89) (2009 version)
* fr_ign_RAF18.tif: Continental France, NGF-IGN 1969 to RGF93 (ETRS89) (2018 version)
* fr_ign_RAF18b.tif: Continental France, NGF-IGN 1969 to RGF93 (ETRS89) (2018b version)
* fr_ign_RAF20.tif: Continental France, NGF-IGN 1969 to RGF93 (ETRS89) (2021 v2b version)
* fr_ign_RAC09.tif: Corsica, NGF-IGN 1978 to RGF93 (ETRS89)
* fr_ign_RAC23.tif: Corsica, NGF-IGN 1978 to RGF93-2b (ETRS89)

French Antilles to RGAF09 (Réseau Géodésique des Antilles Françaises 2009):
* fr_ign_RAGTBT2016.tif: Guadeloupe, IGN 1988 (GUADELOUPE) to RGAF09
* fr_ign_RALD2016.tif: La Desirade, IGN 2008 LD (GUADELOUPE / LA DESIRADE) to RGAF09
* fr_ign_RALS2016.tif: Les Saintes, IGN 1988 LS (GUADELOUPE / LES SAINTES) to RGAF09
* fr_ign_RAMART2016.tif: Martinique, IGN 1987 (MARTINIQUE) to RGAF09
* fr_ign_RAMG2016.tif: Marie Galante, IGN 1988 MG (GUADELOUPE / MARIE-GALANTE) to RGAF09
* fr_ign_gg10_sbv2.tif: Saint Barthelemy, IGN 1988 SB (GUADELOUPE / SAINT-BARTHELEMY) to RGAF09
* fr_ign_gg10_smv2.tif: Saint Martin, IGN 1988 SM (GUADELOUPE / SAINT-MARTIN) to RGAF09

French Antilles to WGS 84 (RRAF: Réseau de Référence des Antilles Françaises):
* fr_ign_ggg00v2.tif: Guadeloupe, IGN 1988 (GUADELOUPE) to WGS 84 (RRAF)
* fr_ign_RALDW842016.tif: La Desirade, IGN 2008 LD (GUADELOUPE / LA DESIRADE) to WGS 84 (RRAF)
* fr_ign_ggg00_lsv2.tif: Les Saintes, IGN 1988 LS (GUADELOUPE / LES SAINTES) to WGS 84 (RRAF)
* fr_ign_ggg00_mgv2.tif: Marie Galante, IGN 1988 MG (GUADELOUPE / MARIE-GALANTE) to WGS 84 (RRAF)
* fr_ign_ggm00v2.tif: Martinique, IGN 1987 (MARTINIQUE) to WGS 84 (RRAF)
* fr_ign_ggg00_sbv2.tif: Saint Barthelemy, IGN 1988 SB (GUADELOUPE / SAINT-BARTHELEMY) to WGS 84 (RRAF)
* fr_ign_ggg00_smv2.tif: Saint Martin, IGN 1988 SM (GUADELOUPE / SAINT-MARTIN) to WGS 84 (RRAF)

Other:
* fr_ign_ggguy15.tif: Guyane, NIVELLEMENT GENERAL DE GUYANE (NGG) 1977 to RGFG95 (RESEAU GEODESIQUE FRANCAIS DE GUYANE 1995)
* fr_ign_ggker08v2.tif: Iles Kerguelen, IGN 1962 (KERGUELEN) to RGTAAF07 (RESEAU GEODESIQUE DES TAAF 2007)
* fr_ign_ggm04v1.tif: Mayotte GGM04, SHOM 1953 (MAYOTTE) to RGM04 (RESEAU GEODESIQUE DE MAYOTTE 2004)
* fr_ign_ggspm06v1.tif: Saint-Pierre et Miquelon (GGSPM06), DANGER 1950 (SAINT-PIERRE-ET-MIQUELON) to RGSPM06 (RESEAU GEODESIQUE DE SAINT-PIERRE-ET-MIQUELON 2006)
* fr_ign_RAR07_bl.tif: La Reunion, IGN 1989 (REUNION) to RGR92 (RESEAU GEODESIQUE DE LA REUNION 1992)
* fr_ign_RASPM2018.tif: Saint-Pierre et Miquelon (RASPM2018), DANGER 1950 (SAINT-PIERRE-ET-MIQUELON) to RGSPM06 (RESEAU GEODESIQUE DE SAINT-PIERRE-ET-MIQUELON 2006)
* fr_ign_CGVD2013RGSPM06.tif: Saint-Pierre et Miquelon (CGVD2013RGSPM06), CGVD2013 to RGSPM06

French Polynesia to RGPF (Réseau Géodésique de Polynésie Française)
* fr_ign_ggpf02-Bora.tif: Bora bora, BORA_SAU 2001 to RGPF
* fr_ign_ggpf02-Huahine.tif: Huahine, HUAHINE_SAU 2001 to RGPF
* fr_ign_ggpf02-Maiao.tif: Maiao, MAIAO 2001 to RGPF
* fr_ign_ggpf02-Maupiti.tif: Maupiti, MAUPITI_SAU 2001 to RGPF
* fr_ign_ggpf02-Raiatea.tif: Raietea, RAIATEA_SAU 2001 to RGPF
* fr_ign_ggpf02-Tahaa.tif: Tahaa, TAHAA_SAU 2001 to RGPF
* fr_ign_ggpf02-Tupai.tif: Tupai, TUPAI 2001 to RGPF
* fr_ign_ggpf05-HivaOa.tif: Hiva Oa, HIVA OA to RGPF
* fr_ign_ggpf05-Nuku.tif: Nuku Hiva, NUKU HIVA ALTI to RGPF
* fr_ign_ggpf08-Fakarava.tif: Fakarava, IGN 1966 (TAHITI) TO RGPF
* fr_ign_ggpf08-Gambier.tif: Gambier, GAMBIER to RGPF
* fr_ign_ggpf08-Hao.tif: Hao, HAO to RGPF
* fr_ign_ggpf08-Mataiva.tif: Mataiva, MATAIVA to RGPF
* fr_ign_ggpf08-Raivavae.tif: Raivavae, Raivavae to RGPF
* fr_ign_ggpf08-Reao.tif: Reao, Reao to RGPF
* fr_ign_ggpf08-Rurutu.tif: Rurutu, Ruruto to RGPF
* fr_ign_ggpf08-Tikehau.tif: Tikehau, Tikehau to RGPF
* fr_ign_ggpf08-Tubuai.tif: Tubuai, Tubuai to RGPF
* fr_ign_ggpf10-Moorea.tif: Moorea, MOOREA 1981 (MOOREA_SAU 2001) to RGPF
* fr_ign_ggpf10-Tahiti.tif: Tahiti, IGN 1966 (TAHITI) to RGPF
