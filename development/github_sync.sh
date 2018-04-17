#!/bin/bash

git clone git@github.com:bregman-arie/FORKED_REPO.git
cd <FORK>
git remote add upstream git://github.com/ORIGINAL_DEV/ORIGINAL_REPO.git
git fetch upstream
git reset --hard upstream/master
