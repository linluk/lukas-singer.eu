#!/bin/bash

# converts given image files or the image files in the given directories to a "lukas-singer.eu-friendly" format
# usage:
#     ./convert-images.sh  [FILES | DIRECTORIES]  OUTPUT-DIRECTORY
#
# first arguments are directories or files to be converted (jpg, png)
# last argument is the output directory for the converted files.
# keeps the basename with $NEW_EXT extension.
#
# use paths relative to project root!
#
# example call:
#     ./tools/convert-images.sh tmp/* out/

# change the directory to where this script is
cd "$(realpath $(dirname $0))"
# change upwards from the to whereevery the project root is
. lib/ensure_project_root.sh

# the new extension/file format
NEW_EXT=webp

# the last argument
OUT_DIR="${*: -1}"


for INPUT in ${@: 1:$#-1}; do
    if [[ -d $INPUT ]]; then
        echo "$INPUT is a directory."
    elif [[ -f $INPUT && $INPUT =~ .*\(webp|png|jpg|jpeg\)$ ]]; then
        ffmpeg                                           \
            -hide_banner -loglevel error                 \
            -i "$INPUT"                                  \
            -vf scale="'min(1000,iw)':-1"                \
            "$OUT_DIR/$(basename ${INPUT%.*}.$NEW_EXT)"
    else
        echo "Don't know how to convert $INPUT  \\_( '_')_/"
    fi
done
