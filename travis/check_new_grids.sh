#!/usr/bin/env bash

# Verify that grids added or modified in a pull request are conformant

set -eu

if [ -z "$TRAVIS_COMMIT_RANGE" ]; then
        echo "No commit range given"
        exit 0
fi

if [[ -n  $TRAVIS_PULL_REQUEST_BRANCH  ]]; then
  # if on a PR, just analyze the changed files
  echo "TRAVIS PR BRANCH: $TRAVIS_PULL_REQUEST_BRANCH"
  FILES=$(git diff --diff-filter=AM --name-only $(git merge-base HEAD ${TRAVIS_BRANCH}) | tr '\n' ' ' )
elif [[ -n  $TRAVIS_COMMIT_RANGE  ]]; then
  echo "TRAVIS COMMIT RANGE: $TRAVIS_COMMIT_RANGE"
  FILES=$(git diff --diff-filter=AM --name-only ${TRAVIS_COMMIT_RANGE/.../..} | tr '\n' ' ' )
fi

for f in $FILES; do
    if ! [ -f "$f" ]; then
            continue
    fi

    case "$f" in
    *.tif)
            ;;

    *)
            continue
            ;;
    esac

    echo "Checking $f"
    docker run --rm -v /home:/home osgeo/gdal:alpine-normal-latest gdalinfo -mm $PWD/$f
    docker run --rm -v /home:/home osgeo/gdal:alpine-normal-latest python3 $PWD/grid_tools/check_gtiff_grid.py $PWD/$f
done
