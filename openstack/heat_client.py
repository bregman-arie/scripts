#!/usr/bin/env python
# coding=utf-8

from keystoneauth1 import loading
from keystoneauth1 import session
from heatclient import client

loader = loading.get_plugin_loader('password')
auth = loader.load_from_options(auth_url='',
                                username='',
                                password='',
                                user_domain_name='Default')

sess = session.Session(auth=auth)
heat = client.Client('1', session=sess)

for h in heat.stacks.list():
    print(h)
