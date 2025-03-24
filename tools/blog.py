#!/usr/bin/env python3

"""
A small Tool to handle Blog related stuff.

Usage:
    python3 blog.py ARGUMENT

Arguments:
-h, --help                print this help text and exits without error.

-u, --update              reads the yaml headers from all markdown files under
                          './src/blog/**' (except './src/blog/**/index.md'),
                          rewrites the corresponding 'index.md' files and
                          creates 'rss.xml' files in './src/blog/' and its
                          subdirectories (categories).

-n, --new CATEGORY TITLE  creates a new file './src/blog/<CATEGORY>/<TITLE>.md'
                          and inserts the basic yaml configuration header.
"""

import sys
import os
import datetime
import yaml
from lib.log import error, warning, info, debug
from lib.ensure_project_root import ensure_project_root

# import lib.log
# lib.log.LOG_DEBUG = True
# lib.log.LOG_INFO = True
# lib.log.LOG_WARNING = True

APP_NAME = 'blog.py'
APP_VERSION = 'v0.2'
APP_NAME_VERSION = f'{APP_NAME} {APP_VERSION}'

BLOG_PATH = 'src/blog/'

KEEP_GOING_ON_YAML_ERROR = False


def datetime2rfc2822(dt: datetime.datetime | None = None) -> str:
    """ returns the date and time represented by dt
    in RFC2822 compatible format using CET (central european time)
    with DLT (daylight saving time).
    rss feeds use this format.
    if dt is None it will assume now().
    see: https://www.rfc-editor.org/rfc/rfc2822#section-3.3
    """
    if dt is None:
        dt = datetime.datetime.now()

    dst_start = datetime.datetime(
        dt.year,
        3,  # Month (March)
        (31 - datetime.date(dt.year, 3, 31).weekday()),  # Last Sunday of March
        3,  # Hour
        0,  # Minute
        0,  # Second
        1   # Microsecond
    )
    # same as dst_start, but ists last Sunday of October
    dst_end = datetime.datetime(
        dt.year, 10, (31 - datetime.date(dt.year, 10, 31).weekday()),
        3, 0, 0, 1)

    if dst_start <= dt < dst_end:
        offset = datetime.timedelta(hours=2)  # CEST (UTC+2)
    else:
        offset = datetime.timedelta(hours=1)  # CET (UTC+1)
    # Convert to GMT
    dt = dt - offset
    # zone = 'GMT'
    zone = '+0000'
    # OR
    # calculate the CET/CEST
    # zone = '0200' if dst_start < dt < dst_end else '0100'

    return dt.strftime(f'%a, %d %b %Y %H:%M:%S {zone}')


def date2rfc2822(d: datetime.date | None = None) -> str:
    """ same as 'datetime2rfc2822()' but uses date instead of datetime,
    which implies static 00:00:00 (midnight) for the time part.
    """
    if d is None:
        d = datetime.date.today()
    d = datetime.datetime.combine(d, datetime.time.min)
    return datetime2rfc2822(d)


BLOG_MAIN_INDEX_HEAD = f"""---
title: Blog
lang: de
keywords:
- blog
description: Index of Blog
blog-title:
blog-date:
nav-blog: true
nav-blog-home: true
blog-changelog:
comment: created by blog.py {datetime.datetime.now():%Y-%m-%d %H:%M:%S}
---
<!-- created by blog.py {datetime.datetime.now():%Y-%m-%d %H:%M:%S} -->

blog <a href="rss.xml"><img src="/images/rss.png" alt="rss" height=24></a>
===

"""

BLOG_CATEGORY_INDEX_HEAD = f"""---
title: Blog({{category}})
lang: de
keywords:
- blog
- {{category}}
description: Index of Blog about {{category}}
blog-title:
blog-date:
nav-blog: true
nav-blog-{{category}}: true
blog-changelog:
comment: created by blog.py {datetime.datetime.now():%Y-%m-%d %H:%M:%S}
---
<!-- created by blog.py {datetime.datetime.now():%Y-%m-%d %H:%M:%S} -->

{{category}} <a href="rss.xml"><img src="/images/rss.png" alt="rss" height=24></a>
===

"""

