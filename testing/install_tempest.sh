#!/bin/bash

virtualenv /tmp/test && source /tmp/test/bin/activate
pip install os-testr python-tempestconf
# Source OpenStack creds
source $1
# Run Tempest config
# 1 is flavor ID (openstack flavor list)
# image_ref and image_ref_alt is the ID of cirros image
python ~/tobiko_venv/lib/python2.7/site-packages/config_tempest/config_tempest.py compute.flavor_ref 1 scenario.img_dir '/tmp' compute.image_ref 262bd1d3-9e57-4795-9b77-d35a0e39c78f compute.image_ref_alt 262bd1d3-9e57-4795-9b77-d35a0e39c78f
mkdir etc
# Put pass in volume and ceilometer methods
# Remove tempest tests
tempest run --config-file etc/tempest.conf --regex tobiko
