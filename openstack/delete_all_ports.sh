#!/bin/bash
for PORT_ID in `openstack port list -f csv -c ID | tail -n +2 | tr -d '"' `; do
    openstack port delete $PORT_ID
done