BLOG_INDEX_ENTRY = (
    '<li>'
    '<a href="{href}">{title}</a>'
    '<br>'
    '<small>[{lang}] {date} ({keywords})</small>'
    '</li>\n')

BLOG_NEW_POST = f"""---
title: {{title}}
lang: de
keywords:
- blog
- {{category}}
- {{title}}
description: {{category}} - {{title}}
blog-title: {{title}}
blog-date: {datetime.date.today():%Y-%m-%d}
nav-blog: true
nav-blog-{{category_dirname}}: true
blog-changelog:
---

Hier den Blogeintrag schreiben ...
Und nicht vergessen, den YAML Header anzupassen!
"""

RSS_TEMPLATE = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
  <title>{{title}}</title>
  <link>{{link}}</link>
  <description>{{description}}</description>
  <lastBuildDate>{datetime2rfc2822()}</lastBuildDate>
  <generator>{APP_NAME_VERSION}</generator>
{{items}}
</channel>
</rss>
"""

RSS_ITEM_TEMPLATE = """  <item>
    <title>{title}</title>
    <link>{link}</link>
    <description>{description}</description>
    <author>Lukas Singer</author>
    <pubDate>{date}</pubDate>
  </item>"""


def filename_compatible(name: str) -> str:
    """ converts a name (f.e. blog title) in a filename friendly name """
    # my filenames should only consist of [a-z\-0-9]
    return ''.join(c for c in (name
                               .lower()
                               .replace(' ', '-')
                               .replace('/', '-')
                               .replace('\\', '-')
                               .replace('_', '-')
                               .replace('ä', 'ae')
                               .replace('ö', 'oe')
                               .replace('ü', 'ue')
                               .replace('ß', 'sz'))
                   if c in 'abcdefghijklmnopqrstuvwxyz-1234567890')


def update_index_files(category_headers: dict[str, list[dict]]):
    toplevel_index_file = os.path.join(BLOG_PATH, 'index.md')
    with open(toplevel_index_file, 'w') as toplevel_index:
        toplevel_index.write(BLOG_MAIN_INDEX_HEAD)
        # TODO: currently we sort categories alphabetically,
        #       maybe we should sort by latest blog entry overall
        for category, headers in sorted(
                category_headers.items(),
                key=lambda chs: chs[0]):
            toplevel_index.write(f'{category} <a href="{category}/rss.xml"><img src="/images/rss.png" alt="rss" height=16></a>\n---\n\n<ul>\n')
            category_index_file = os.path.join(BLOG_PATH, category, 'index.md')
            with open(category_index_file, 'w') as category_index:
                category_index.write(
                    BLOG_CATEGORY_INDEX_HEAD.format(category=category))
                category_index.write("<ul>")
                for header in sorted(headers,
                                     key=lambda h: h.get('blog-date', '0'),
                                     reverse=True):
                    href = header.get('href', None)
                    if href is None:
                        error(0, "'href' missing in data!", **header)
                        continue
                    entry = {
                        'href': href,
                        'title': header.get('title', 'No Title Found!'),
                        'lang': header.get('lang', 'de'),
                        'keywords': '|'.join(
                            header.get('keywords', ['blog', category])),
                        'date': header.get('blog-date', 'unknown')}
                    category_index.write(BLOG_INDEX_ENTRY.format(**entry))
                    toplevel_index.write(BLOG_INDEX_ENTRY.format(**entry))
                category_index.write("</ul>")
            toplevel_index.write("</ul>\n\n")


def analyze_nested_types(x, prefix=''):
    print(f'{prefix}{type(x)}{getattr(x, "__name__", "")}')
    if isinstance(x, dict):
        for k, v in x.items():
            print(f'{prefix}>Key: ', end='')
            analyze_nested_types(k, f'  {prefix}')
            print(f'{prefix}>Value: ', end='')
            analyze_nested_types(v, f'  {prefix}')
            print(prefix, end='')
            print('-' * (len(prefix) + 10))
    elif isinstance(x, (list, set, tuple)):
        for i in x:
            analyze_nested_types(i, f'  {prefix}')
            print(prefix, end='')
            print('-' * (len(prefix) + 10))


def update_rss_files(category_headers: dict[str, list[dict]]):
    # def ymd2d(ymd):
    #     t = ymd.split('-')
    #     d = datetime.date()
    #     d.replace(year=t[0], month=t[1], day=t[2])
    #     return d

    all_items = []
    category_items = {}
    for category, headers in category_headers.items():
        category_items[category] = []
        for header in headers:
            if 'href' not in header:
                continue
            item = RSS_ITEM_TEMPLATE.format(
                title=header.get('title', 'unknown'),
                link=f"https://lukas-singer.eu{header.get('href')}",
                description=header.get('description', ''),
                date=date2rfc2822(header.get('blog-date')))
            all_items.append(item)
            category_items[category].append(item)

    toplevel_feed_file = os.path.join(BLOG_PATH, 'rss.xml')
    with open(toplevel_feed_file, 'w') as toplevel_feed:
        toplevel_feed.write(
            RSS_TEMPLATE.format(
                title="(.*) auf lukas-singer.eu",
                link="https://lukas-singer.eu/blog",
                description="Der gesamte Blog auf lukas-singer.eu",
                items='\n'.join(all_items)))

    for category in category_items:
        category_feed_file = os.path.join(BLOG_PATH, category, 'rss.xml')
        with open(category_feed_file, 'w') as category_feed:
            category_feed.write(
                RSS_TEMPLATE.format(
                    title=f"{category} auf lukas-singer.eu",
                    link=f"https://lukas-singer.eu/blog/{category}",
                    description=f"Blog über {category} auf lukas-singer.eu",
                    items='\n'.join(category_items[category])))


def update_blog():
    # read categories and yaml headers
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
            if (os.path.isfile(os.path.join(cat_dir, e))
                and e != 'index.md'
                and e.endswith('.md'))]
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
    debug(category_headers)
    # pass categories and headers to index-builder and rss-builder
    update_index_files(category_headers)
    update_rss_files(category_headers)


def new_blog_entry(category: str, title: str) -> None:
    categories: list[str] = [
        dir
        for dir in os.listdir(BLOG_PATH)
        if os.path.isdir(os.path.join(BLOG_PATH, dir))]
    category_dirname = filename_compatible(category)
    cat_dir = os.path.join(BLOG_PATH, category_dirname)
    if category_dirname not in categories:
        warning(f'New Category: {category_dirname} ({category})!')
        print('You are about to create a new blog category.')
        print(f'This will create the directory "{cat_dir}"')
        print('Make sure to add it to template.html')
        print('grep for "blog-nav-*"')
        answer = ''
        while answer not in ('y', 'yes', 'n', 'no'):
            answer = input('Create new category? (y/n)').lower()
        if answer not in ('y', 'yes'):
            error(0, 'User canceled.')
            return  # unreachable error() calls exit()
    os.makedirs(cat_dir, exist_ok=True)

    entry_file = os.path.join(cat_dir, f"{filename_compatible(title)}.md")
    if os.path.exists(entry_file):
        error(1, f'Entry "{entry_file}" already exists! Skipping...')
        return  # unreachable error() calls exit()

    with open(entry_file, 'w') as file:
        file.write(
            BLOG_NEW_POST.format(
                title=title,
                category=category,
                category_dirname=category_dirname))
    info(f'New blog entry created: "{entry_file}"')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__.strip())
        exit(1)
    elif ('-h' in sys.argv) or ('--help' in sys.argv):
        print(__doc__.strip())
    elif len(sys.argv) == 2 and sys.argv[1] in ('-u', '--update'):
        ensure_project_root()
        update_blog()
    elif len(sys.argv) == 4 and sys.argv[1] in ('-n', '--new'):
        category = sys.argv[2]
        title = sys.argv[3]
        info(f'{category=}, {title=}')
        new_blog_entry(category, title)
    else:
        print('Unknown or Invalid Arguments. Try --help')
        exit(1)
