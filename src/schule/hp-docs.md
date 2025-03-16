---
title: Switch- und Routerdoku
lang: de
keywords:
- tfbs-eke
- informatik
- switch
- router
- hp
- aruba
- labor
- itl
- netzwerktechnik
- lukas singer
description: Doku für HP Switches und Router für netzwerktechnische Laborübungen an der Tiroler Fachberufsschule für Elektrotechnik, Kommunikation und Elektronik
use-toc: true
nav-schule: true
nav-schule-switch-router: true
---

# Über diese Dokumentation

Diese Dokumentation dient dem Laborunterricht an der [Tiroler
Fachberufsschule für Elektrotechnik, Kommunikation und Elektronik
(tfbs-eke)](https://www.eke.at) in den IT-Berufen. Es werden die
wichtigsten (am häufigsten benötigten) CLI-Befehle für die an der Schule
verwendeten Netzwerkgeräte (Switches, Router) kurz und knapp
beschrieben. Diese Dokumentation ersetzt nicht die
Datenblätter/Manuals/Dokumentationen der jeweiligen Netzwerkgeräte.

Diese Dokumentation ist Work-In-Progress und kann (wird!) \"Fehler\"
enthalten und \"unvollständig\" sein.

**Viel Spaß und viel Erfolg bei den Laborübungen!**

## Synopsis

Befehle werden folgendermaßen dargestellt:

``` example
(config)# vlan  VLAN
(vlan-1)# ip address  IP  SNM
```

Am Anfang der Zeile steht immer der für den Befehl (hier: `vlan` bzw.
`ip address`) benötigte Prompt (hier: `(config)#` bzw. `(vlan-1)#`;
möglicherweise muss dazu in den gewünschten Modus/Interface/...
gewechselt werden) gefolgt von Parametern (hier: `VLAN` bzw. `IP  SNM`).

Die Parameter (meist in Großbuchstaben und mit doppelten Leerzeichen
eingefasst) müssen durch die gewünschten \"Werte\" ersetzt werden. Die
tatsächliche Eingabe sieht dann beispielsweise so aus:

``` example
(config)# vlan 1
(vlan-1)# ip address 192.168.42.1 255.255.255.0
```

## Tags (`TBV`, `INC`, `ERR`)

Der Tag **`TBV`** in einer Überschrift steht für `*T*o *B*e *V*erified`
und bedeutet, dass der folgende Abschnitt nicht ausreichend getestet
ist.

Der Tag **`INC`** in einer Überschrift steht für `*Inc*omplete` und
bedeutet, dass der folgende Abschnitt nicht vollständig ist.

Der Tag **`ERR`** in einer Überschrift steht für `*Err*or` und bedeutet,
dass der folgende Abschnitt bekannte Fehler enthält.

## Tabulator `<TAB>` und Fragezeichen `<?>`

Bei der Abreit mit dem **`CLI`** (Command Line Interface) sollte man
sich unbeding angewöhnen viel `TAB` und `?` zu verwenden.

-   `TAB`: vervollständigt einen Bereits teilweise eingegebenen Befehl
    oder schlägt eine Liste an möglichen Vervollständigungen vor.
-   `?`: Listet alle an der aktuellen Curserposition sinnvollen
    Eingebemöglichkeiten auf.

Beispiel:

``` example
(vlan-1)# ip <?>
  access-group          Apply the specified IPv4 ACL on this VLAN interface.
  address               Set IP parameters for communication within an IP 
                        network.
  bootp-gateway         Set the gateway address to be used for stamping incoming
                        DHCP requests.
  helper-address        Add a DHCP server IP address for the VLAN.
  igmp                  Enable/disable/configure IP Multicast Group Protocol 
                        (IGMP) feature on a VLAN.

(vlan-1)# ip ad<TAB>  
(vlan-1)# ip address
```

# CLI-Verbindung herstellen

## Mac OS

### Serielle Verbindung

``` example
$ sudo screen /dev/cu.usbserial-110
```

Zum Lösen (detach) der Verbindung: `Ctrl-a Ctrl-d`

Kann mit `sudo screen -r` wieder aufgebaut (reconnected) werden.

Zum Beenden der Verbindung: `Ctrl-a \`

USB-Seriell-Adapter werden unter Mac OS *typischerweise* als Gerätedatei
`/dev/cu.XXXXXX` dargestellt. Mit dem Befehl `ls /dev/cu.*` werden alle
Gerätedateien aufgelistet, die diesem Muster entsprechen. Die gewünschte
Gerätedatei ist jene, die beim Ein-/Ausstecken des USB-Seriell-Adapters
hinzukommt bzw. wegfällt.

### [TBV] SSH Verbindung

``` example
$ ssh  IP
```

## Linux

### Serielle Verbindung

``` example
$ sudo screen /dev/ttyUSB0
```

Zum Lösen (detach) der Verbindung: `Ctrl-a Ctrl-d`. Diese kann dann mit
`sudo screen -r` wieder aufgebaut (reconnected) werden.

Zum Beenden der Verbindung: `Ctrl-a \`

Möchte man mit dem eigenen User (also nicht als *root* und ohne dem
Befehl `sudo`) eine serielle Verbindung nutzen, kann man den eigenen
User der Gruppe `dialout` hinzufügen:

``` example
$ sudo usermod -aG dialout $USERNAME
```

Nach dem nächsten Login kann die serielle Verbindung ohne `sudo`
geöffnet werden.

### SSH Verbindung

Aufgrund von \"veralteten\" Schlüsselaustausch und
Verschlüsselungsverfahren seitens des Switches funktioniert ein
einfaches

``` example
$ ssh  IP
```

nicht.

Die Lösung sieht dann so, oder so ähnlich aus:

``` example
$ ssh -oKexAlgorithms=+diffie-hellman-group14-sha1 -oHostKeyAlgorithms=ssh-rsa   IP
```

## Windows

### Serielle Verbindung

Am besten mittels [PuTTY](https://putty.org/). Dort \"Serial\"
auswählen, den COM-Port eingeben und \"Open\" klicken.

### [TBV] SSH Verbindung

Entweder mittels [PuTTY](https://putty.org/). Dort \"SSH\" auswählen,
die IP-Adresse des Switches und den Port (standardmäßig: `22`) eingeben
und \"Open\" klicken.

Oder über `cmd` bzw. `PowerShell`:

``` example
C:\> ssh  IP
```

Tritt eine Fehlermeldung bzgl. inkompatibler Schlüsselaustauschverfahren
auf, [kann]{.underline} folgender Befehl helfen:

``` example
C:\> ssh -oKexAlgorithms=+diffie-hellman-group14-sha1 -oHostKeyAlgorithms=ssh-rsa   IP
```

# Switch (HP 2530-24G)

## Zurücksetzen

Vor und nach jeder Laborübung sollten die Switches zurückgesetzt werden,
damit jede:r Schüler:in mit einem *frischen* (unkonfigurierten) Switch
arbeiten kann.

### Löschen der aktuellen Konfiguration

``` example
# erase startup-config
```

### Reset via `Monitor ROM Console`

Serielle Verbindung aufbauen bevor der Switch eingeschaltet
(eingesteckt) wurde. Beim Bootvorgang nach aufforderung
`0. Monitor ROM Console` wählen (\"schnell\" automatisch wird
typischerweise `1. Primary Software Image` nach wenigen Sekunden
ausgewählt).

``` example
=> erase-all
```

Dann bootet der Switch neu und es sollte kein Username/Passwort mehr
gesetzt sein. Nicht wundern, der Reboot dauert etwas länger als gewohnt
(ca. 2 Minuten).

### Hardreset (!)

**Achtung!** Das sollte nur die letzte Möglichkeit sein! Wenn irgendwie
möglich sollten die Switches Softwaremäßig (Löschen der Konfiguration,
Booten der ROM Console, ...) zurückgesetzt werden.

-   `Button RESET` und `Button CLEAR` drücken und gedrückt halten
-   `Button RESET` loslassen (`Button CLEAR` weite halten)
-   sobald `Led TEST` blinkt, kann auch `Button CLEAR` losgelassen werden
-   der Switch rebootet mit Factory Settings

## Modes

``` example
# system-view
(config)#
```

## Default Boot Image wählen

``` example
# boot set-default flash  IMAGE
```

Für `IMAGE` muss `primary` oder `secondary` ausgewählt werden.

## Config File

### Anzeigen

``` example
# display current-configuration
```

### Zurücksetzen

``` example
# erase startup-config
```

### Speichern

``` example
# wr mem
```

### Backup

``` example
# copy startup-config tftp  IP  FILENAME
```

### Restore

``` example
# copy tftp running-config  IP  FILENAME
```

## IP

### Statisch

``` example
(config)# vlan  VLAN
(vlan-1)# ip address  IP  SNM
```

### Dynamisch

``` example
(config)# vlan 1
(vlan-1)# ip dhcp-bootp
```

## SSH Zugang

``` example
(config)# crypto key generate ssh rsa
(config)# ip ssh
(config)# show crypto host-public-key fingerprint
```

## MAC-Address-Table

``` example
# show mac-address
```

## Mirror Port

Einstellen auf welchen Port hin gespiegelt werden soll:

``` example
(config)# mirror-port  PORT
```

Einstellen welcher Port gespiegelt werden soll:

``` example
(config)# interface  INTERFACE
(eth-1)# monitor
```

Beispiel:

``` example
(config)# mirror-port 24
(config)# interface 1
(eth-1)# monitor
```

Durch diese Befehle wird der gesamte Traffic der über den Port `eth-1`
läuft, auch auf Port 24 ausgegeben. Port 24 \"überwacht\" die
Kommunikation von Port 1.

## Spanning Tree

``` example
(config)# spanning-tree enable
```

``` example
(config)# spanning-tree disable
```

``` example
# show spanning-tree
```

# [INC] Router (HP MSR 1003)

## [TBV] Modes

``` example
<> system-view
[]
```

``` example
[] exit
<>
```

## Dateien und Verzeichnise

Aktuelles Verzeichnis anzeigen:

``` example
<> pwd
```

Verzeichnisinhalt anzeigen:

``` example
<> dir
```

Verzeichnis wechseln:

``` example
<> cd  DIRECTORY
```

Neues Verzeichnis erstellen:

``` example
<> mkdir  DIRECTORY
```

Dateien kopieren:

``` example
<> copy  SOURCE-FILENAME  DESTINATION-FILENAME
```

Dateien umbenennen/verschieben:

``` example
<> move  SOURCE-FILENAME  DESTINATION-FILENAME
```

Dateien löschen:

``` example
<> delete  FILENAME
```

Verzeichnise löschen:

``` example
<> rmdir  DIRECTORY
```

## TTL-Expires

``` example
[] ip ttl-expires enable
```

## SSH Zugang

``` example
[] local-user  USERNAME
[USERNAME] password simple  PASSWORD
[USERNAME] authorization-attribute user-role network-admin
[USERNAME] service-type ssh
[USERNAME] exit
[] public-key local create rsa
[] ssh server enable
[] line vty 0 63
[line-vty0-63] authentication-mode scheme
```

Beim Verbinden via PuTTY wird man nach dem `USERNAME` und dem `PASSWORD`
gefragt. Beim Verbinden über eine Shell (*cmd*, *pwsh*, *bash*, ...)
muss man den `USERNAME` gleich mitgeben. Der Befehl lautet dann:
`ssh USERNAME@IP` (Beispiel: `ssh user@192.168.42.254`).

## [TBV] Config File

### Anzeigen

``` example
<> display current-configuration
```

### Zurücksetzen

``` example
<> delete startup.cfg
```

Anschließend muss der Router mittels `<> reboot` neugestartet werden.

**Achtung!** Genau lesen, was man gefragt wird!

### Speichern

``` example
<> write main
```

### Backup

(via TFTP)

``` example
<> backup startup-configuration to  IP  FILENAME
```

## [TBV] Interfaces

Im folgenden ist öfters von `A/B` die rede. Dies sind Platzhalter für
konkrete Interfaces wie beispielsweise `0/1`.

`GigabitEthernet A/B` sollte also durch das gewünschte Interface (zum
Beispiel: `GigabitEthernet 0/1`) ersetzt werden.

### Informationen anzeigen

``` example
[] show interface brief
```

### Mode

``` example
[] interface gigabitethernet A/B
[GigabitEthernetA/B] port link-mode  MODUS
```

Wobei `MODUS` entweder `bridge` oder `route` sein soll.

### IP

``` example
[] interface gigabitethernet A/B
[GigabitEthernetA/B] ip address  IP  SNM
```

## Routing

### Statisch

``` example
[] ip route-static  DESTINATION-NETID  DESTINATION-SNM  NEXTHOP
```

Möchte man einen *Default Gateway* einrichten nimmt man für die
`DESTINATION-NETID` und die `DESTINATION-SNM` jeweils `0.0.0.0`.

Um alle **statischen** Routen auf einmal zu löschen gibt es folgenden
Befehl:

``` example
[] delete static-routes all
```

### Dynamisch

1.  RIPv2

    ``` example
    [] rip
    [rip] version 2
    [rip] network  CONNECTED-NET-ID  CONNECTED-NET-SNM
    [rip] network  CONNECTED-NET-ID  CONNECTED-NET-SNM
          ...
    ```

2.  [TBV] OSPF

    ``` example
    [] router id  ROUTER-ID
    [] ospf
    [ospf] area  AREA-ID
    [ospf-AREA-ID] network  CONNECTED-NET-ID  CONNECTED-SNM
    [ospf-AREA-ID] network  CONNECTED-NET-ID  CONNECTED-SNM
                   ...
    ```

    ``` example
    <> display ospf interface gigabitethernet  A/B
    ```

### Routing Tabelle anzeigen

``` example
[] show ip routing-table
```

## [TBV] NAT, PAT

### 1:1 statisches NAT

``` example
[] nat static outbound  LAN-HOST-IP  WAN-INTERFACE-IP
[] interface  WAN-INTERFACE
[WAN-INTERFACE] nat static enable
```

### Dynamisches NAT

``` example
[] nat address-group 0
[address-group-0] address  LOW-WAN-IP  HIGH-WAN-IP
[address-group-0] exit
[] acl basic 2000
[access-list-2000] rule permit source  LAN-NET-ID  LAN-WILDCARD-MASK
[access-list-2000] exit
[] interface  WAN-INTERFACE
[WAN-INTERFACE] nat outbound 2000 address-group 0
```

### PAT

``` example
[] acl basic 2000
[access-list-2000] rule permit source  LAN-NET-ID  LAN-WILDCARD-MASK
[access-list-2000] exit
[] interface WAN_INTERFACE
[WAN-INTERFACE] nat outbound 2000
```

### Anzeigen, Debugging

``` example
[] display nat all
```

``` example
[] display nat outbound
```

``` example
[] terminal logging level debugging
[] debugging nat packet
[] terminal monitor
```

Zum Stoppen des loggings einfach `no terminal monitor` eingeben.

# Credits

Vielen Dank an alle Kolleg:innen und Schüler:innen die sich bei der
Erstellung und Verbesserung dieser Doku beteiligt haben!

Diese Doku basiert ursprünglich (und zu großen Teilen) auf einer Doku
die von Hansjörg Agerer und seinen Schüler:innen erstellt wurde.

Special Thanks an:

``` example
Hansjörg Agerer
Martin Amann
Alexandra Aurora Göttlicher
Marcel Haidner
Alexander Kircher
Thomas Wolf
Sebastian Kohl
Benjamin Lackner
```
