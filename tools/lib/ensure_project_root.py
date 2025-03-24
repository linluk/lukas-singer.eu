#!/usr/bin/env python3

"""
    use this to walk up the directory tree until we hit our
    project root directory, which is indicated by the presence
    of our beloved '.git/' directory
"""

import os

import lib.log as log


def ensure_project_root():
    # Find and Change to Project Root (indicated by the presence of '.git')
    while not os.path.isdir('.git'):
        os.chdir('..')
        if os.getcwd() == '/':
            log.error(1, 'Project Root not found!')
    log.debug(f"Project Root: '{os.getcwd()}'")
