#!/bin/bash

git remote add upstream https://review.openstack.org/openstack/<project>.git
git fetch --tags upstream
git remote add rhos ssh://abregman@<internal_git>:22/<project>
git push --tags rhos
