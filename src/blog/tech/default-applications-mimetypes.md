---
title: Default Applications (MimeTypes)
lang: en
keywords:
- blog
- tech
- Default Applications (MimeTypes)
- mime
- brave
- default
- bash
- sh
- grep
- markdown
- linux
- debian
- xfce
description: tech - Default Applications (MimeTypes)
blog-title: Default Applications (MimeTypes)
blog-date: 2026-03-05
nav-blog: true
nav-blog-tech: true
blog-changelog:
---

> **TL;DR:** how to "revert" messed up default application after installing brave (or any other app that fucks up mime type associations)

## the story

Yesterday I had the *great* idea of installing [brave](https://brave.com/) on my machine. Not because I want to use it, but I want to "test" it.

It worked, it launched, it asked if I want it to be my "Default Browser", no! (I am 98,765% sure, that I clicked on "NO") ... everything was fine. I went to bed.

**but**

Today I wanted to open a PDF, using `xdg-open`. Surprise: the PDF opened in *brave*. Ok, stupid, lets fix it.  
So I opened up the "Default Applications"-Settings on XFCE.

**WTF**

*brave* is set as default Browser,  
*brave* is set as default PDF-Viewer,  
*brave* is set as default Image-Viewer,  
*brave* is set as default *<small><small>fuckin'</small> (almost) </small>**everything**!*

<br>

After *deleting* or resetting some entries in the Settings GUI I found, that they get marked as *modified* and setting them to *default* (*re*)sets the entries to brave ...

Suspicious!

So I have read a little bit about how "Default Application"/"Default MimeType"-handling worked.

Then I wrote a little Shell Script to find *all* locations of interest.

The script generated a report, then I manually "*fixed*" all files and regenerated the mime caches.

**voila**

The mess is gone!

## the background

Default Applications based on Mime Types works in a quite clever way on Linux.

First, there are `.desktop`-files. They contain information like the icon for the UI, the command to be executed when run, ... *and* a list of MimeTypes, which can be opened by
the app.

Second, there are `mimeinfo.cache` files. These are generated files, the command `update-desktop-database` reads all `.desktop` files and populates them.
They are the base for handy "Default Application"-UIs.

Last but not least, there are some default app `.list` files. Some for system defaults (in `/usr/...`), some for "admin" defaults (in `/etc/...`) and some per user (in `$HOME/.config/...` or `$HOME/.local/...`). These files are what you can edit via the "Default Application"-UI.

Most of the *known* MimeTypes had no assosiated application (why would I wan't to have an application for "*Windows App Store Installer*", ...?) and I don't want brave to populate those *empty* entries.

So I had to delete them in a way, that `update-desktop-database` would not regenerate `.list` files with brave.

Easier said than done. I was in desperate need of a `bash` script reporting all these locations. (the brave installer put `brave` in lots of places.)


## the script

```bash
#!/usr/bin/env bash
set -euo pipefail

DEFAULT_APP_FILES=( \
    "$HOME/.config/mimeapps.list" \
    "$HOME/.local/share/applications/mimeapps.list" \
    "/etc/xdg/xfce4/helpers.rc" \
    "/etc/xdg/mimeapps.list" \
    "/usr/share/applications/mimeapps.list" \
    "/usr/share/applications/defaults.list" \
    "/usr/local/share/applications/mimeapps.list" \
    "/usr/local/share/applications/defaults.list" \
)
DESKTOP_FILES=( \
    "/usr/share/applications/brave-browser.desktop" \
    "/usr/share/applications/brave-browser-beta.desktop" \
    "/usr/share/applications/brave-browser-nightly.desktop" \
    "/usr/share/applications/com.brave.Browser.desktop" \
)
MIME_CACHE_FILES=( \
    "/usr/local/share/applications/mimeinfo.cache" \
    "/usr/share/applications/mimeinfo.cache" \
)

do_report() {
    # usage:
    #     do_report  TITLE  PATTERN  ARRAY
    # where:
    #     TITE      is the title.
    #     PATTERN   is whatever you want to look for (f.e. brave)
    #     ARRAY     is an array of filenames to check
    local TITLE=$1
    local PATTERN=$2
    shift 2  # "skips" the first 2 arguments
    printf '\n## Common "%s"\n\n' "$TITLE"
    printf 'Search Pattern: `%s`\n\n' "$PATTERN"
    for FILE in "$@"; do
        if [ -f "$FILE" ]; then
            printf '### %s\n\n' "$FILE"
            MATCHES=$(grep -i "$PATTERN" "$FILE" || true)
            if [[ "$MATCHES" != "" ]]; then
                printf '```plain\n'
                printf '%s' "$MATCHES"
                printf '\n```\n\n'
            else
                printf 'Pattern not found.\n\n'
            fi
        fi
    done
}

printf '# fu-brave report\n'

do_report "Default-App Files" brave "${DEFAULT_APP_FILES[@]}"
do_report ".desktop Files" "MimeType=" "${DESKTOP_FILES[@]}"
do_report "MIME-Cache Files" brave "${MIME_CACHE_FILES[@]}"

printf '# Next Steps\n\n'
printf 'Clean Up whatever you want to clean up; then do:\n\n'
printf '```\n$ sudo update-desktop-database\n```\n'
```

[fu-brave.sh](https://codeberg.org/linluk/dump/src/branch/main/fu-brave.sh) (this `bash` script, on `codeberg.org`)

<br>

**Thanks for Reading :-)**

