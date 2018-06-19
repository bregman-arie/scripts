#!/bin/bash

set -e

FLAVOR="m1.small"
IMAGE="rhel-7.5-server-x86_64-latest"
read -p "How do you want to call the machine and all other related resources?: " NAME

# Make sure requirements are installed
if ! hash openstack 2>/dev/null; then
    sudo dnf install python-openstackclient

fi

if [ -z "$OS_AUTH_URL" ]; then
    echo "WARNING: I suspect you didn't source credentials to use OpenStack project"
fi

# Create network
openstack network create \
    $NAME || true

# Create subnet
openstack subnet create \
    --network $NAME \
    --subnet-range 10.0.0.0/24 \
    $NAME

# Create Instance
openstack server create \
    --flavor $FLAVOR \
    --image  $IMAGE \
    --network $NAME \
    $NAME
