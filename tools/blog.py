#!/usr/bin/env python3

"""
A small Tool to handle Blog related stuff.

Usage:
    python3 blog.py ARGUMENT

Arguments:
-h, --help                print this help text and exits without error.

-u, --update              reads the yaml headers from all markdown files under
                          './src/blog/**' (except './src/blog/**/index.md') and
                          updates the corresponding 'index.md'.

-n, --new CATEGORY TITLE  creates a new file './src/blog/<CATEGORY>/<TITLE>.md'
                          and inserts the basic yaml configuration header.
"""

import sys
import os
import datetime
import yaml

BLOG_PATH = 'src/blog/'

KEEP_GOING_ON_YAML_ERROR = False

LOG_DEBUG = False
LOG_INFO = LOG_DEBUG or True
LOG_WARNING = LOG_INFO or True


def message_builder(message: str, *args, **kwargs) -> str:
    return (f'{message}'
            f'{", " if args else ""}{", ".join(map(str, args))}'
            f'{", " if args else ""}'
            f'{", ".join(f"{k}: {v}" for k, v in kwargs.items()) if kwargs is not None else ""}')  # noqa E501


def error(code: int | None, message: str, *args, **kwargs) -> None:
    print(f'[ERROR] {message_builder(message, *args, **kwargs)}',
          file=sys.stderr)
    if code is not None:
        exit(code)


def debug(message: str, *args, **kwargs) -> None:
    if LOG_DEBUG:
        print(f'[DEBUG] {message_builder(message, *args, **kwargs)}')


def info(message: str, *args, **kwargs) -> None:
    if LOG_INFO:
        print(f'[INFO] {message_builder(message, *args, **kwargs)}')


def warning(message: str, *args, **kwargs) -> None:
    if LOG_WARNING:
        print(f'[WARNING] {message_builder(message, *args, **kwargs)}')


def ensure_project_root():
    # Find and Change to Project Root (indicated by the presence of '.git')
    while not os.path.isdir('.git'):
        os.chdir('..')
        if os.getcwd() == '/':
            error(1, 'Project Root not found!')
    debug(f"Project Root: '{os.getcwd()}'")


def filename_compatible(name: str) -> str:
    return ''.join(c for c in (name
                               .lower()
                               .replace(' ', '_')
                               .replace('/', '-')
                               .replace('\\', '-')
                               .replace('ä', 'ae')
                               .replace('ö', 'oe')
                               .replace('ü', 'ue')
                               .replace('ß', 'sz'))
                   if c in 'abcdefghijklmnopqrstuvwxyz_-1234567890')


