#!/usr/bin/env python
# coding=utf-8

import argparse
import subprocess


def create_parser():
    """Returns argument parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', required=True)
    return parser


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    # Establish a tunnel
    subprocess.call("ssh -f -L 1990:localhost:27017 root@{} sleep 22".format(args.host),
                    shell=True)
    # Dump the database from the remote host
    subprocess.call("mongodump --forceTableScan --host localhost:1990", shell=True)
    # Restore the database on your localhost
    subprocess.call("mongorestore --drop --host localhost:27017", shell=True)
