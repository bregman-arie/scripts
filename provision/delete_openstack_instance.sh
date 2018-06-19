#!/bin/bash

set -e

read -p "How the instance you want to remove is called?: " NAME

# Make sure requirements are installed
if ! hash openstack 2>/dev/null; then
    sudo dnf install python-openstackclient

fi

if [ -z "$OS_AUTH_URL" ]; then
    echo "WARNING: I suspect you didn't source credentials to use OpenStack project"
fi

# Remove instance
openstack server delete $NAME || true

# Remove subnet
openstack subnet delete $NAME || true

# Remove network
openstack network delete $NAME || true
