---
title: Bye Gnome, Hi xfce - Part 0
lang: de
keywords:
- blog
- tech
- gnome
- xfce
- x11
- wayland
- debian
- linux
description: tech - Bye Gnome, Hi xfce - Part 0
blog-title: Bye Gnome, Hi xfce - Part 0
blog-date: 2025-04-21
nav-blog: true
nav-blog-tech: true
blog-changelog:
---

> Ich mag [Gnome](https://www.gnome.org/) und bin wirklich sehr zufrieden damit!  
> `Super Key` $+$ *drauf-los tippen*, `Ctrl-Meta-Left`/`Ctrl-Meta-Right` zum super schnellen wechseln zwischen Desktops ist genial.
> Die mitgelieferten Tools, allen voran der Mail-Client *Evolution*, das *Gnome-Terminal* und der PDF-Viewer *Evince* sind großartige,
> Programme, die sich sehr stabil anfühlen und mich über die letzten Jahre so gut wie nie im Stich gelassen haben.

Und Trotzdem!

Hin und wieder muss man sich was Neues (oder anderes ansehen), nicht weil das Gras auf der anderen Seite grüner zu sein scheint,
sondern weil Routine und praktisches und gewohntes und und und ... auch manchmal ein bisschen Betriebsblind werden lässt.

## Von `vim` über `Emacs` zu `Neovim`

<small>
*Das wäre eigentlich einen eigenen Blogbeitrag wert, deswegen hier nur kurz für ein paar Gedanken und vielleicht irgendwann mal ausführlich.*  
<small>Wenn ich dran denke, dann wir dieser *Vielleicht-Irgendwann-Beitrag* HIER verlinkt!</small>
</small>

Vor ca. zwei Jahren hab ich beschloßen meinen wunderbaren Editor [`vim`](https://www.vim.org/) (inkl. meiner liebevoll zusammengestellten,
ca. 2000 Zeilen langen `vimrc`-Konfiguration) hinter mir zu lassen und [`Emacs`](https://www.gnu.org/software/emacs/) "auszuprobieren".  
Wer solche Editoren kennt, weiß, dass sie anfangs nicht einfach zu bedienen sind, nicht in einer, zwei oder drei Wochen einfach so nebenbei
erlernt werden können *aber auch*, dass man damit unglaublich produktiv sein kann, dass sie bei Programmierne, beim Schreiben, beim Konfigurieren, ...
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


## Ausprobieren! Aber wie?

Oh, ich nutze ja `Debian` (und dabei bleibe ich auch!).  
Momentan `Debian bookworm` aka `Debian 12` aka `Debian stable`. Das `stable` bedeutet bei `Debian`, dass es sehr (sehr!) stabil ist.  
Un das bedeutet, dass es kaum neue Softwarepakete gibt, außer Sicherheitsupdates natürlich.

Für mein Vorhaben sehe ich daher zwei Varianten.

1. **Selbst Kompilieren:** Das mache ich bei "kleinerer" Software, entweder aus interesse oder weil ich sie bleeding-edge-aktuell haben will so.
2. **Debian unstable:** `unstable`? klingt wild! Ist es das? scheinbar nicht, ... vielleicht doch?

Selbst kompilieren ist mir bei einer Software, die ich (noch nicht) nutze und (noch nicht) so gut kenne und die einen so essenziellen Teil meiner Arbeitsumgebung ausmacht irgendwie zu heikel. <small>(Ohne da jetzt genauer drüber nachgedacht zu haben)</small>

Mit `unstable` (diese Variante heißt, wie alle `Debian`-Versionen nach einem Toy Story Charakter), liebevoll auch `sid` genannt habe ich (noch) wenig erfahrung, vorallem als daily-driver.

Jetzt wird erstmal eine [QEMU](https://www.qemu.org/)-Umgebung aufgesetzt, `Debian sid` mit `xfce` installiert und diese dann verwendet.

<div class="img-max-width-800">
| ![xfce mit ersten tweaks in QEMU](/images/blog/tech/bye-gnome-hi-xfce/xfce01.webp) |
|:---:|
| xfce mit ersten tweaks in QEMU |
</div>

## End-Of-Part-0

Der Part 0 dieser Reihe ist jetzt schon mal ziemlich unstrukturiert geworden.

Es geht in erster Linie darum warum man (in dem Fall ich) einfach ab-und-zu neue Software ausprobieren sollte und wie ich das vorhabe zu tun.


