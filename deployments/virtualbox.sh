#!/bin/bash
# Install VirtualBox
# Tested on: Fedora 28

sudo dnf update -y
sudo dnf install -y binutils gcc make patch libgomp glibc-headers glibc-devel kernel-headers kernel-devel dkms
sudo dnf install -y VirtualBox-5.2
sudo /usr/lib/virtualbox/vboxdrv.sh setup

echo "Done. I recommend to reboot"
