#!/usr/bin/env python

import logging
import os
import re
import subprocess

LOG = logging.getLogger(__name__)

HOME = os.path.expanduser('~')
ALIASES = {
           'dsneutron':
           'git clone https://codeng/gerrit/p/neutron.git',

           'oi-pc':
           'git clone https://github.com/openstack-infra/project-config.git',

           'usneutron':
           'git clone git://git.openstack.org/openstack/neutron.git'
          }

ALIAS_F = {
           'zsh': HOME + '/.zshrc'
          }

def alias_exist(alias_name, alias_f):
    """ Checks if alias already exists in file """
    with open(alias_f, 'r') as f:
        for line in f.readlines():
            if alias_name in line:
                return True
        return False

def get_shell_name():
    """ Retrieve the shell name """
    return os.path.basename(os.environ['SHELL'])

def write_aliases():
    alias_file = ALIAS_F[get_shell_name()]
    with open(alias_file, 'a') as shell_file:
        shell_file.writelines('alias {}="{}"\n'.
                              format(k, v) for k, v in ALIASES.items()
                              if not alias_exist(k, alias_file))

def main():
    write_aliases()

if __name__ == '__main__':
    main()
