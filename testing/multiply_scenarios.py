#!/usr/bin/env python
# coding=utf-8

from testscenarios.scenarios import multiply_scenarios

scenarios = multiply_scenarios([('scenario1', dict(param1=1)), ('scenario2', dict(param1=2))],
                               [('scenario2', dict(param2=1))],)
