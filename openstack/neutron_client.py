#!/usr/bin/env python
# coding=utf-8

from keystoneauth1 import loading
from keystoneauth1 import session
from neutronclient.neutron import client

loader = loading.get_plugin_loader('password')
auth = loader.load_from_options(auth_url='',
                                username='',
                                password='',
                                user_domain_name='Default')

sess = session.Session(auth=auth)
nc = client.Client('2.0', session=sess)

for n in nc.network.list():
    print(n)
