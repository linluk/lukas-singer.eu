#!/bin/bash

# change the directory to where this script is
cd "$(realpath "$(dirname "$BASH_SOURCE")")"
# change upwards from the to whereevery the project root is
. lib/ensure_project_root.sh

if [[ -f secrets.sh ]]; then
    . secrets.sh
    if [[ -z "${SECRET_SSH_IDENTITY_FILE:-}" ]]; then
        echo "SECRET_SSH_IDENTITY_FILE is not set or empty. Check secrets.sh" 1>&2
        exit 1
    fi
    if [[ -z "${SECRET_SSH_USER:-}" ]]; then
        echo "SECRET_SSH_USER is not set or empty. Check secrets.sh" 1>&2
        exit 1
    fi
    ssh -i "$SECRET_SSH_IDENTITY_FILE" $SECRET_SSH_USER@lukas-singer.eu
else
    echo "secret.sh not found." 1>&2
    exit 1
fi
