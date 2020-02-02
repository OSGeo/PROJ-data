#!/bin/sh

TARGET=s3://cdn.proj.org/

for i in `ls -d *_*/`; do
    if test "$i" != "grid_tools/"; then
        echo "Synchronizing $i ..."
        aws s3 sync $i "$TARGET" --exclude ".github/*" --profile projcdn
    fi
done
aws s3 cp geotiff.bundle.min.js "$TARGET" --profile projcdn
aws s3 cp ol.js "$TARGET" --profile projcdn
aws s3 cp ol.css "$TARGET" --profile projcdn
aws s3 cp index.html "$TARGET" --profile projcdn --content-type "text/html"
aws s3 cp files.geojson "$TARGET" --profile projcdn --content-type "application/geo+json"
aws s3 cp README.DATA "$TARGET" --profile projcdn --content-type "text/plain"
