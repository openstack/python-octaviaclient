# Copyright (c) 2018 China Telecom Corporation
# Copyright 2019 Red Hat, Inc. All rights reserved.
#
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

"""Availabilityzone action implementation"""

from cliff import lister
from osc_lib.command import command
from osc_lib import utils

from octaviaclient.osc.v2 import constants as const
from octaviaclient.osc.v2 import utils as v2_utils


class CreateAvailabilityzone(command.ShowOne):
    """Create an octavia availability zone"""

    def get_parser(self, prog_name):
        parser = super(CreateAvailabilityzone, self).get_parser(prog_name)

        parser.add_argument(
            '--name',
            metavar='<name>',
            required=True,
            help="New availability zone name."
        )
        parser.add_argument(
            '--availabilityzoneprofile',
            metavar='<availabilityzone_profile>',
            required=True,
            help="Availability zone profile to add the AZ to (name or ID)."
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help="Set the availability zone description."
        )
        admin_group = parser.add_mutually_exclusive_group()
        admin_group.add_argument(
            '--enable',
            action='store_true',
            default=None,
            help="Enable the availability zone."
        )
        admin_group.add_argument(
            '--disable',
            action='store_true',
            default=None,
            help="Disable the availability zone."
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.AVAILABILITYZONE_ROWS
        attrs = v2_utils.get_availabilityzone_attrs(self.app.client_manager,
                                                    parsed_args)
        body = {"availability_zone": attrs}
        data = self.app.client_manager.load_balancer.availabilityzone_create(
            json=body)

        formatters = {'availability_zone_profiles': v2_utils.format_list}

        return (rows,
                (utils.get_dict_properties(
                    data['availability_zone'], rows, formatters=formatters)))


class DeleteAvailabilityzone(command.Command):
    """Delete an availability zone"""

    def get_parser(self, prog_name):
        parser = super(DeleteAvailabilityzone, self).get_parser(prog_name)

        parser.add_argument(
            'availabilityzone',
            metavar='<availabilityzone>',
            help="Name of the availability zone to delete."
        )

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_availabilityzone_attrs(self.app.client_manager,
                                                    parsed_args)
        availabilityzone_name = attrs.pop('availabilityzone_name')

        self.app.client_manager.load_balancer.availabilityzone_delete(
            availabilityzone_name=availabilityzone_name)


class ListAvailabilityzone(lister.Lister):
    """List availability zones"""

    def get_parser(self, prog_name):
        parser = super(ListAvailabilityzone, self).get_parser(prog_name)

        parser.add_argument(
            '--name',
            metavar='<name>',
            help="List availability zones according to their name."
        )
        parser.add_argument(
            '--availabilityzoneprofile',
            metavar='<availabilityzone_profile>',
            help="List availability zones according to their AZ profile.",
        )
        admin_state_group = parser.add_mutually_exclusive_group()
        admin_state_group.add_argument(
            '--enable',
            action='store_true',
            default=None,
            help="List enabled availability zones."
        )
        admin_state_group.add_argument(
            '--disable',
            action='store_true',
            default=None,
            help="List disabled availability zones."
        )

        return parser

    def take_action(self, parsed_args):
        columns = const.AVAILABILITYZONE_COLUMNS
        attrs = v2_utils.get_availabilityzone_attrs(self.app.client_manager,
                                                    parsed_args)
        data = self.app.client_manager.load_balancer.availabilityzone_list(
            **attrs)
        formatters = {'availabilityzoneprofiles': v2_utils.format_list}
        return (columns,
                (utils.get_dict_properties(s, columns, formatters=formatters)
                 for s in data['availability_zones']))


class ShowAvailabilityzone(command.ShowOne):
    """Show the details for a single availability zone"""

    def get_parser(self, prog_name):
        parser = super(ShowAvailabilityzone, self).get_parser(prog_name)

        parser.add_argument(
            'availabilityzone',
            metavar='<availabilityzone>',
            help="Name of the availability zone."
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.AVAILABILITYZONE_ROWS
        attrs = v2_utils.get_availabilityzone_attrs(self.app.client_manager,
                                                    parsed_args)
        availabilityzone_name = attrs.pop('availabilityzone_name')

        data = self.app.client_manager.load_balancer.availabilityzone_show(
            availabilityzone_name=availabilityzone_name
        )
        formatters = {'availabilityzoneprofiles': v2_utils.format_list}

        return (rows, (utils.get_dict_properties(
            data, rows, formatters=formatters)))


class SetAvailabilityzone(command.Command):
    """Update an availability zone"""

    def get_parser(self, prog_name):
        parser = super(SetAvailabilityzone, self).get_parser(prog_name)

        parser.add_argument(
            'availabilityzone',
            metavar='<availabilityzone>',
            help='Name of the availability zone to update.'
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help="Set the description of the availability zone."
        )
        admin_group = parser.add_mutually_exclusive_group()
        admin_group.add_argument(
            '--enable',
            action='store_true',
            default=None,
            help="Enable the availability zone."
        )
        admin_group.add_argument(
            '--disable',
            action='store_true',
            default=None,
            help="Disable the availability zone."
        )

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_availabilityzone_attrs(self.app.client_manager,
                                                    parsed_args)
        availabilityzone_name = attrs.pop('availabilityzone_name')
        body = {'availability_zone': attrs}

        self.app.client_manager.load_balancer.availabilityzone_set(
            availabilityzone_name, json=body)


class UnsetAvailabilityzone(command.Command):
    """Clear availability zone settings"""

    def get_parser(self, prog_name):
        parser = super(UnsetAvailabilityzone, self).get_parser(prog_name)

        parser.add_argument(
            'availabilityzone',
            metavar='<availabilityzone>',
            help="Name of the availability zone to update."
        )
        parser.add_argument(
            '--description',
            action='store_true',
            help="Clear the availability zone description."
        )
        return parser

    def take_action(self, parsed_args):
        unset_args = v2_utils.get_unsets(parsed_args)
        if not unset_args:
            return

        availabilityzone_id = v2_utils.get_resource_id(
            self.app.client_manager.load_balancer.availabilityzone_list,
            'availability_zones', parsed_args.availabilityzone)

        body = {'availability_zone': unset_args}

        self.app.client_manager.load_balancer.availabilityzone_set(
            availabilityzone_id, json=body)
