# Copyright (c) 2018 China Telecom Corporation
# All Rights Reserved.
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

"""Octavia provider action implementation"""

from cliff import lister
from osc_lib import utils

from octaviaclient.osc.v2 import constants as const
from octaviaclient.osc.v2 import utils as v2_utils


class ListProvider(lister.Lister):
    """List all providers"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        return parser

    def take_action(self, parsed_args):
        columns = const.PROVIDER_COLUMNS
        data = self.app.client_manager.load_balancer.provider_list()

        return (columns,
                (utils.get_dict_properties(
                    s, columns,
                    formatters={},
                ) for s in data['providers']))


class ListProviderCapability(lister.Lister):
    """List specified provider driver's capabilities."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'provider',
            metavar='<provider_name>',
            help="Name of the provider driver."
        )
        type_group = parser.add_mutually_exclusive_group()
        type_group.add_argument(
            '--flavor',
            action='store_true',
            default=None,
            help="Get capabilities for flavor only."
        )
        type_group.add_argument(
            '--availability-zone',
            action='store_true',
            default=None,
            help="Get capabilities for availability zone only."
        )

        return parser

    def take_action(self, parsed_args):
        columns = const.PROVIDER_CAPABILITY_COLUMNS
        attrs = v2_utils.get_provider_attrs(parsed_args)
        provider = attrs.pop('provider_name')
        fetch_flavor = attrs.pop('flavor', False)
        fetch_az = attrs.pop('availability_zone', False)
        client = self.app.client_manager

        data = []
        if not fetch_az:
            flavor_data = (
                client.load_balancer.
                provider_flavor_capability_list(provider=provider))
            for capability in flavor_data['flavor_capabilities']:
                capability['type'] = 'flavor'
                data.append(capability)
        if not fetch_flavor:
            az_data = (
                client.load_balancer.
                provider_availability_zone_capability_list(
                    provider=provider))
            for capability in az_data['availability_zone_capabilities']:
                capability['type'] = 'availability_zone'
                data.append(capability)
        return (columns,
                (utils.get_dict_properties(
                    s, columns,
                    formatters={},
                ) for s in data))
