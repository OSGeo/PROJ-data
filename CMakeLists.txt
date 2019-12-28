# CMake build system for proj-datumgrid-geotiff releases.

cmake_minimum_required(VERSION 2.6)

project(PROJ_DATUMGRID_GEOTIFF)
set(PROJ_DATUMGRID_GEOTIFF_VERSION_MAJOR 1)
set(PROJ_DATUMGRID_GEOTIFF_VERSION_MINOR 0)

set(CPACK_SOURCE_GENERATOR "TGZ;ZIP")
set(CPACK_INCLUDE_TOPLEVEL_DIRECTORY 0)
set(CPACK_SOURCE_PACKAGE_FILE_NAME "proj-datumgrid-geotiff-${PROJ_DATUMGRID_GEOTIFF_VERSION_MAJOR}.${PROJ_DATUMGRID_GEOTIFF_VERSION_MINOR}")
set(CPACK_SOURCE_IGNORE_FILES "/travis/;/.github/;/.git/;.swp$;.*~;.py$;.sh$;/scripts/;.csv$;${CPACK_SOURCE_IGNORE_FILES}")
set(CPACK_INSTALL_COMMANDS
    "${CMAKE_COMMAND} -E make_directory ${CMAKE_BINARY_DIR}/tmp"
    "${CMAKE_COMMAND} -E copy ${CMAKE_SOURCE_DIR}/README.DATUMGRID ${CMAKE_BINARY_DIR}/tmp"
)
set(CPACK_SOURCE_INSTALLED_DIRECTORIES
    "${CMAKE_BINARY_DIR}/tmp/" "."
    "${CMAKE_CURRENT_SOURCE_DIR}/at_bev/" "."
    "${CMAKE_CURRENT_SOURCE_DIR}/au_ga/" "."
    "${CMAKE_CURRENT_SOURCE_DIR}/au_icsm/" "."
    "${CMAKE_CURRENT_SOURCE_DIR}/be_ign/" "."
    "${CMAKE_CURRENT_SOURCE_DIR}/ca_nrc/" "."
    "${CMAKE_CURRENT_SOURCE_DIR}/ca_que_mern/" "."
    "${CMAKE_CURRENT_SOURCE_DIR}/ch_swisstopo/" "."
    "${CMAKE_CURRENT_SOURCE_DIR}/de_bkg/" "."
    "${CMAKE_CURRENT_SOURCE_DIR}/de_geosn/" "."
    "${CMAKE_CURRENT_SOURCE_DIR}/de_lgl_bw/" "."
    "${CMAKE_CURRENT_SOURCE_DIR}/de_lgvl_saarland/" "."
    "${CMAKE_CURRENT_SOURCE_DIR}/dk_sdfe/" "."
    "${CMAKE_CURRENT_SOURCE_DIR}/es_cat_icgc/" "."
    "${CMAKE_CURRENT_SOURCE_DIR}/fr_ign/" "."
    "${CMAKE_CURRENT_SOURCE_DIR}/is_lmi/" "."
    "${CMAKE_CURRENT_SOURCE_DIR}/nz_linz/" "."
    "${CMAKE_CURRENT_SOURCE_DIR}/pt_dgt/" "."
    "${CMAKE_CURRENT_SOURCE_DIR}/se_lantmateriet/" "."
    "${CMAKE_CURRENT_SOURCE_DIR}/uk_os/" "."
    "${CMAKE_CURRENT_SOURCE_DIR}/us_nga/" "."
    "${CMAKE_CURRENT_SOURCE_DIR}/us_noaa/" "."
)

include(CPack)

add_custom_target(dist COMMAND ${CMAKE_MAKE_PROGRAM} package_source)
