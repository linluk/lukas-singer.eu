---
title: CPT unter Linux
lang: de
description: Cisco Packet Tracer unter Linux installieren
nav-blog: true
blog-title: CPT unter Linux
blog-date: 2025-03-17
blog-changelog:
---

CPT unter Linux
===============

Der **Cisco Packet Tracer** (kurz: CPT) funktioniert auch unter Linux!

Zumindest auf (halbweg aktuellen) Debian-basierten Distributionen.
Mit ein bisschen bastelei, bekommt man es aber auf anderen Distros bestimmt auch hin.

Ich habe es auf meinem Debian System getestet.

<small>Hier ein paar Details dazu:
```sh
$ lsb_release -d -s
Debian GNU/Linux 12 (bookworm)
$ uname -r -s
Linux 6.1.0-32-amd64
```
</small>

Nachdem man sich einen NatAcad (Cisco Networking Academy) Account erstellt hat bietet Cisco ein DEB-Paket zum Download an.
Stand heute (das ändert sich bei Cisco leider immer wieder) ist es
[hier](https://www.netacad.com/resources/lab-downloads?courseLang=en-US) zu finden und heißt:
*Packet Tracer 8.2.2 Ubuntu 64bit*.

Angenommen es gibt nach dem Download eine Datei namens `~/Downloads/Packet_Tracer822_amd64_signed.deb`,
dann kann diese mit folgendem Befehl installiert werden:

```sh
sudo apt install ~/Downloads/Packet_Tracer822_amd64_signed.deb
```
Wenn alles geklappt hat, dann lässt sich der CPT nun in den Anwendungen finden und starten.
Alternativ natürlich auch über die Kommandozeile hierfür einfach `packettracer` eingeben.




