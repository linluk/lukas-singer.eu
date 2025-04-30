---
title: Linux - Begriffe
lang: de
keywords:
- tfbs-eke
- linux
- begriffe
description: Linux, GNU/Linux, Kernel, Shell, Terminal, Distribution, Paketmanager, ...
use-toc: true
nav-schule: true
nav-schule-linux: true
---

<center>
    ***Diese Seite ist Work in Progress!***
    <br>
    <small>
        *Input (Ideen, Wünsche, Fehler, Ergänzungen) sind natürlich Willkommen!*
    </small>
</center>

<br>

<center> **Nutze `<C-f>` in deinem Browser!** </center>

<br>

### Linux
ist genau genommen kein Betriebssystem, sondern "nur" ein Kernel.

Das erste Erscheinen von Linux ist in der Usenet Gruppe `comp.os.minix` dokumentiert,
dort schrieb Linus Thorvalds am 25. August 1991 folgende historische Zeilen:
<small>
```plain
 Hello everybody out there using minix -

I'm doing a (free) operating system (just a hobby, won't be big and
professional like gnu) for 386(486) AT clones. This has been brewing
since april, and is starting to get ready. I'd like any feedback on
things people like/dislike in minix, as my OS resembles it somewhat
(same physical layout of the file-system (due to practical reasons)
among other things).

I've currently ported bash(1.08) and gcc(1.40), and things seem to work.
This implies that I'll get something practical within a few months, and
I'd like to know what features most people would want. Any suggestions
are welcome, but I won't promise I'll implement them :-)

Linus (torv...@kruuna.helsinki.fi)

PS. Yes - it's free of any minix code, and it has a multi-threaded fs.
It is NOT protable (uses 386 task switching etc), and it probably never
will support anything other than AT-harddisks, as that's all I have :-(.
```
</small>

### GNU
steht für **G**NU is **N**ot **U**nix.  
Es ist eine Sammlung von Werkzeugen, die aus der Unix-Welt bekannt sind.
Ziel war und ist es ein vollständiges und freies Betriebssystem zu sein,
als Kernel können neben *Linux* auch *BSD*-Kernels oder der GNU-eigene Kernel *Hurd* zum Einsatz kommen.

### GNU/Linux
bezeichnet eine Familie von Betriebssystemen, die einerseits den Linux Kernel und andererseits GNU-Tools nutzen.

### Distribution
Wer Linux nutzt, nutzt meistens eine Linux-Distribution.  
Eine Linux-Distribution ist ein startbares System welches neben den GNU-Tools und dem Linux Kernel noch weitere
Anwendungen und meist auch Tools zur Paketverwaltung mitliefert.  
Bekannte Distributionen sind u.a.: `Ubuntu`, `Debian`, `Fedora`, `Arch`, `Puppy`, `Kali`, `Suse`, `Mint`, `Void`, ...  
Unterschiede zwischen den Distributionen sind unter anderem die mitgelieferte Software, die Paketverwaltung,
die Paketquellen, die Releasemechanik, das "Look-And-Feel", usw.

### Paketmanager
ist ein Werkzeug zur verwaltung Softwarepaketen (Anwendungen, Bibliotheken, ...).  
Sie ermöglichen das *Installieren*, *Deinstallieren* und *Aktualisieren* von Software am System.  
Bekannte Paketmanager sind: `apt`, `dpgk`, `rpm`, `yum`, `xbps`, `pacman`, `portage`, `flatpack`, ...  

### Container
### Desktopumgebung
### Windowmanager
### X (X11, XOrg)
### Wayland
### Root, Superuser
### Terminal
### Shell
### Kommando
Als *Kommando* bezeichnet man "etwas, das man in die Kommandozeile eingeben kann".
Also einen *Befehl* oder eine *Verkettung von Befehlen*.

### Pipe, Redirect, `stdin`, `stdout`, `stderr`

