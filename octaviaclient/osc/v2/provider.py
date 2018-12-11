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
        parser = super(ListProvider, self).get_parser(prog_name)

        return parser

    def take_action(self, parsed_args):
        columns = const.PROVIDER_COLUMNS
        data = self.app.client_manager.load_balancer.provider_list()

        return (columns,
                (utils.get_dict_properties(
                    s, columns,
                    formatters={},
                ) for s in data['providers']))


class ListProviderFlavorCapability(lister.Lister):
    """List specified provider driver's flavor capabilicies."""

    def get_parser(self, prog_name):
        parser = super(ListProviderFlavorCapability,
                       self).get_parser(prog_name)

        parser.add_argument(
            'provider',
            metavar='<provider_name>',
            help="Name of the provider driver."
        )

        return parser

    def take_action(self, parsed_args):
        columns = const.PROVIDER_CAPABILICY_COLUMNS
        attrs = v2_utils.get_provider_attrs(parsed_args)
        provider = attrs.pop('provider_name')
        client = self.app.client_manager
        data = client.load_balancer.provider_capability_list(
            provider=provider)
        return (columns,
                (utils.get_dict_properties(
                    s, columns,
                    formatters={},
                ) for s in data['flavor_capabilities']))
