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


def retrieve_image(image_url):
    """Downloads Software factory image."""
    image_name = image_url.rsplit('/', 1)[-1]
    if not os.path.exists(os.getcwd() + '/' + image_name):
        logging.info("== Downloading software factory image ==")
        wget.download(image_url)
    else:
        logging.info("Image already exists locally...skipping image download")

    return image_name


def upload_image(cloud, img_name):
    if cloud.get_image(img_name):
        logging.info("Image already exists in the cloud...skipping uploading")
    else:
        logging.info("== Uploading the image ==")
        cloud.create_image(img_name, filename=img_name, wait=True)


def retrieve_heat_template(template_url):
    template_name = template_url.rsplit('/', 1)[-1]
    if not os.path.exists(os.getcwd() + '/' + template_name):
        logging.info("== Downloading heat template ==")
        wget.download(template_url)
    else:
        logging.info(
            "Heat template already exists...skipping template download")


def create_sf_heat_stack(cloud):
    logging.info("== Creating stack! This might take couple of minutes... ==")
    cloud.create_stack(STACK_NAME, template_file=HEAT_TEMPLATE_NAME, wait=False, key_name=KEY_NAME)
    #heat stack-create --template-file ./softwarefactory-C7.0-2.2.3-allinone.hot -P "key_name=SSH_KEY;domain=FQDN;im$age_id=GLANCE_UUID;external_network=NETWORK_UUID;flavor=m1.large" sf_stack

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
    parser.add_argument('--stack_name', required=False, dest="template_url",
                        default='http://46.231.132.68:8080/v1/AUTH_b50e80d3969f441a8b7b1fe831003e0a/sf-images/softwarefactory-C7.0-2.2.3-allinone.hot')

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    # Initialize cloud
    cloud = shade.openstack_cloud(cloud=args.cloud)

    img_name = retrieve_image(args.image_url)
    upload_image(cloud, img_name)

    retrieve_heat_template(args.template_url)
    create_sf_heat_stack(cloud)

if __name__ == '__main__':
    main()
