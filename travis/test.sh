#!/bin/sh

set -eu

rm -rf build_travis
mkdir build_travis
cd build_travis
cmake ..
make dist
cd ..

unzip -l  build_travis/proj-data*.zip | tail -n +4 | head -n -2 | awk '{print $4}' | sort > /tmp/got_main.lst
cat travis/expected_main.lst | sort > /tmp/expected_main.lst
if ! diff -u /tmp/expected_main.lst /tmp/got_main.lst; then
    echo "Got difference in proj-data"
    exit 1;
fi
