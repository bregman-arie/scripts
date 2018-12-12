#!/usr/bin/env python
# coding=utf-8

from collections import namedtuple
from ansible.executor import playbook_executor
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager

loader = DataLoader()
inventory = InventoryManager(loader=loader, sources='localhost,')

extra_vars = {'name': 'create'}
variable_manager = VariableManager(loader=loader, inventory=inventory)
variable_manager.extra_vars = extra_vars

Options = namedtuple('Options', ['connection', 'module_path',
                                 'forks', 'become', 'become_method',
                                 'become_user', 'check', 'diff', 'listhosts',
                                 'listtasks', 'listtags', 'syntax'])

options = Options(connection='local', module_path=['/to/mymodules'],
                  forks=10, become=None, become_method=None,
                  become_user=None, check=False, diff=False, listhosts=False,
                  listtasks=False, listtags=False, syntax=False)

passwords = dict(vault_pass='secret')

pb_executor = playbook_executor.PlaybookExecutor(
    playbooks=['test.yaml'],
    inventory=inventory,
    variable_manager=variable_manager,
    loader=loader,
    options=options,
    passwords=passwords)

pb_executor.run()
