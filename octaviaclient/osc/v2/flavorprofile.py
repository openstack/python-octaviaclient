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

"""Flavor profile action implementation"""

from cliff import lister
from osc_lib.command import command
from osc_lib import exceptions
from osc_lib import utils
from oslo_utils import uuidutils

from octaviaclient.osc.v2 import constants as const
from octaviaclient.osc.v2 import utils as v2_utils


class CreateFlavorProfile(command.ShowOne):
    """Create a octavia flavor profile"""

    def get_parser(self, prog_name):
        parser = super(CreateFlavorProfile, self).get_parser(prog_name)

        parser.add_argument(
            '--name',
            metavar='<name>',
            required=True,
            help="New octavia flavor profile name."
        )
        parser.add_argument(
            '--provider',
            metavar='<provider name>',
            required=True,
            help="Provider name for the flavor profile."
        )
        parser.add_argument(
            '--flavor-data',
            metavar='<flavor_data>',
            required=True,
            help="The JSON string containing the flavor metadata."
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.FLAVORPROFILE_ROWS
        attrs = v2_utils.get_flavorprofile_attrs(self.app.client_manager,
                                                 parsed_args)
        body = {"flavorprofile": attrs}
        data = self.app.client_manager.load_balancer.flavorprofile_create(
            json=body)

        return (rows,
                (utils.get_dict_properties(
                    data['flavorprofile'], rows, formatters={})))


class DeleteFlavorProfile(command.Command):
    """Delete a flavor profile"""

    def get_parser(self, prog_name):
        parser = super(DeleteFlavorProfile, self).get_parser(prog_name)

        parser.add_argument(
            'flavorprofile',
            metavar='<flavor_profile>',
            help="Flavor profiles to delete (name or ID)"
        )

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_flavorprofile_attrs(self.app.client_manager,
                                                 parsed_args)
        flavorprofile_id = attrs.pop('flavorprofile_id')

        self.app.client_manager.load_balancer.flavorprofile_delete(
            flavorprofile_id=flavorprofile_id)


class ListFlavorProfile(lister.Lister):
    """List flavor profile"""

    def get_parser(self, prog_name):
        parser = super(ListFlavorProfile, self).get_parser(prog_name)

        parser.add_argument(
            '--name',
            metavar='<name>',
            help="List flavor profiles by flavor profile name."
        )
        parser.add_argument(
            '--provider',
            metavar='<provider_name>',
            help="List flavor profiles according to their provider.",
        )

        return parser

    def take_action(self, parsed_args):
        columns = const.FLAVORPROFILE_COLUMNS
        attrs = v2_utils.get_flavorprofile_attrs(self.app.client_manager,
                                                 parsed_args)
        data = self.app.client_manager.load_balancer.flavorprofile_list(
            **attrs)
        return (columns,
                (utils.get_dict_properties(s, columns, formatters={})
                 for s in data['flavorprofiles']))


class ShowFlavorProfile(command.ShowOne):
    """Show the details for a single flavor profile"""

    def get_parser(self, prog_name):
        parser = super(ShowFlavorProfile, self).get_parser(prog_name)

        parser.add_argument(
            'flavorprofile',
            metavar='<flavor_profile>',
            help="Name or UUID of the flavor profile to show."
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.FLAVORPROFILE_ROWS
        data = None
        if uuidutils.is_uuid_like(parsed_args.flavorprofile):
            try:
                data = (
                    self.app.client_manager.load_balancer.flavorprofile_show(
                        flavorprofile_id=parsed_args.flavorprofile))
            except exceptions.NotFound:
                pass
        if data is None:
            attrs = v2_utils.get_flavorprofile_attrs(self.app.client_manager,
                                                     parsed_args)
            flavorprofile_id = attrs.pop('flavorprofile_id')

            data = self.app.client_manager.load_balancer.flavorprofile_show(
                flavorprofile_id=flavorprofile_id
            )

        return (rows, (utils.get_dict_properties(
            data, rows, formatters={})))


class SetFlavorProfile(command.Command):
    """Update a flavor profile"""

    def get_parser(self, prog_name):
        parser = super(SetFlavorProfile, self).get_parser(prog_name)

        parser.add_argument(
            'flavorprofile',
            metavar='<flavor_profile>',
            help='Name or UUID of the flavor profile to update.'
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help="Set the name of the flavor profile."
        )
        parser.add_argument(
            '--provider',
            metavar='<provider_name>',
            help="Set the provider of the flavor profile."
        )
        parser.add_argument(
            '--flavor-data',
            metavar='<flavor_data>',
            help="Set the flavor data of the flavor profile."
        )

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_flavorprofile_attrs(self.app.client_manager,
                                                 parsed_args)
        flavorprofile_id = attrs.pop('flavorprofile_id')
        body = {'flavorprofile': attrs}

        self.app.client_manager.load_balancer.flavorprofile_set(
            flavorprofile_id, json=body)