def update_index_files():
    categories: list[str] = [
        dir
        for dir in os.listdir(BLOG_PATH)
        if os.path.isdir(os.path.join(BLOG_PATH, dir))]
    debug(f'{categories=}')
    category_headers = {c: list() for c in categories}
    for category in categories:
        cat_dir = os.path.join(BLOG_PATH, category)
        entries: list[str] = [
            e
            for e in os.listdir(cat_dir)
            if os.path.isfile(os.path.join(cat_dir, e)) and e != 'index.md']
        for entry in entries:
            entry_file = os.path.join(cat_dir, entry)
            debug(f"{category=}, {cat_dir=}, {entry=}, {entry_file=}")
            header = []
            with open(entry_file, 'r') as file:
                for lno, line in enumerate(file):
                    debug(f'{lno=}: {line=}')
                    if lno == 0:
                        if line != '---\n':
                            warning('No YAML Header found in'
                                    f'"{entry_file}". Skipping...')
                            break
                        continue
                    if line == '---\n':
                        # end of yaml header
                        break
                    header.append(line)
            try:
                category_headers[category].append(
                    {'href': entry_file
                        .removeprefix('src')
                        .removesuffix('.md') + '.html',
                     **yaml.safe_load(''.join(header))})
            except yaml.YAMLError as ex:
                debug('yaml.safe_load() failed!',
                      ex, entry_file, ''.join(header))
                error(None if KEEP_GOING_ON_YAML_ERROR else 1,
                      f'Failed to parse YAML Header in "{entry_file}" '
                      f'{"Continue" if KEEP_GOING_ON_YAML_ERROR else "Stop"}!')
    # TODO: index.md files befüllen.
    debug(category_headers)
    toplevel_index_file = os.path.join(BLOG_PATH, 'index.md')
    with open(toplevel_index_file, 'w') as toplevel_index:
        toplevel_index.write(f"""---
title: Blog
lang: de
keywords:
- blog
- lukas singer
description: Index of Blog
blog-title:
blog-date:
nav-blog: true
blog-changelog:
comment: created by blog.py {datetime.datetime.now():%Y-%m-%d %H:%M:%S}
---
<!-- created by blog.py {datetime.datetime.now():%Y-%m-%d %H:%M:%S} -->

Blog
====
""")
        for category, headers in category_headers.items():
            toplevel_index.write(f"""
{category}
----------

<ul>
""")
            category_index_file = os.path.join(BLOG_PATH, category, 'index.md')
            with open(category_index_file, 'w') as category_index:
                category_index.write(f"""---
title: Blog({category})
lang: de
keywords:
- blog
- lukas singer
- {category}
description: Index of Blog about {category}
blog-title:
blog-date:
nav-blog: true
nav-blog-{category}: true
blog-changelog:
comment: created by blog.py {datetime.datetime.now():%Y-%m-%d %H:%M:%S}
---
<!-- created by blog.py {datetime.datetime.now():%Y-%m-%d %H:%M:%S} -->

{category}
==========

<ul>
""")
                for header in headers:
                    href = header.get('href', None)
                    if href is None:
                        error(0, "'href' missing in data!", **header)
                        continue
                    title = header.get('title', 'No Title Found!')
                    lang = header.get('lang', 'de')  # default website language
                    keywords = header.get('keywords', ['blog', category])
                    date = header.get('blog-date', None)
                    category_index.write(f"""<li>
<a href="{href}">{title}</a><br><small>[{lang}] {date} ({'|'.join(keywords)})</small>
</li>
""")
                    toplevel_index.write(f"""<li>
<a href="{href}">{title}</a><br><small>[{lang}] {date} ({'|'.join(keywords)})</small>
</li>
""")
                category_index.write("</ul>")
        toplevel_index.write("</ul>\n\n")


def new_blog_entry(category: str, title: str) -> None:
    categories: list[str] = [
        dir
        for dir in os.listdir(BLOG_PATH)
        if os.path.isdir(os.path.join(BLOG_PATH, dir))]
    category_dirname = filename_compatible(category)
    if category_dirname not in categories:
        warning(f'New Category: {category_dirname} ({category})!')
    cat_dir = os.path.join(BLOG_PATH, category_dirname)
    os.makedirs(cat_dir, exist_ok=True)

    entry_file = os.path.join(cat_dir, f"{filename_compatible(title)}.md")
    if os.path.exists(entry_file):
        error(1, f'Entry "{entry_file}" already exists! Skipping...')
        return

    with open(entry_file, 'w') as file:
        file.write(f"""---
title: {title}
lang: de
keywords:
- blog
- lukas singer
- {category}
- {title}
description: {category} - {title}
blog-title: {title}
blog-date: {datetime.date.today():%Y-%m-%d}
nav-blog: true
nav-blog-{category_dirname}: true
blog-changelog:
---

Hier den Blogeintrag schreiben ...
Und nicht vergessen, den YAML Header anzupassen!
""")
    info(f'New blog entry created: "{entry_file}"')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__.strip())
        exit(1)
    elif ('-h' in sys.argv) or ('--help' in sys.argv):
        print(__doc__.strip())
    elif len(sys.argv) == 2 and sys.argv[1] in ('-u', '--update'):
        ensure_project_root()
        update_index_files()
    elif len(sys.argv) == 4 and sys.argv[1] in ('-n', '--new'):
        category = sys.argv[2]
        title = sys.argv[3]
        info(f'{category=}, {title=}')
        new_blog_entry(category, title)
    else:
        print('Unknown or Invalid Arguments. Try --help')
        exit(1)
