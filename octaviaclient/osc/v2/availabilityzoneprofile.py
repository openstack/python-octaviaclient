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

"""Availabilityzone profile action implementation"""

from cliff import lister
from osc_lib.command import command
from osc_lib import utils

from octaviaclient.osc.v2 import constants as const
from octaviaclient.osc.v2 import utils as v2_utils


class CreateAvailabilityzoneProfile(command.ShowOne):
    """Create an octavia availability zone profile"""

    def get_parser(self, prog_name):
        parser = super().get_parser(
            prog_name)

        parser.add_argument(
            '--name',
            metavar='<name>',
            required=True,
            help="New octavia availability zone profile name."
        )
        parser.add_argument(
            '--provider',
            metavar='<provider name>',
            required=True,
            help="Provider name for the availability zone profile."
        )
        parser.add_argument(
            '--availability-zone-data',
            metavar='<availability_zone_data>',
            required=True,
            help="The JSON string containing the availability zone metadata."
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.AVAILABILITYZONEPROFILE_ROWS
        attrs = v2_utils.get_availabilityzoneprofile_attrs(
            self.app.client_manager, parsed_args)
        body = {"availability_zone_profile": attrs}
        client_manager = self.app.client_manager
        data = client_manager.load_balancer.availabilityzoneprofile_create(
            json=body)

        return (rows,
                (utils.get_dict_properties(
                    data['availability_zone_profile'], rows, formatters={})))


class DeleteAvailabilityzoneProfile(command.Command):
    """Delete an availability zone profile"""

    def get_parser(self, prog_name):
        parser = super().get_parser(
            prog_name)

        parser.add_argument(
            'availabilityzoneprofile',
            metavar='<availabilityzone_profile>',
            help="Availability zone profile to delete (name or ID)."
        )

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_availabilityzoneprofile_attrs(
            self.app.client_manager, parsed_args)
        availabilityzoneprofile_id = attrs.pop('availability_zone_profile_id')

        self.app.client_manager.load_balancer.availabilityzoneprofile_delete(
            availabilityzoneprofile_id=availabilityzoneprofile_id)


class ListAvailabilityzoneProfile(lister.Lister):
    """List availability zone profiles"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            '--name',
            metavar='<name>',
            help="List availability zone profiles by profile name."
        )
        parser.add_argument(
            '--provider',
            metavar='<provider_name>',
            help="List availability zone profiles according to their "
                 "provider.",
        )

        return parser

    def take_action(self, parsed_args):
        columns = const.AVAILABILITYZONEPROFILE_COLUMNS
        attrs = v2_utils.get_availabilityzoneprofile_attrs(
            self.app.client_manager, parsed_args)
        client_manager = self.app.client_manager
        data = client_manager.load_balancer.availabilityzoneprofile_list(
            **attrs)
        return (columns,
                (utils.get_dict_properties(s, columns, formatters={})
                 for s in data['availability_zone_profiles']))


class ShowAvailabilityzoneProfile(command.ShowOne):
    """Show the details of a single availability zone profile"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'availabilityzoneprofile',
            metavar='<availabilityzone_profile>',
            help="Name or UUID of the availability zone profile to show."
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.AVAILABILITYZONEPROFILE_ROWS
        attrs = v2_utils.get_availabilityzoneprofile_attrs(
            self.app.client_manager, parsed_args)
        availabilityzoneprofile_id = attrs.pop('availability_zone_profile_id')
        client_manager = self.app.client_manager
        data = client_manager.load_balancer.availabilityzoneprofile_show(
            availabilityzoneprofile_id=availabilityzoneprofile_id
        )

        return (rows, (utils.get_dict_properties(
            data, rows, formatters={})))


class SetAvailabilityzoneProfile(command.Command):
    """Update an availability zone profile"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'availabilityzoneprofile',
            metavar='<availabilityzone_profile>',
            help='Name or UUID of the availability zone profile to update.'
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help="Set the name of the availability zone profile."
        )
        parser.add_argument(
            '--provider',
            metavar='<provider_name>',
            help="Set the provider of the availability zone profile."
        )
        parser.add_argument(
            '--availability-zone-data',
            metavar='<availability_zone_data>',
            help="Set the availability zone data of the profile."
        )

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_availabilityzoneprofile_attrs(
            self.app.client_manager, parsed_args)
        availabilityzoneprofile_id = attrs.pop('availability_zone_profile_id')
        body = {'availability_zone_profile': attrs}

        self.app.client_manager.load_balancer.availabilityzoneprofile_set(
            availabilityzoneprofile_id, json=body)
