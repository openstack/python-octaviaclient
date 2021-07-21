# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

"""OpenStackClient plugin for Load Balancer service."""

import logging

from octaviaclient.api.v2 import octavia
from osc_lib import utils

LOG = logging.getLogger(__name__)

DEFAULT_LOADBALANCER_API_VERSION = '2.0'
API_VERSION_OPTION = 'os_loadbalancer_api_version'
API_NAME = 'load_balancer'
LOAD_BALANCER_API_TYPE = 'loadbalancer'
LOAD_BALANCER_API_VERSIONS = {
    '2.0': 'octaviaclient.api.v2.octavia.OctaviaAPI',
}


def make_client(instance):
    """Returns a load balancer service client"""
    endpoint = instance.get_endpoint_for_service_type(
        'load-balancer',
        region_name=instance.region_name,
        interface=instance.interface,
    )
    client = octavia.OctaviaAPI(
        session=instance.session,
        service_type='load-balancer',
        endpoint=endpoint,
    )
    return client


def build_option_parser(parser):
    """Hook to add global options

    Called from openstackclient.shell.OpenStackShell.__init__()
    after the builtin parser has been initialized. This is
    where a plugin can add global options such as an API version.

    :param argparse.ArgumentParser parser: The parser object that
        has been initialized by OpenStackShell.
    """
    parser.add_argument(
        '--os-loadbalancer-api-version',
        metavar='<loadbalancer-api-version>',
        default=utils.env(
            'OS_LOADBALANCER_API_VERSION',
            default=DEFAULT_LOADBALANCER_API_VERSION),
        help='OSC Plugin API version, default=' +
             DEFAULT_LOADBALANCER_API_VERSION +
             ' (Env: OS_LOADBALANCER_API_VERSION)')
    return parser
