#!/bin/bash

# Ensure an input file is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <path_to_source_file>"
    exit 1
fi

# Get the absolute path of the input file
SOURCE_FILE="$1"

# Ensure the input file exists
if [ ! -f "$SOURCE_FILE" ]; then
    echo "Error: File '$SOURCE_FILE' not found."
    exit 1
fi

# Define a temporary file for the corrected grid
TEMP_FILE="temp_grid.dat"

# Swap latitude and longitude using awk and create a temporary file
awk '{print $2, $1, $3}' "$SOURCE_FILE" | sort -s -n -k1,1 -k2,2r > "$TEMP_FILE"

# Convert the corrected grid to a GeoTIFF
TEMP_FILE2="temp_grid.tif"
gdal_translate -of GTiff -a_nodata 9999 "$TEMP_FILE" "$TEMP_FILE2"

# Run the vertoffset grid conversion
OUTPUT_TIF="lv_lgia_lv14.tif"
python3 ../grid_tools/vertoffset_grid_to_gtiff.py \
  --description "LKS92 (EPSG:4949) to Latvia 2000 height (EPSG:7700). Converted from $SOURCE_FILE" \
  --type "GEOGRAPHIC_TO_VERTICAL" \
  --copyright "Derived from work by Latvian Geospatial Information Agency. CC-BY 4.0" \
  --area-of-use "Latvia - onshore mainland" \
  --parameter-name "geoid_undulation" \
  --source-crs "EPSG:4949" \
  --target-crs "EPSG:7700" \
  "$TEMP_FILE2" "$OUTPUT_TIF"

python3 ../grid_tools/check_gtiff_grid.py "$OUTPUT_TIF"

# Cleanup temporary files
rm -f "$TEMP_FILE"
rm -f "$TEMP_FILE2"

echo "Processing complete. Output saved to $OUTPUT_TIF"
