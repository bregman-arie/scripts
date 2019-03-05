#!/bin/bash

git clone https://github.com/redhat-openstack/infrared.git
pushd infrared
pipenv install -e .
pipenv shell
popd
