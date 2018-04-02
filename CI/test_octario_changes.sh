#!/bin/bash

infrared plugin remove octario
sed -i '/octario/,+4 d' $ir_venv/lib/python2.7/site-packages/infrared/__init__.py
rm -rf plugins/octario
git clone https://github.com/redhat-openstack/octario.git
pushd octario
git fetch https://review.gerrithub.io/redhat-openstack/octario refs/changes/47/404147/10 && git cherry-pick FETCH_HEAD
popd
infrared plugin add octario
