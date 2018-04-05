# Copyright 2016 Arie Bregman
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# NOTES
# -----
# 1. This script is dowmloading a specific image. You should check if it's the
#    latest image used for installing SF.
# 2. This deployment is done on OpenStack

import argparse
import logging
import os
import shade
import wget

logging.basicConfig(level=logging.INFO, format='%(message)s')


def retrieve_image(cloud, image_url):
    """Downloads Software factory image."""
    image_name = image_url.rsplit('/', 1)[-1]
    if (not os.path.exists(os.getcwd() + '/' + image_name) and
        not cloud.get_image(image_name)):
        logging.info("== Downloading software factory image ==")
        wget.download(image_url)
    else:
        logging.info("Image already exists...skipping image download")

    return image_name


def upload_image(cloud, img_name):
    if cloud.get_image(img_name):
        logging.info("Image already exists in the cloud...skipping uploading")
    else:
        logging.info("== Uploading the image ==")
        cloud.create_image(img_name, filename=img_name, wait=True)

    return cloud.get_image(img_name)['id']


def retrieve_heat_template(template_url):
    '''Returns the name of the heat template'''
    template_name = template_url.rsplit('/', 1)[-1]

    if not os.path.exists(os.getcwd() + '/' + template_name):
        logging.info("== Downloading heat template ==")
        wget.download(template_url)
    else:
        logging.info(
            "Heat template already exists...skipping template download")

    return template_name


def get_network_id(cloud, external_network):
    """Returns external network id."""
    return cloud.get_network(external_network)['id']


def create_sf_heat_stack(cloud, stack_name, template_name,
                         key, img_id, external_net):
    logging.info("== Creating stack! This might take couple of minutes... ==")
    cloud.create_stack(stack_name, template_file=template_name,
                       wait=True, key_name=key, image_id=img_id,
                       ext_net_uuid=external_net)
    logging.info("== Done! You can start using Software Factory ==")


def create_parser():
    """Returns argument parser."""

    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument('--key', required=False, dest="key_name",
                        default='rhos-jenkins', help="Key name in the cloud")
    parser.add_argument('--cloud', required=True, dest="cloud",
                        default='qeos', help="OpenStack cloud name")
    parser.add_argument('--image_url', required=False, dest="image_url",
                        default='http://46.231.132.68:8080/v1/AUTH_b50e80d3969f441a8b7b1fe831003e0a/sf-images/softwarefactory-C7.0-2.2.3.img.qcow2')
    parser.add_argument('--template_url', required=False, dest="template_url",
                        default='http://46.231.132.68:8080/v1/AUTH_b50e80d3969f441a8b7b1fe831003e0a/sf-images/softwarefactory-C7.0-2.2.3-allinone.hot')
    parser.add_argument('--stack_name', required=False, dest="stack_name",
                        default='software-factory-stack')
    parser.add_argument('--key_name', required=False, dest="key_name",
                        default='rhos-jenkins')
    parser.add_argument('--external_net', required=True, dest="external_net")

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    # Initialize cloud
    cloud = shade.openstack_cloud(cloud=args.cloud)

    img_name = retrieve_image(cloud, args.image_url)
    image_id = upload_image(cloud, img_name)
    ext_net_uuid = get_network_id(cloud, args.external_net)

    template_name = retrieve_heat_template(args.template_url)
    create_sf_heat_stack(cloud, args.stack_name, template_name,
                         args.key_name, image_id, ext_net_uuid)

if __name__ == '__main__':
    main()
