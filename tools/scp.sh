#!/bin/bash

# change the directory to where this script is
cd "$(realpath $(dirname $0))"
# change upwards from the to whereevery the project root is
. lib/ensure_project_root.sh

if [[ -f secrets.sh ]]; then
    . secrets.sh
    if [[ -z "${SECRET_SCP_IDENTITY_FILE:-}" ]]; then
        echo "SECRET_SCP_IDENTITY_FILE is not set or empty. Check secrets.sh" 1>&2
        exit 1
    fi
    if [[ -z "${SECRET_SCP_USER:-}" ]]; then
        echo "SECRET_SCP_USER is not set or empty. Check secrets.sh" 1>&2
        exit 1
    fi
    scp -i "$SECRET_SCP_IDENTITY_FILE" -r www/* scp://$SECRET_SCP_USER@lukas-singer.eu/public_html/
else
    echo "secret.sh not found." 1>&2
    exit 1
fi
