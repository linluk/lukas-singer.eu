---
title: Bash - Command Line Arguments
lang: de
keywords:
- blog
- tech
- bash
- command line arguments
- dirname
- basename
- realpath
description: Bash - Command Line Arguments - Kurz und Knapp ein paar Basics zur Arbeit mit Kommandozeilenargumenten sowie  Pfaden und Dateinamen
blog-title: Bash - Command Line Arguments
blog-date: 2025-04-02
nav-blog: true
nav-blog-tech: true
blog-changelog:
---

> *Es gibt Dinge, die würden in meinem Google-Suchverlauf sehr häufig auftauchen;  
> wenn das die Suchmaschine meiner Wahl wäre.*  
>
> *Das Handling von Kommandozeilenargumenten und das Arbeiten mit dem eigenen Pfad bzw.
> dem eigenen Dateinamen in Bash-Skripten wären solche Dinge.*

<br>

Without any further ado schauen wir uns hier Kurz und Knapp ein paar Bash-Basics an.

# Pfade und Dateinamen

## `$0`

```sh
# how your script was called
# f.e.:  './my-script.sh'
#   or:  './path/to/my-script.sh'
#   or:  'my-script.sh'
echo "\$0 = $0"
```

## `basename`

```sh
# the name of your script
echo "\$(basename \$0) = $(basename $0)"
```

## `realpath`

```sh
# the absoulte path to your script
echo "\$(realpath \$0) = $(realpath $0)"
```

## `dirname`

```sh
# the directory of your script (relative)
echo "\$(dirname \$0) = $(dirname $0)"
```

## `realpath` $+$ `dirname` $= <3$

```sh
# the directory of your script (absolute)
echo "\$(realpath \$(dirname \$0)) = $(realpath $(dirname $0))"
```

# Kommandozeilenargumente

## By Position `$1`, `$2`, ... `$n`

```sh
# the first command line argument
# (replace 1 with 2 for the 2nd, with 3 for the 3rd, ...)
echo "\$1 = $1"
```

## Alle auf Einmal

### Wirklich alle auf Einmal

```sh
# all arguments as one string seperated by $IFS (spaces by default)
echo "\$* = $*"
echo "\$(IFS='|' ; echo \"\$*\") = $(IFS='|' ; echo "$*")"
```

### Oder als Array

```sh
# all arguments as an array
echo "\$@ = $@"
```

## Die Anzahl

```sh
# the number of arguments (excluding $0)
echo "\$# = $#"
```

## Das Letzte

```sh
# the last argument
echo "\${\*: -1} = ${*: -1}"
```

## Alle außer das Letzte

```sh
# all (excluding $0) but the last argument
echo "\${\*: 1:\$#-1} = ${*: 1:$#-1}"
```

# In Action

```plain
$ pwd
/home/linluk
$ ./tmp/my-script.sh

$0 = ./tmp/my-script.sh
$(basename $0) = my-script.sh
$(realpath $0) = /home/linluk/tmp/my-script.sh
$(dirname $0) = ./tmp
$(realpath $(dirname $0)) = /home/linluk/tmp
$1 = arg1
$* = arg1 arg2 arg 3 arg4 arg5
$(IFS='|' ; echo "$*") = arg1|arg2|arg 3|arg4|arg5
$@ = arg1 arg2 arg 3 arg4 arg5
$# = 5
${\*: -1} = arg5
${\*: 1:$#-1} = arg1 arg2 arg 3 arg4
```

# Anhang

Hier noch das Skript als Ganzes:
<small>
```sh
#!/bin/bash

# how your script was called
# f.e.:  './my-script.sh'
#   or:  './path/to/my-script.sh'
#   or:  'my-script.sh'
echo "\$0 = $0"

# the name of your script
echo "\$(basename \$0) = $(basename $0)"

# the absoulte path to your script
echo "\$(realpath \$0) = $(realpath $0)"

# the directory of your script (relative)
echo "\$(dirname \$0) = $(dirname $0)"

# the directory of your script (absolute)
echo "\$(realpath \$(dirname \$0)) = $(realpath $(dirname $0))"

# the first command line argument
# (replace 1 with 2 for the 2nd, with 3 for the 3rd, ...)
echo "\$1 = $1"

# all arguments as one string seperated by $IFS (spaces by default)
echo "\$* = $*"
echo "\$(IFS='|' ; echo \"\$*\") = $(IFS='|' ; echo "$*")"

# all arguments as an array
echo "\$@ = $@"

# the number of arguments (excluding $0)
echo "\$# = $#"

# the last argument
echo "\${\*: -1} = ${*: -1}"

# all (excluding $0) but the last argument
echo "\${\*: 1:\$#-1} = ${*: 1:$#-1}"
```
</small>
