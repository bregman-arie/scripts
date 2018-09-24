#!/usr/bin/env python
# coding=utf-8

from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client
auth = v3.Password(auth_url='https://my.keystone.com:5000/v3',
                   user_id='myuserid',
                   password='mypassword',
                   project_id='myprojectid')
sess = session.Session(auth=auth)
heat = client.Client('1', session=sess)
heat.stacks.list()
