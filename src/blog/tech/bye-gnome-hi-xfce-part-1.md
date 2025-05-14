---
title: Bye Gnome; Hi xfce - Part 1
lang: de
keywords:
- blog
- tech
- Bye Gnome; Hi xfce - Part 1
description: tech - Bye Gnome; Hi xfce - Part 1
blog-title: Bye Gnome; Hi xfce - Part 1
blog-date: 2025-05-14
nav-blog: true
nav-blog-tech: true
blog-changelog:
---

[Zurück zu Part 0](bye-gnome-hi-xfce-part-0.md)

# Das Ziel: `sid`

Mit dem Codenamen `sid` wird die `unstable` (so instabielt soll die scheibar nicht sein; wir werden es sehen)
Version von Debian bezeichnet.  
Während sich die Codenamen der `stable` und `testing` Versionen mit jedem Release ändern,
bleibt der Codename `sid` für `unstable` immer gleich.

Momentan hat Debian `stable` die Version 12 und trägt den Codenamen `bookworm`.
Version 13 wird dann `trixie` heißen, der aktuelle `testing` Release heißt natürlich auch so.
Wenn `trixie` dann als `stable` released wird, dann wird der neue `testing` Release `forky` heißen.  
Nur `sid` bleibt `sid`.  
<small>Wer es genauer wissen möchte, kann [hier](https://www.debian.org/releases/) mehr über Debian Releases nachlesen.</small>

> Die Namen basieren übrigens auf
> [Charakteren aus dem Toy-Story-Universum](https://en.wikipedia.org/wiki/List_of_Toy_Story_characters).

**Es soll also `sid` installiert werden.**

# Das Vorgehen

Um `sid` zu installieren, gibt es mehrere [Möglichkeiten](https://wiki.debian.org/DebianUnstable#Installation).
Ich habe mich (zumindest für meine ersten Tests) für folgende Variante entschieden:

1. Debain `stable` installieren
1. `source.list`s anpassen (`stable` bzw. `bookworm` durch `sid` austauschen
1. mit `apt update` gefolgt von `apt full-upgrade` das System "auf `sid` umstellen"

> Diese Variante ist eine Einbahnstraße, man kann:  
> `bookworm` (`stable`) $\rightarrow$ `trixie` (`testing`) $\rightarrow$ `sid` (`unstable`)  
> oder - wie hier geplant - natürlich direkt: `bookworm` (`stable`) $\rightarrow$ `sid` (`unstable`) upgraden.
>
> `sid` (`unstable`) $\rightarrow$ `trixie` (`testing`) oder gar `sid` (`unstable`) $\rightarrow$ `bookworm` (`stable`)
> funktioniert nicht <small><small>(so einfach)</small></small>!

## Let's go - wir installieren Debian Bookworm mit XFCE

Als Erstes erstellen wir eine "QEMU-Festplatte" mit $20GB$ Speicher, das sollte locker genügen, auch um später ein bisschen Software in der VM zu installieren. Das funktioniert mit folgendem Befehl:

```plain
qemu-img create -f qcow2 debian-vm.qcow2 20G
```

Dann starten wir eine QEMU-VM und geben mit "eingelegtem ISO" - dem Debian Net-Installer. Dazu dient dieser Befehl:

```plain
qemu-system-x86_64 -enable-kvm -m 2048 -smp 2                           \
                   -cdrom "~/Downloads/debian-12.9.0-amd64-netinst.iso" \
                   -drive file=debian-vm.qcow2,format=qcow2             \
                   -boot d -nic user,model=virtio
```

| ![Installer Welcome](/images/blog/tech/bye-gnome-hi-xfce/01-deb-inst-welcome.webp) | ![Sprache Auswählen](/images/blog/tech/bye-gnome-hi-xfce/01-deb-inst-lang.webp) |
|:---:|:---:|
|Hello World! Vom ISO booten und man wird vom Installer Willkommen-geheißen. | Als Erstes können wir die Sprache wählen, ich mags wenn meine Software English spricht. |

<br>

| ![Location 1](/images/blog/tech/bye-gnome-hi-xfce/01-deb-inst-loc-01.webp) | ![Location 2](/images/blog/tech/bye-gnome-hi-xfce/01-deb-inst-loc-02.webp) |
|:---:|:---:|
| Zur Auswahl zum Beispiel der Locale Settings ... | ... oder der Zeitzone ... |

<br>

| ![Location 3](/images/blog/tech/bye-gnome-hi-xfce/01-deb-inst-loc-03.webp) | ![Location 4](/images/blog/tech/bye-gnome-hi-xfce/01-deb-inst-loc-04.webp) |
|:---:|:---:|
| ... sollte man sein geografische Position ... | ... sowie seine geünschte Locale Einstellungenwählen. |

<br>

| ![Keyboard Layout](/images/blog/tech/bye-gnome-hi-xfce/01-deb-inst-kb.webp) | ![Hostname](/images/blog/tech/bye-gnome-hi-xfce/01-deb-inst-hostname.webp) |
|:---:|:---:|
| Ab jetzt braucht man nicht mehr nur `<UP>`, `<DOWN>`, `<TAB>` und `<RETURN>`, somit ist das richtige Keyboardlayout auszuwählen. | Damit kann man dann gleich den Hostanem ... |

<br>

| ![Domainname](/images/blog/tech/bye-gnome-hi-xfce/01-deb-inst-domain.webp) | ![Rootpassword](/images/blog/tech/bye-gnome-hi-xfce/01-deb-inst-rootpassword.webp) |
|:---:|:---:|
| ... und Domänennamen (der hier einfach frei bleibt) vergeben. | Das Rootpasswort. Dazu gibt es ein wichtiges Detail zu wissen. |

<br>

Wird bei der Installation ein Rootpassword vergeben, so kann man sich am System nachher als User `root` anmelden (Login oder `su`),
dafür ist der "haupt Benutzer" dann nicht von vornherein in der Lage den Befehl `sudo` zu nutzen.

Für Desktopsysteme ist es meiner Meinung nach Sinnvoll das Rootpassword einfach leer zu lassen; man sollte ohnehin nicht als `root` arbeiten und `sudo` will und braucht man meistens auch.

<br>

| ![Full Name](/images/blog/tech/bye-gnome-hi-xfce/01-deb-inst-fullname.webp) | ![Username](/images/blog/tech/bye-gnome-hi-xfce/01-deb-inst-user.webp) |
|:---:|:---:|
| Somit gehts ans User-Anlegen. Neben dem vollen Namen ... | ... brauchte der natürlich einen Username. |

<br>

Der Username ist gleichzeitig auch der Verzeichnisname des Heimatverzeichnisses des Users; in meinem Beispiel somit `/home/linluk/`.
Er muss also den Richtlinien für Verzeichnisnamen entsprechen und darf keine Leerzeichen enthalten. Großbuchstaben sind auch unüblich.

<br>

| ![Userpassword](/images/blog/tech/bye-gnome-hi-xfce/01-deb-inst-password.webp) | ![Partitionieren](/images/blog/tech/bye-gnome-hi-xfce/01-deb-inst-part-01.webp) |
|:---:|:---:|
| Als User braucht man natürlich auch ein Passwort!<br>Das sollte auch nicht zu *schwach* sein, schließlich darf dieser User dann als `sudo` damit *alles*. | Kaum ist der User angelegt, geht es auch schon ans Partitionieren ... |

<br>

| ![Partitionieren](/images/blog/tech/bye-gnome-hi-xfce/01-deb-inst-part-02.webp) | ![Partitionieren](/images/blog/tech/bye-gnome-hi-xfce/01-deb-inst-part-03.webp) |
|:---:|:---:|
| Weils für die mein Vorhaben keine große Rolle spielt: *Guided, Entire Disk* (also geführt, gesamte Platte). Diese (gibt eh nur eine) wählt man aus ... | ... und dann belasse ich es hier auch Simpel und lege alles auf eine Partition. |

<br>

| ![Partitionieren](/images/blog/tech/bye-gnome-hi-xfce/01-deb-inst-part-04.webp) | ![Partitionieren](/images/blog/tech/bye-gnome-hi-xfce/01-deb-inst-part-05.webp) |
|:---:|:---:|
| Ein kurzer Kontrollblick obs eh so passt. Ja. | Und das ganze nochmal bestätigen. Fertig Partitioniert. |

<br>

| ![Extra Installation Media](/images/blog/tech/bye-gnome-hi-xfce/01-deb-inst-extra-media.webp) | ![Paketmanager](/images/blog/tech/bye-gnome-hi-xfce/01-deb-inst-apt-01.webp) |
|:---:|:---:|
| Wenn wir noch ein weiteres ISO mit zusätzlichen Paketen hätten, könnten wir das jetzt durchsuchen; hab ich nicht. | Aber dafür starten wir gleich mit der Konfiguration des `APT`, als Erstes werden wir nach unserem bevorzugtem Spiegelserver gefragt ... |

<br>

| ![Paketmanager](/images/blog/tech/bye-gnome-hi-xfce/01-deb-inst-apt-02.webp) | ![Paketmanager](/images/blog/tech/bye-gnome-hi-xfce/01-deb-inst-apt-03.webp) |
|:---:|:---:|
| ... dann auf Basis dessen, nach unserer gewünschten URL ... | ... und (was ich leer lassen kann) nach einem Proxy. |

<br>

| ![Survey](/images/blog/tech/bye-gnome-hi-xfce/01-deb-inst-survey.webp) | ![Software](/images/blog/tech/bye-gnome-hi-xfce/01-deb-inst-software.webp) |
|:---:|:---:|
| Der *Popularity Contest* von Debian ist was tolles[^1], macht für "virtuelle Testsysteme" aber nicht viel Sinn. | Und jetzt gehts endlich drum die **Software auszuwählen** es wird natürlich ***XFCE*** gewählt! |

<br>

| ![Grub](/images/blog/tech/bye-gnome-hi-xfce/01-deb-inst-grub-01.webp) | ![Grub](/images/blog/tech/bye-gnome-hi-xfce/01-deb-inst-grub-02.webp) |
|:---:|:---:|
| Nach kurzer Wartezeit sind wir jetzt so gut wie am Ende. Der Installer möchte noch wissen ob und wohin der Bootloader installiert werden soll. Erstens: ja. | Zweitens: hierhin |

<br>

| ![Reboot](/images/blog/tech/bye-gnome-hi-xfce/01-deb-inst-reboot.webp) | ![Grub](/images/blog/tech/bye-gnome-hi-xfce/01-deb-reboot.webp) |
|:---:|:---:|
| Ein Neustart und ... | ... man wird von GRUB zum ersten booten eines ganz frisch installiertem Systems begrüßt. |

Somit ist die Installation abgeschlossen.

Mit dem Befehl:
```plain
qemu-system-x86_64 -enable-kvm                              \
                   -m 2048                                  \
                   -smp 2                                   \
                   -drive file=debian-vm.qcow2,format=qcow2 \
                   -nic user,model=virtio
```
lässt sich das virtuelle System nun einfach starten.

| ![XFCE Desktop in Bookworm](/images/blog/tech/bye-gnome-hi-xfce/01-deb-desktop.webp) |
|:---:|
| Hello XFCE! <br><small>Sorry, aber so siehst du nicht besonders toll aus.</small> |

<br>

Wir haben nun ein frisch installiertes Debian System vor uns, allerdings *noch* mit Debian *stable*. Wir möchten jedoch **`unstable`** also **`sid`**.

## Aus `Bookworm` werde `sid`



| ![sudoedit sources.list](/images/blog/tech/bye-gnome-hi-xfce/01-deb-sources-list-01.webp) | ![Die alte sources.list](/images/blog/tech/bye-gnome-hi-xfce/01-deb-sources-list-02.webp) |
|:---:|:---:|
| Mit `sudoedit` (nicht `sudo vim`, `sudo nano`, ...!) öffnen wir die `sources.list` ... | ... welche nach unserer Installation so aussieht. |

<br>

| ![Die neue sources.list](/images/blog/tech/bye-gnome-hi-xfce/01-deb-sources-list-03.webp) | ![apt update](/images/blog/tech/bye-gnome-hi-xfce/01-deb-apt-update.webp) |
|:---:|:---:|
| Die Paketquellen werden folgendermaßen angepasst und ... | ... mittels `sudo apt update` aktualisiert. |

<br>

| ![apt full-upgrade](/images/blog/tech/bye-gnome-hi-xfce/01-deb-apt-full-upgrade.webp) | ![neowofetch](/images/blog/tech/bye-gnome-hi-xfce/01-deb-neowofetch.webp) |
|:---:|:---:|
| Mit `sudo apt full-upgrade` (nicht wie bei einem "normalen" *upgrade* mit `sudo apt upgrade`) wird aus **`bookworm`** nun endlich **`sid`**. | Hier der Beweis ;-) |


# End-Of-Part-1

In Part 1 der Reihe haben wir das für das Experiment nötige System **`Debian sid/unstable`** aufgesetzt.

Im nächsten Teil wird es dann um ein paar "aufhübschungen" gehen, so dass das System ein bisschen netter aussieht und sich effizient bedienen lässt (Shortcuts usw.).

<br>

See ya.


<br>

<br>

[Zurück zu Part 0](bye-gnome-hi-xfce-part-0.md)

<br>

[^1]: https://popcon.debian.org/
