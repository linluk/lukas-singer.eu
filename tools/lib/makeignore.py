#!/usr/bin/env python3

"""
    This file handles the makeignore file.
    The reference implementation is the Makefile directive:

        IGNORE := $(shell grep -vE '^\s*\#|^\s*$$' makeignore)

    applied as:

        MARKDOWN_SOURCES := $(filter-out $(IGNORE),$(MARKDOWN_SOURCES))

    See also the extensive comment in:

        $PROJECT_ROOT/makeignore

    This module is required to be run with CWD in $PROJECT_ROOT!
    See: ensure_project_root.py

"""


import re


MAKEIGNORE = 'makeignore'

_entries = None


def entries():
    global _entries
    if _entries is not None:
        return _entries
    _entries = list()
    regex = re.compile(r"^\s*\#|^\s*$", re.IGNORECASE)
    with open(MAKEIGNORE, 'r') as file:
        for line in file:
            if not regex.match(line):
                _entries.append(line)
    return _entries


def ignore(filename: str) -> bool:
    """ returns True if filename matches an entry in makeignore """
    # TODO : make this compatible to filter-out; see:
    #        https://www.gnu.org/software/make/manual/html_node/Text-Functions.html
    return False


if __name__ == '__main__':
    # TEST!
    # Call From $PROJECT_ROOT!
    print(entries())
