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

import logging
import os
import shade
import wget

logging.basicConfig(level=logging.INFO, format='%(message)s')

IMAGE_URL_PATH = 'http://46.231.132.68:8080/v1/AUTH_b50e80d3969f441a8b7b1fe831003e0a/sf-images'
LOCAL_IMAGE_NAME = 'softwarefactory-C7.0-2.2.3.img.qcow2'
UPLOAD_IMAGE_NAME = 'sf-2.3.3'

HEAT_TEMPLATE_NAME = 'softwarefactory-C7.0-2.2.3-allinone.hot'
HEAT_TEMPLATE_URL = 'http://46.231.132.68:8080/v1/AUTH_b50e80d3969f441a8b7b1fe831003e0a/sf-images/softwarefactory-C7.0-2.2.3-allinone.hot'

STACK_NAME = 'sf_stack'
KEY_NAME = 'rhos-jenkins'

# Initialize cloud
cloud = shade.openstack_cloud(cloud='qeos')

# Retrieve image
if not os.path.exists(os.getcwd() + '/' + LOCAL_IMAGE_NAME):
    logging.info("=== Downloading software factory image ===")
    wget.download(IMAGE_URL_PATH + '/' + LOCAL_IMAGE_NAME)
else:
    logging.info("Image already exists locally")

# Upload image
if cloud.get_image(UPLOAD_IMAGE_NAME):
    logging.info("Image already exists on the cloud")
else:
    logging.info("=== Uploading the image ===")
    image = cloud.create_image(UPLOAD_IMAGE_NAME, filename=LOCAL_IMAGE_NAME, wait=True)

# Retrieve heat template
if not os.path.exists(os.getcwd() + '/' + HEAT_TEMPLATE_NAME):
    logging.info("=== Downloading heat template ===")
    wget.download(HEAT_TEMPLATE_URL)
else:
    logging.info("Heat template already exists")

# Create SF heat stackgg
logging.info("Creating stack! This might take couple of minutes...")
cloud.create_stack(STACK_NAME, template_file=HEAT_TEMPLATE_NAME, wait=False, key_name=KEY_NAME)
#heat stack-create --template-file ./softwarefactory-C7.0-2.2.3-allinone.hot -P "key_name=SSH_KEY;domain=FQDN;im$age_id=GLANCE_UUID;external_network=NETWORK_UUID;flavor=m1.large" sf_stack

def check_for_reqs():
    pass

def main():
    
    check_for_reqs()

if __name__ == '__main__':
    main()
