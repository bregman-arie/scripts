# Copyright 2018 Arie Bregman
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import logging
import sys

OVS_TO_OSP = {'2.9': '13',
              '2': '12',
              'DEFAULT': '11'}


def setup_logging(debug):
    """Sets the logging."""
    format = '%(message)s'
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format=format)


def main():
    """Main App Function."""

    ver = sys.argv[1]
    osp = ''
    while ver != '':
        if ver in OVS_TO_OSP:
            osp = OVS_TO_OSP[ver]
            ver = ''
        ver = ver[:-2]
    if not osp:
        print(OVS_TO_OSP['DEFAULT'])
    print(osp)


if __name__ == '__main__':
    sys.exit(main())
