#!/bin/bash
# Tested on Fedora

sudo dnf install mongodb mongodb-server
systemctl start mongod
systemctl enable mongod
