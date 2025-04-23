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
                _entries.append(line.removesuffix('\n'))
    return _entries


def should_ignore(filename: str) -> bool:
    """ returns True if filename matches an entry in makeignore """
    # TODO : make this compatible to filter-out; see:
    #        https://www.gnu.org/software/make/manual/html_node/Text-Functions.html
    for entry in entries():
        if filename.startswith(entry):
            return True
    return False


def filter(filenames):
    for filename in filenames:
        if should_ignore(filename):
            yield filename


def filter_out(filenames):
    for filename in filenames:
        if not should_ignore(filename):
            yield filename


if __name__ == '__main__':
    # TEST!
    # Call From $PROJECT_ROOT!
    print(entries())
    print(f"{should_ignore('src/blog/tech/bye-gnome-hi-xfce-part-1.md')=}")
    print(f"{should_ignore('src/blog/tech/ippy.md')=}")
    print(f"{list(filter(['src/blog/tech/bye-gnome-hi-xfce-part-1.md', 'src/blog/tech/ippy.md']))=}")
    print(f"{list(filter_out(['src/blog/tech/bye-gnome-hi-xfce-part-1.md', 'src/blog/tech/ippy.md']))=}")

