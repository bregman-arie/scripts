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
from bs4 import BeautifulSoup
import logging
import sys
import re
import urllib2


def setup_logging(debug):
    """Sets the logging."""
    format = '%(message)s'
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format=format)


def main():
    """Main App Function."""

    url = 'http://pulp.dist.stage.ext.phx2.redhat.com/content/dist/rhel/server/7/7Server/x86_64/fast-datapath/os/Packages/?C=M;O=A'
    resp = urllib2.urlopen(url)
    soup = BeautifulSoup(resp, "lxml", from_encoding=resp.info().getparam('charset'))
    found = False

    while not found:
        for link in soup.find_all('a', href=True):
            rpm = link['href']
            name = re.search(r'(^[a-zA-z0-9\-]*)\-\d', rpm)
            if name:
                if name.group(1) == 'openvswitch':
                    print(link['href'])
                    found = True
                    break


if __name__ == '__main__':
    sys.exit(main())
