#!/usr/bin/env python
# coding=utf-8
import subprocess

# Change that exists

data = subprocess.check_output(
    [
        'ssh',
        '-p',
        '29418',
        'review.openstack.org',
        'gerrit',
        'query',
        'status:open',
        'project:openstack/neutron',
        'limit:5',
        'change:Ib27dc223fcca56030ebb528625cc927fc60553e1',
        '--format JSON'
    ])

listdata = data.split('\n')[:-1][0]
print(listdata)

# Change that doesn't exists

data = subprocess.check_output(
    [
        'ssh',
        '-p',
        '29418',
        'review.openstack.org',
        'gerrit',
        'query',
        'status:open',
        'project:openstack/blabla',
        'limit:5',
        'change:Ib27dc223fcca56030ebb528625cc927fc60553e1',
        '--format JSON'
    ])

listdata = data.split('\n')[:-1][0]
print(listdata)
