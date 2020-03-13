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

"""Flavor action implementation"""

from cliff import lister
from osc_lib.command import command
from osc_lib import exceptions
from osc_lib import utils
from oslo_utils import uuidutils

from octaviaclient.osc.v2 import constants as const
from octaviaclient.osc.v2 import utils as v2_utils


class CreateFlavor(command.ShowOne):
    """Create a octavia flavor"""

    def get_parser(self, prog_name):
        parser = super(CreateFlavor, self).get_parser(prog_name)

        parser.add_argument(
            '--name',
            metavar='<name>',
            required=True,
            help="New flavor name."
        )
        parser.add_argument(
            '--flavorprofile',
            metavar='<flavor_profile>',
            required=True,
            help="Flavor profile to add the flavor to (name or ID)."
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help="Set flavor description."
        )
        admin_group = parser.add_mutually_exclusive_group()
        admin_group.add_argument(
            '--enable',
            action='store_true',
            default=None,
            help="Enable flavor."
        )
        admin_group.add_argument(
            '--disable',
            action='store_true',
            default=None,
            help="Disable flavor."
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.FLAVOR_ROWS
        attrs = v2_utils.get_flavor_attrs(self.app.client_manager,
                                          parsed_args)
        body = {"flavor": attrs}
        data = self.app.client_manager.load_balancer.flavor_create(
            json=body)

        formatters = {'flavorprofiles': v2_utils.format_list}

        return (rows,
                (utils.get_dict_properties(
                    data['flavor'], rows, formatters=formatters)))


class DeleteFlavor(command.Command):
    """Delete a flavor"""

    def get_parser(self, prog_name):
        parser = super(DeleteFlavor, self).get_parser(prog_name)

        parser.add_argument(
            'flavor',
            metavar='<flavor>',
            help="Flavor to delete (name or ID)"
        )

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_flavor_attrs(self.app.client_manager,
                                          parsed_args)
        flavor_id = attrs.pop('flavor_id')

        self.app.client_manager.load_balancer.flavor_delete(
            flavor_id=flavor_id)


class ListFlavor(lister.Lister):
    """List flavor"""

    def get_parser(self, prog_name):
        parser = super(ListFlavor, self).get_parser(prog_name)

        parser.add_argument(
            '--name',
            metavar='<name>',
            help="List flavors according to their name."
        )
        parser.add_argument(
            '--flavorprofile',
            metavar='<flavor_profile>',
            help="List flavors according to their flavor profile.",
        )
        admin_state_group = parser.add_mutually_exclusive_group()
        admin_state_group.add_argument(
            '--enable',
            action='store_true',
            default=None,
            help="List enabled flavors."
        )
        admin_state_group.add_argument(
            '--disable',
            action='store_true',
            default=None,
            help="List disabled flavors."
        )

        return parser

    def take_action(self, parsed_args):
        columns = const.FLAVOR_COLUMNS
        attrs = v2_utils.get_flavor_attrs(self.app.client_manager,
                                          parsed_args)
        data = self.app.client_manager.load_balancer.flavor_list(
            **attrs)
        formatters = {'flavorprofiles': v2_utils.format_list}
        return (columns,
                (utils.get_dict_properties(s, columns, formatters=formatters)
                 for s in data['flavors']))


class ShowFlavor(command.ShowOne):
    """Show the details for a single flavor"""

    def get_parser(self, prog_name):
        parser = super(ShowFlavor, self).get_parser(prog_name)

        parser.add_argument(
            'flavor',
            metavar='<flavor>',
            help="Name or UUID of the flavor."
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.FLAVOR_ROWS
        data = None
        if uuidutils.is_uuid_like(parsed_args.flavor):
            try:
                data = self.app.client_manager.load_balancer.flavor_show(
                    flavor_id=parsed_args.flavor)
            except exceptions.NotFound:
                pass
        if data is None:
            attrs = v2_utils.get_flavor_attrs(self.app.client_manager,
                                              parsed_args)
            flavor_id = attrs.pop('flavor_id')

            data = self.app.client_manager.load_balancer.flavor_show(
                flavor_id=flavor_id
            )
        formatters = {'flavorprofiles': v2_utils.format_list}

        return (rows, (utils.get_dict_properties(
            data, rows, formatters=formatters)))


class SetFlavor(command.Command):
    """Update a flavor"""

    def get_parser(self, prog_name):
        parser = super(SetFlavor, self).get_parser(prog_name)

        parser.add_argument(
            'flavor',
            metavar='<flavor>',
            help='Name or UUID of the flavor to update.'
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help="Set the name of the flavor."
        )
        admin_group = parser.add_mutually_exclusive_group()
        admin_group.add_argument(
            '--enable',
            action='store_true',
            default=None,
            help="Enable flavor."
        )
        admin_group.add_argument(
            '--disable',
            action='store_true',
            default=None,
            help="Disable flavor."
        )

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_flavor_attrs(self.app.client_manager,
                                          parsed_args)
        flavor_id = attrs.pop('flavor_id')
        body = {'flavor': attrs}

        self.app.client_manager.load_balancer.flavor_set(
            flavor_id, json=body)


class UnsetFlavor(command.Command):
    """Clear flavor settings"""

    def get_parser(self, prog_name):
        parser = super(UnsetFlavor, self).get_parser(prog_name)

        parser.add_argument(
            'flavor',
            metavar='<flavor>',
            help="Flavor to update (name or ID)."
        )
        parser.add_argument(
            '--description',
            action='store_true',
            help="Clear the flavor description."
        )
        return parser

    def take_action(self, parsed_args):
        unset_args = v2_utils.get_unsets(parsed_args)
        if not unset_args:
            return

        flavor_id = v2_utils.get_resource_id(
            self.app.client_manager.load_balancer.flavor_list,
            'flavors', parsed_args.flavor)

        body = {'flavor': unset_args}

        self.app.client_manager.load_balancer.flavor_set(
            flavor_id, json=body)
