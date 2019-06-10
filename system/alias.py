#!/usr/bin/env python

import logging
import os

LOG = logging.getLogger(__name__)

HOME = os.path.expanduser('~')
ALIASES = {
    'd': 'date',
    'dsneutron': 'git clone https://codeng/gerrit/p/neutron.git',
    'g': 'grep -R -i',
    'ga': 'git add',
    'gfa': 'git fetch upstream',
    'gl': 'git log',
    'gri': 'git rebase -i',
    'gs': 'git show',
    'jjbu': 'jenkins-jobs --conf component/config.ini update',
    'nosetests': 'nt',
    'oi-ia': 'git clone https://github.com/openstack-infra/infra-ansible.git',
    'oi-pc': 'git clone https://github.com/openstack-infra/project-config.git',
    'r': 'rsync -azv',
    'tox27': 'tox -e py27',
    'tox8': 'tox -e pep8',
    'usneutron': 'git clone git://git.openstack.org/openstack/neutron.git',
    'v': "virtualenv",
    'pi': "sudo pip install",
    'pu': "sudo pip uninstall",
    'sync': "git pull upstream master && git push origin",
    'unin': "pip uninstall -y ${PWD##*/}  && pip install .",
}


ALIAS_F = {'zsh': HOME + '/.zshrc'}


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
