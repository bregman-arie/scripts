#!/usr/bin/env python
# coding=utf-8
import argparse
import logging
from pygerrit.rest import GerritRestAPI
import subprocess
import tempfile

US_GERRIT_URL = "https://review.openstack.org"
DS_GERRIT_URL = "<INTERNAL_GERRIT_URL>"
RELEASE_MAP = {'pike': '12',
               'ocata': '11',
               'newton': '10',
               'mitaka': '9',
               'liberty': '8',
               'kilo': '7',
               }

LOG = logging.getLogger(__name__)


def create_parser():
    """Returns ArgumentParser instance with arguments"""

    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument('--patch',
                        '-p',
                        dest='patch',
                        required=True,
                        help="Patch number")

    parser.add_argument('--debug',
                        action='store_true',
                        dest="debug",
                        help='Turn on debug')

    return parser


def setup_logging(debug):
    """Setup logging level and format."""

    format = '%(levelname)s: %(name)s | %(message)s'
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format=format)


def get_project_and_release(patch_num):
    """Returns downstream & upstream branch and project based on given

    upstream change.
    """
    rest = GerritRestAPI(url=US_GERRIT_URL, auth=None)
    change = rest.get("/changes/?q=change:%s" % patch_num)
    us_branch = change[0]['branch'].split('/')[1]
    project = change[0]['project'].split('/')[1]
    logging.info("Detected project: %s, branch: %s" % (project, us_branch))

    return project, "rhos-%s.0-patches" % RELEASE_MAP[us_branch], us_branch


def cherry_pick_ds(project, branch, patch_num):
    """Clones downstream project and cherry-picks the change from upstream."""
    tmpdir = tempfile.mkdtemp(dir='/tmp')
    logging.info("Cloning %s from downstream gerrit to %s" % (project, tmpdir))
    subprocess.call("git clone %s/%s.git" % (DS_GERRIT_URL, project),
                    shell=True,
                    cwd=tmpdir)
    logging.info("Checking out %s" % branch)
    subprocess.call("git checkout origin/%s" % branch, shell=True,
                    cwd=(tmpdir + "/" + project))
    subprocess.call("git remote add upstream https://review.openstack.org/openstack/%s.git" % project, shell=True, cwd=(tmpdir + '/' + project))
    subprocess.call("git-review -r upstream -x %s" % patch_num, shell=True,
                    cwd=(tmpdir + '/' + project))


def main():
    # Create argument parser
    parser = create_parser()
    args = parser.parse_args()

    # Setup logging to appropriate format and level
    setup_logging(args.debug)

    project, branch, us_branch = get_project_and_release(args.patch)
    logging.info("Downstream project: %s, branch: %s" % (project, branch))

    cherry_pick_ds(project, branch, args.patch)
    logging.info("Done cherry-picking. Remember to add the following lines to\
the commit message:")
    logging.info("Upstream-%s: https://review.openstack.org/#/c/%s" % (
        us_branch, args.patch))
    logging.info("Related-rhbz: <bug_number>")


if __name__ == '__main__':
    main()
