#!/bin/bash

virtualenv /tmp/test && source /tmp/test/bin/activate
pip install os-testr python-tempestconf
# Source OpenStack creds
source $1
# Run Tempest config
# 1 is flavor ID (openstack flavor list)
python /tmp/test/lib/python2.7/site-packages/config_tempest/config_tempest.py compute.flavor_ref 1
