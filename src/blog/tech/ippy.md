---
title: ippy - IP-Analyse in Python
lang: de
keywords:
- ippy
- ip analyse
- cidr
- itl
- tfbs-eke
- schule
- code
- python
- github
description: ippy ist ein kleines Werkzeug zur Analyse von IP-Adressen, geschrieben in Python, für und mit der Klasse 1APEC 2024/25 an der Tiroler Fachberufsschule für Elektrotechnik, Kommunikation und Elektronik
blog-title: ippy - IP-Analyse in Python
blog-date: 2025-03-31
nav-blog: true
nav-blog-tech: true
blog-changelog:
---

*Heute ging es im IT-Laborunterricht um IP-Adressen, IP-Analyse, CIDR, usw.
kurzerhand haben die Klasse und ich dann ein kleines Tool entwickelt, welches die IP-Analyse für uns durchführt.*

<br>

> **TL;DR**  
> **`ippy`** ist ein kleines Werkzeug zur Analyse von IP-Adressen, geschrieben in Python,
> für und mit der Klasse 1APEC im 3. Lehrgang 2024/25 an der Tiroler Fachberufsschule
> für Elektrotechnik, Kommunikation und Elektronik  
> Sourcecode unter [github.com/eke-singer/ippy](https://github.com/eke-singer/ippy).

<br>

---

## IP-Analyse

Zum Auffrischen bzw. für ein bisschen Kontext:  
Wir analysierten eine IP-Adresse; auf Schüler:innenwunsch hin die von Google.

In die Kommandzeile `nslookup google.com` eingegeben, bekamen wir diese Informationen:

```plain
Server:		192.168.0.1
Address:	192.168.0.1#53

Non-authoritative answer:
Name:	google.com
Address: 142.250.184.196
Name:	google.com
Address: 2a00:1450:4016:809::200e
```

Zusätzlich haben wir noch ein Suffix "erfunden", in diesem Fall $/20$.

| ![Tafelbild zur IP-Analyse](/images/blog/tech/ippy/drawing.webp) |
|:---:|
| <small>Tafelbild zur IP-Analyse von `142.250.184.196 /20`</small> |

---

## Coding Projekt

Das ganze "bitweise UND-Verknüpfen", "invertieren", ... schreit gerade zu danach in einem kleinen
Coding Projekt umgesetzt zu werden.

### Hello World!

Gesagt, getan.
```python
#!/usr/bin/env python3

""" ippy is a small tool to analyze ip adresses
    usage:
        ippy  IP  SUFFIX
"""

if __name__ == '__main__':
    print(__doc__)
```

Schnell ist unser *Hello-World*-artiges Grundgerüst geschrieben von dem aus wir weiter machen können.

> **Warum Hello World?**  
> Mit *Hello World* (oder ähnlich einfachen Programmabläufen) startet jedes Programm.
> Nicht weil man sich als Softwareentwickler davpr fürchtet, gleich komplexeres zu programmieren,
> sondern weil sich dadurch einfach und schnell feststellen lässt, ob die Programmier- und
> Ausführungsumgebung richtig konfiguriert ist.  
> Würde *Hello World* nicht funktionieren, macht es keinen Sinn weiter zu machen, man müsste vorher
> sein Entwicklungssystem "in Ordnung" bringen.

Ausführbar gemacht und ausprobiert:
```plain
$ chmod u+x ippy
$ ./ippy
 ippy is a small tool to analyze ip adresses
    usage:
        ippy  IP  SUFFIX
$
```

Funktioniert, also machen wir weiter.

### Kommandozeilenparameter und Errorcode

Gemeinsam mit den Schüler:innen entsteht die Logik um zwei Argumente von der Kommandozeile einzulesen und gegebenenfalls eine Fehlermeldung auszugeben:
```python
# ...
import sys
# ...
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        exit(1)
    print(f'{sys.argv=}')
```

> Mit `exit(1)` gibt das Programm den ERRORCODE 1 an das Betriebssystem zurück.  
> Üblicherweise bedeutet der ERRORCODE 0, dass das Programm erfolgreich ausgeführt und beendet wurde,
> wohingegen ein ERRORCODE ungleich 0 auf einen Fehler hindeutet. In unserem Fall auf eine ungültige
> Anzahl von Kommandozeilenparametern.  
> Unter Linux und MacOS kann man den ERRORCODE des zuletzt ausgeführten Programms mit `echo $?`,
> unter Windows mit `echo %errorlevel%` einsehen.

Das Programm wird natürlich wieder ausprobiert:
```plain
$ ./ippy test1 test2
sys.argv=['./ippy', 'test1', 'test2']
$ echo $?
0
$ ./ippy
 ippy is a small tool to analyze ip adresses
    usage:
        ippy  IP  SUFFIX
$ echo $?
1
```

Soweit so gut! Als Nächstes müssen wir die Eingaben validieren und in einen geeigneten Datentyp umwandeln.

### IP-Adresse validieren und umwandeln

Für das Einlesen der IP-Adresse haben wir eine Funktion `str_to_ip()` geschrieben,
welche einen String (`str`, Zeichenkette) übernimmt und einen Integer (`int`, Ganzzahl) zurückgibt.

```python
# ...
def str_to_ip(s: str) -> int | None:
    """ check if s is in the form A.B.C.D where A, B, C and D
        are integers greater or equalt to 0 and less than 256.
        if so return them as tuple else returns None """
    parts = s.split('.')
    if len(parts) != 4:
        return None
    if not all(lambda x: x.isnumeric() and (0 <= int(x) < 256) for x in parts):
        return None
    ip = 0
    for part in parts:
        ip <<= 8
        ip |= int(part)
    return ip
# ...
```

Schritt für Schritt:

1. Mit `parts = s.split('.')` teilen wir die Eingabe bei den Punkten auf

1. Mit `if len(parts) != 4: ...` wird geprüft, ob die Eingabe aus vier Elementen bestand,
   wenn das nicht so ist, wird `None` zurückgegeben, um einen Fehler zu signalisieren.

1. `if not all(lambda x: x.isnumeric() and (0 <= int(x) < 256) for x in parts): ...` betrachten wir Schritt für Schritt:

    1. `all( ... for x in parts)` bedeutet, dass wir die folgenden Prüfungen für jeden der 4 Elemente machen,
        die hier `x` genannt werden.

    1. `x.isnumeric()` prüft, ob es sich um eine Zahl handelt.

    1. `(0 <= int(x) < 256)` prüft, ob diese Zahl größer-gleich $0$ und kleiner $256$ ist.

    1. `not` negiert das Ergebnis.  
       Ist also auch nur ein Teil der IP ungültig, gibt die Funktion `None` zurück.

1. `ip = 0` initialisiert eine Integer-Variable.

1. `for part in parts: ...` geht nun alle Teile der IP der Reihe nach durch.  
    In jedem Schritt wird:

    1. Mit `ip <<= 8` der bisherige wert der IP-Adresse um $8$ Bit nach links geshiftet.

    1. Mit `ip |= int(part)` der aktuelle Teil der IP-Adresse durch ODER-Verknüpfung gesetzt.

1. `return ip` gibt die IP-Adresse jetzt als Integer zurück.  


Hier nochmal ein Versuch den Algorithmus darzustellen:
```python
# Angenommen  ip  hat den Wert 42
# Dann sieht  ip  in Binär so aus:
# ip   = 0b_0000_0000__0000_0000__0000_0000__0010_1010
ip <<= 8      # jetzt wird  ip  um 8 Bit nach links geshiftet
# dann sieht  ip  in Binär jetzt so aus:
# ip   = 0b_0000_0000__0000_0000__0010_1010__0000_0000
# Angenommen  part  hat den Wert 23, also
# part = 0b_0000_0000__0000_0000__0000_0000__0001_0111
ip |= part    # jetzt wird  ip  mit  part  ODER-verknüpft
# dann sieht  ip  in Binär jetzt so aus:
# ip   = 0b_0000_0000__0000_0000__0010_1010__0001_0111
```

### Suffix validieren und umwandeln

Dann validieren wir noch das Suffix, wandeln es in einen Integer um und "basteln" auch gleich noch die Subnetzmaske daraus:
```python
# ...
tmp = sys.argv[2] # tmp is easier to type
suffix = int(tmp) if tmp.isnumeric() and (0 < int(tmp) < 32) else None
if suffix is None:
    print("invalid suffix", file=sys.stderr)
    exit(1)
snm = 0x80_00_00_00 # 32nd Bit is 1 all others are 0
for _ in range(suffix - 1):
    snm |= (snm >> 1)
# ...
```

### Die eigentliche IP-Analyselogik (plötzlich ganz simpel!)

Und jetzt nur noch die bereits am Tafelbild gezeigten Regeln anwenden:

```python
netid = ip & snm                       # NetID = IP bitwise-OR Subnetmask
bca = ip | ~snm                        # BCA = IP bitwise-AND inverted Subnetmask
host_range = (netid + 1, bca - 1)      # Hostrange = from (NetID + 1) to (BCA - 1)
host_count = 2 ** (32 - suffix) - 2    # Two less than Two to the power of 32 minus Suffix
```
und Fertig!

Fast.

### IP, NetID, BCA, ... wieder als String darstellen

Die "interne" Darstellung muss für eine sinnvolle Ausgabe natürlich noch in representative Strings
umgewandelt werden:
```python
def ip_to_str(ip: int) -> str:
    """ converts an ip address (int) to its str-representation """
    return '.'.join(
        map(
            str, (
                (ip >> 24) & 0xff,
                (ip >> 16) & 0xff,
                (ip >> 8) & 0xff,
                (ip & 0xff)
            )
        )
    )
```

Hier wird jedes Oktett (8-Bit-Gruppe) in einen String umgewandelt und diese mittels `'.'.join()` durch Punkte verbunden.

`ip_to_str()` kann dann für alle berechneten Adressen (BCA, NetID, SNM, ...) verwendet werden.

---

## Das Fertige Programm

Ich war so frei und hab das Programm nach Unterrichtsende dann noch ein bisschen erweitert.
Man kann sich die Ein- und Ausgaben jetzt auch in Binär bzw. Hexadezimal anzeigen lassen,
außerdem hab ich den Hilfe-Text etwas erweitert, einen Lizenzhinweis hinzugefügt und ein kleines
bisschen aufgeräumt.

> **Disclaimer:**  
> Wie jede Software wird auch diese Software Fehler haben!  
> Vieles lässt sich bestimmt auch besser/anders/eleganter/... lösen, ich habe versucht, einen
> Kommpromiss aus Lesbarkeit, "Eleganz" und "Pythonicität" zu erreichen.

Der aktuelle Code ist unter [github.com/eke-singer/ippy](https://github.com/eke-singer/ippy) auf GitHub zu finden.

Um das Programm ausführen zu können, ist Python3 notwendig.

  - Unter Linux oder MacOS sollte Python bereits installiert
    (oder zumindest in den Paketquellen verfügbar) sein.  
    Zum Ausführen genügt es den Befehl `./ippy` in dem Verzeichnis, in dem der Sourcecode liegt, einzugeben.

  - Unter Windows muss Python wahrscheinlich erst installiert werden.  
    Am besten über die [offizielle Seite](https://www.python.org/).  
    Zum Ausführen muss `ippy` an die `python3.exe` übergeben werden,
    das könnte beisielsweise so `C:\Python3\python3.exe C:\Code\ippy\ippy` aussehen.

### Ein paar Beispiele

Wie sieht das Fertige Programm nun in Action aus?

#### `-h` der Hilfetext

```plain
$ ./ippy -h
ippy is a small python tool to perform ip analysis.
usage:
    ./ippy  [ARG]  IP  SUFFIX

options:
IP       the ip address to analyze in the format
         A.B.C.D where A, B, C and D must be integers
         greater or equalt to 0 and less than 256.

SUFFIX   the cidr suffix for the ip address.
         it must be an integer greater or equal to 0
         and less than 32.

ARG      optional argument(s). can be none, one or more
         of the following:

    -h   prints this help text and exits without error.

    -b   prints ip analysis additionally in binary

    -x   prints ip analysis additionally in hexadecimal

examples:
    ./ippy  192.168.42.23  24

    ./ippy  -b  172.16.31.45  16

license:
    (C) Lukas Singer 2025
    ippy is free open source software provided under WTFPL
    see:  https://www.wtfpl.net/ for details.

ippy was developed by lukas singer on 2025-03-31 for and
with 1APEC 2024/25 @ tfbs-eke.
visit https://www.eke.at and https://www.lukas-singer.eu

```

#### Die IP aus dem Unterrichtsbeispiel

```plain
$ ./ippy 142.250.184.196 20
IP / Suffix = 142.250.184.196 / 20
SNM         = 255.255.240.0
NetID       = 142.250.176.0
BCA         = 142.250.191.255
Host Range  = 142.250.176.1 bis 142.250.191.254
# of Hosts  = 2 ^ (32 - 20) - 2 = 4094
```

#### Ausgabe zusätzlich in Binär

```plain
$ ./ippy -b 192.168.42.23 24
IP / Suffix = 192.168.42.23 / 24
SNM         = 255.255.255.0
NetID       = 192.168.42.0
BCA         = 192.168.42.255
Host Range  = 192.168.42.1 bis 192.168.42.254
# of Hosts  = 2 ^ (32 - 24) - 2 = 254
in binary:
    IP    = 0b11000000.0b10101000.0b00101010.0b00010111
    SNM   = 0b11111111.0b11111111.0b11111111.0b00000000
    NetID = 0b11000000.0b10101000.0b00101010.0b00000000
    BCA   = 0b11000000.0b10101000.0b00101010.0b11111111
```

#### Ausgabe zusätzlich in Hexadezimal

```plain
$ ./ippy -x 10.0.10.5 30
IP / Suffix = 10.0.10.5 / 30
SNM         = 255.255.255.252
NetID       = 10.0.10.4
BCA         = 10.0.10.7
Host Range  = 10.0.10.5 bis 10.0.10.6
# of Hosts  = 2 ^ (32 - 30) - 2 = 2
in hexadecimal:
    IP    = 0x0A.0x00.0x0A.0x05
    SNM   = 0xFF.0xFF.0xFF.0xFC
    NetID = 0x0A.0x00.0x0A.0x04
    BCA   = 0x0A.0x00.0x0A.0x07
```

<br>

---

<br>

<center> **Danke fürs Lesen und viel Spaß mit `ippy`.** </center>

<br>

<center> **Special Thanks an die Schülerinnen und Schüler der Klasse 1 APEC im 3. Lehrgang 2024/25!** </center>

<br>

<br>

---

<small>
Der Quellcode zum Stand 31.3.2025 ist hier:

```python
#!/usr/bin/env python3

"""ippy is a small python tool to perform ip analysis.
usage:
    ./ippy  [ARG]  IP  SUFFIX

options:
IP       the ip address to analyze in the format
         A.B.C.D where A, B, C and D must be integers
         greater or equalt to 0 and less than 256.

SUFFIX   the cidr suffix for the ip address.
         it must be an integer greater or equal to 0
         and less than 32.

ARG      optional argument(s). can be none, one or more
         of the following:

    -h   prints this help text and exits without error.

    -b   prints ip analysis additionally in binary

    -x   prints ip analysis additionally in hexadecimal

examples:
    ./ippy  192.168.42.23  24

    ./ippy  -b  172.16.31.45  16

license:
    (C) Lukas Singer 2025
    ippy is free open source software provided under WTFPL
    see:  https://www.wtfpl.net/ for details.

ippy was developed by lukas singer on 2025-03-31 for and
with 1APEC 2024/25 @ tfbs-eke.
visit https://www.eke.at and https://www.lukas-singer.eu
"""

import sys


def str_to_ip(s: str) -> int | None:
    """ check if s is in the form A.B.C.D where A, B, C and D
        are integers greater or equalt to 0 and less than 256.
        if so return them as tuple else returns None """
    parts = s.split('.')
    if len(parts) != 4:
        return None
    if not all(lambda x: x.isnumeric() and (0 <= int(x) < 256) for x in parts):
        return None
    ip = 0
    for part in parts:
        ip <<= 8
        ip |= int(part)
    return ip


def ip_to_str(ip: int, conv=str) -> str:
    """ converts an ip address (int) to its str-representation """
    return '.'.join(
        map(
            conv, (
                (ip >> 24) & 0xff,
                (ip >> 16) & 0xff,
                (ip >> 8) & 0xff,
                (ip & 0xff)
            )
        )
    )


if __name__ == "__main__":
    if '-h' in sys.argv:
        print(__doc__)
        exit(0)

    print_bin = '-b' in sys.argv
    print_hex = '-x' in sys.argv

    if len(sys.argv) < 3:
        print(__doc__, file=sys.stderr)
        exit(1)

    ip = str_to_ip(sys.argv[-2])
    if ip is None:
        print("invalid IP", file=sys.stderr)
        exit(1)

    tmp = sys.argv[-1]
    suffix = int(tmp) if tmp.isnumeric() and (0 < int(tmp) < 32) else None
    if suffix is None:
        print("invalid suffix", file=sys.stderr)
        exit(1)
    snm = 0x80_00_00_00
    for _ in range(suffix - 1):
        snm |= (snm >> 1)

    netid = ip & snm
    bca = ip | ~snm
    host_range = (netid + 1, bca - 1)
    host_count = 2 ** (32 - suffix) - 2

    print(f"IP / Suffix = {ip_to_str(ip)} / {suffix}")
    print(f"SNM         = {ip_to_str(snm)}")
    print(f"NetID       = {ip_to_str(netid)}")
    print(f"BCA         = {ip_to_str(bca)}")
    print(f"Host Range  = {' bis '.join(map(ip_to_str, host_range))}")
    print(f"# of Hosts  = 2 ^ (32 - {suffix}) - 2 = {host_count}")

    if print_bin:
        print('in binary:')
        def conv(s): return f"0b{s:08b}"
        print(f"    IP    = {ip_to_str(ip, conv)}")
        print(f"    SNM   = {ip_to_str(snm, conv)}")
        print(f"    NetID = {ip_to_str(netid, conv)}")
        print(f"    BCA   = {ip_to_str(bca, conv)}")

    if print_hex:
        print('in hexadecimal:')
        def conv(s): return f"0x{s:02X}"
        print(f"    IP    = {ip_to_str(ip, conv)}")
        print(f"    SNM   = {ip_to_str(snm, conv)}")
        print(f"    NetID = {ip_to_str(netid, conv)}")
        print(f"    BCA   = {ip_to_str(bca, conv)}")
```
</small>

