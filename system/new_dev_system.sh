#!/bin/bash
# CentOS 8

set -eux

dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
sudo dnf install -y virtualenv git gcc git docker-ce
git clone https://github.com/bregman-arie/infraform.git
systemctl start docker
systemctl enable docker
firewall-cmd --zone=public --add-port=8080/tcp
firewall-cmd --zone=public --add-masquerade --permanent
sudo firewall-cmd --reload
