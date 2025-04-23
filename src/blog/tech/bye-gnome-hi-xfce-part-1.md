---
title: Bye Gnome; Hi xfce - Part 1
lang: de
keywords:
- blog
- tech
- Bye Gnome; Hi xfce - Part 1
description: tech - Bye Gnome; Hi xfce - Part 1
blog-title: Bye Gnome; Hi xfce - Part 1
blog-date: 2025-04-22
nav-blog: true
nav-blog-tech: true
blog-changelog:
---

Hier den Blogeintrag schreiben ...
Und nicht vergessen, den YAML Header anzupassen!









### NOTES AND COMMANDS

```
qemu-img create -f qcow2 debian-vm.qcow2 20G
qemu-system-x86_64 -enable-kvm -m 2048 -smp 2 -cdrom "~/Downloads/debian-12.9.0-amd64-netinst.iso" -drive file=debian-vm.qcow2,format=qcow2 -boot d -nic user,model=virtio
qemu-system-x86_64 -enable-kvm -m 2048 -smp 2 -drive file=debian-vm.qcow2,format=qcow2 -nic user,model=virtio
