#!/bin/bash

#
# source this file to walk up the directory tree until we hit our project
# root directory, which is indicated by the presence of our beloved '.git/'
# directory.
#

while [[ ! -d .git/ ]]; do
    cd ..
    if [[ $(pwd) == "/" ]]; then
        echo "Project Root not found!" >&2
        exit 1
    fi
done
echo "[INFO] Changed to Project Root: '$(pwd)'"
