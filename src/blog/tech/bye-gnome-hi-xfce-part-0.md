---
title: Bye Gnome; Hi xfce - Part 0
lang: de
keywords:
- blog
- tech
- gnome
- xfce
- x11
- wayland
- qemu
- debian
- sid/unstable
- linux
description: tech - Bye Gnome; Hi xfce - Part 0
blog-title: Bye Gnome; Hi xfce - Part 0
blog-date: 2025-04-22
nav-blog: true
nav-blog-tech: true
blog-changelog:
---

**TL;DR:**  
Um mal wieder was Neues auszuprobieren, möchte ich von `Gnome` auf `xfce` wechseln. Auf `xfce 4.20`, das gibts erst in Debian Testing bzw. Debian Sid (unstable).  
Also mein Plan: Debian Sid in QEMU mit xfce ausprobieren.

<br>

> Ich mag [Gnome](https://www.gnome.org/) und bin wirklich sehr zufrieden damit!  
> `Super Key` $+$ *drauf-los tippen*, `Ctrl-Meta-Left`/`Ctrl-Meta-Right` zum super schnellen wechseln zwischen Desktops ist genial.
> Die mitgelieferten Tools, allen voran der Mail-Client *Evolution*, das *Gnome-Terminal* und der PDF-Viewer *Evince* sind großartige,
> Programme, die sich sehr stabil anfühlen und mich über die letzten Jahre so gut wie nie im Stich gelassen haben.

Und Trotzdem!

Hin und wieder muss man sich was Neues (oder anderes ansehen), nicht weil das Gras auf der anderen Seite grüner zu sein scheint,
sondern weil Routine und praktisches und gewohntes und und und ... auch manchmal ein bisschen Betriebsblind werden lässt.

<br>

## Von `vim` über `Emacs` zu `Neovim`

<small>
*Das wäre eigentlich einen eigenen Blogbeitrag wert, deswegen hier nur kurz für ein paar Gedanken und vielleicht irgendwann mal ausführlich.*  
<small>Wenn ich dran denke, dann wir dieser *Vielleicht-Irgendwann-Beitrag* HIER verlinkt!</small>
</small>

Vor ca. zwei Jahren hab ich beschlossen meinen wunderbaren Editor [`vim`](https://www.vim.org/) (inkl. meiner liebevoll zusammengestellten,
ca. 2000 Zeilen langen `vimrc`-Konfiguration) hinter mir zu lassen und [`Emacs`](https://www.gnu.org/software/emacs/) "auszuprobieren".  
Wer solche Editoren kennt, weiß, dass sie anfangs nicht einfach zu bedienen sind, nicht in einer, zwei oder drei Wochen einfach so nebenbei
erlernt werden können *aber auch*, dass man damit unglaublich produktiv sein kann, dass sie bei Programmieren, beim Schreiben, beim Konfigurieren, ...
einfach geniale Helfer sind.  

Ich war mit `vim` auch sehr zufrieden.  
Ich war mit `vim` auch sehr produktiv.  
Mit `Emacs` war ich anfangs nicht (und ich meine **überhaupt nicht!**) produktiv.

Aber.

`Emacs` und das ganze Rundherum (vorallem [Org-Mode](https://orgmode.org/)) hat mir viele neue Denkanstöße und Arbeitsweisen aufgezeigt,
die ich heute in angepasster Form in [`Neovim`](https://neovim.io/) nutze und die ich in meinem Workflow nicht mehr missen möchte.

> Nach mehr als 10 Jahren `vim` hat mir ein Jahr `Emacs` sehr viel gebracht und eingerostete "das-hab-ich-immer-schon-so-gemacht"-Workflows aufgelöst.

Heute nutze ich `Neovim` (btw.).


## Zurück zu Desktopenvironments

<div class="img-max-width-800">
| ![Gnome Applications and Desktop Switcher](/images/blog/tech/bye-gnome-hi-xfce/gnome01.webp) |
|:---:|
| Gnome Applications and Desktop Switcher |
</div>

`Gnome` vs. `KDE` vs. `Cinnamon` vs. `MATE` vs. `LXDE` vs. ...
Desktopumgebungen haben auf den ersten Blick mindestens gleichviel "Glaubenskriegspotential" wie Editoren (vgl. ["Editor war"](https://en.wikipedia.org/wiki/Editor_war)).  
Der erste Blick täuscht hier auch nicht `;-)`  
Niemals würde ich `KDE` probieren `:-P`  

Aber **[`xfce`](https://xfce.org/)**?  
**Klar!**

Wäre nicht das erste Mal.

Zugegeben, `xfce` war in der Vergangenheit nicht immer die *fancyeste* Desktopumgebung.

Für richtig schwache System sind die noch ressourcenschonenderen [`LXDE`](https://www.lxde.org/) bzw. [`LXQt`](https://lxqt-project.org/) für mich die bessere Wahl.

`xfce` hat somit eine undankbare Position zwischen den "Großen und Schönen" (`Gnome`, `KDE`, `Cinnamon`, ...) und den "Kleinen und Schwachen" (`LXDE`, `LXQt`, ...).

Der neue Release [xfce 4.20](https://alexxcons.github.io/blogpost_14.html) rückte das System wieder mehr in meinen Fokus.

`xfce` ist "immer noch nicht" Wayland-ready. Ich nutze jetzt Wayland schon seit einiger Zeit, muss aber gestehen, dass ich mich weder mit X11 noch mit Wayland wirklich auseinandergesetzt habe. Beides hat für mich einfach immer funktioniert.

Jetzt bin ich gespannt, ob ich beim Wechsel-zurück also von Wayland zu X11 irgendwas bemerke.


## Ausprobieren! Aber wie?

Oh, ich nutze ja `Debian` (und dabei bleibe ich auch!).  
Momentan `Debian bookworm` aka `Debian 12` aka `Debian stable`. Das `stable` bedeutet bei `Debian`, dass es sehr (sehr!) stabil ist.  
Un das bedeutet, dass es kaum neue Softwarepakete gibt, außer Sicherheitsupdates natürlich.

Für mein Vorhaben sehe ich daher zwei Varianten.

1. **Selbst Kompilieren:** Das mache ich bei "kleinerer" Software, entweder aus Interesse oder weil ich sie bleeding-edge-aktuell haben will so.
2. **Debian unstable:** `unstable`? klingt wild! Ist es das? scheinbar nicht, ... vielleicht doch?

Selbst kompilieren ist mir bei einer Software, die ich (noch nicht) nutze und (noch nicht) so gut kenne und die einen so essenziellen Teil meiner Arbeitsumgebung ausmacht irgendwie zu heikel. <small>(Ohne da jetzt genauer drüber nachgedacht zu haben)</small>

Mit `unstable` (diese Variante heißt, wie alle `Debian`-Versionen nach einem Toy Story Charakter), liebevoll auch `sid` genannt habe ich (noch) wenig Erfahrung, vorallem als daily-driver.

Jetzt wird erstmal eine [QEMU](https://www.qemu.org/)-Umgebung aufgesetzt, `Debian sid` mit `xfce` installiert und diese dann verwendet.

<div class="img-max-width-800">
| ![xfce mit ersten tweaks in QEMU](/images/blog/tech/bye-gnome-hi-xfce/xfce01.webp) |
|:---:|
| xfce mit ersten tweaks in QEMU |
</div>


## Ausprobieren. Gut, aber was muss funktionieren, was wird "getestet"?

Mein *Workflow* soll produktiv bleiben, dazu gehört:

* `Super` $+$ *drauf-los-tippen* sollte funktionieren, um Anwendungen zu finden und zu starten
* mehrere Arbeitsflächen
* meine Terminal-Tools und Konfigurationen (u.a.: [`.bashrc.d`](https://github.com/linluk/.bashrc.d)) sollen funktionieren (`Neovim`, `Bash`, `tmux`, `Newsboat`, ...)
* Beamer und zweiter Monitor muss problemlos funktionieren
* `Xournalpp` und mein Wacom-Tablet muss problemlos funktionieren.
* Die Maus soll für (so gut wie) nichts nötig sein

Außerdem muss sich alles flott und "snappy" anfühlen (da bin ich guter Dinge, mir kommt `Gnome` jetzt ja auch nicht langsam vor).

Ein zwei größere Updates sollten eventuell gemacht werden um die Stabilität von `sid` zu "testen".

Ein bisschen was von der [debian-devel-announce E-Mail-Liste](https://lists.debian.org/debian-devel-announce/) (mit)lesen, das wird für `sid`-User empfohlen. Und natürlich hinterfragen, wie das mit Paketupdates zusammenhängt.

Customizen, customizen, customizen, ... damit mein ich jetzt nicht ein neues [r/unixporn](https://www.reddit.com/r/unixporn/)-Highlight zu schaffen, sondern viel mehr herauszufinden wie und was man alles so machen kann.
Und es wär ja nicht schlecht, wenns gut aussieht.

`CapsLock` als zweite `Escape`-Taste mappen! (Das war mit `Gnome` total simpel mit dem `Gnome Tweak Tool`)


## End-Of-Part-0

Der Part 0 dieser Reihe ist jetzt schon mal ziemlich unstrukturiert geworden.

Es geht in erster Linie darum warum man (in dem Fall ich) einfach ab-und-zu neue Software ausprobieren sollte und wie ich das vorhabe zu tun.

Im nächsten Teil wirds dann um das Einrichten einer QEMU-VM, die Intallation und das Upgrade auf `sid` gehen.

<br>
