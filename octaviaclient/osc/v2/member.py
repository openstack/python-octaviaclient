#   Copyright 2019 Red Hat, Inc. All rights reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

"""Member action implementation"""

import functools

from cliff import lister
from osc_lib.command import command
from osc_lib import exceptions
from osc_lib import utils
from osc_lib.utils import tags as _tag
from oslo_utils import uuidutils

from octaviaclient.osc.v2 import constants as const
from octaviaclient.osc.v2 import utils as v2_utils
from octaviaclient.osc.v2 import validate


class ListMember(lister.Lister):
    """List members in a pool"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'pool',
            metavar='<pool>',
            help="Pool name or ID to list the members of."
        )

        _tag.add_tag_filtering_option_to_parser(parser, 'member')

        return parser

    def take_action(self, parsed_args):
        columns = const.MEMBER_COLUMNS

        attrs = v2_utils.get_member_attrs(self.app.client_manager, parsed_args)

        data = self.app.client_manager.load_balancer.member_list(
            **attrs)

        return (columns,
                (utils.get_dict_properties(
                    s, columns,
                    formatters={},
                ) for s in data['members']))


class ShowMember(command.ShowOne):
    """Shows details of a single Member"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'pool',
            metavar='<pool>',
            help='Pool name or ID to show the members of.'
        )
        parser.add_argument(
            'member',
            metavar='<member>',
            help="Name or ID of the member to show."
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.MEMBER_ROWS
        data = None
        if (uuidutils.is_uuid_like(parsed_args.pool) and
                uuidutils.is_uuid_like(parsed_args.member)):
            try:
                data = self.app.client_manager.load_balancer.member_show(
                    pool_id=parsed_args.pool, member_id=parsed_args.member)
            except exceptions.NotFound:
                pass
        if data is None:
            attrs = v2_utils.get_member_attrs(self.app.client_manager,
                                              parsed_args)

            member_id = attrs.pop('member_id')
            pool_id = attrs.pop('pool_id')

            data = self.app.client_manager.load_balancer.member_show(
                pool_id=pool_id, member_id=member_id)

        # Handle older API versions that did not have the vnic_type
        if not data.get('vnic_type', False):
            data['vnic_type'] = 'normal'

        formatters = {'tags': v2_utils.FlatListColumn}

        return (rows, (utils.get_dict_properties(
            data, rows, formatters=formatters)))


class CreateMember(command.ShowOne):
    """Creating a member in a pool"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'pool',
            metavar='<pool>',
            help="ID or name of the pool to create the member for."
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help="Name of the member."
        )
        backup = parser.add_mutually_exclusive_group()
        backup.add_argument(
            '--disable-backup',
            action='store_true',
            default=None,
            help="Disable member backup (default)."
        )
        backup.add_argument(
            '--enable-backup',
            action='store_true',
            default=None,
            help="Enable member backup."
        )
        parser.add_argument(
            '--weight',
            metavar='<weight>',
            type=int,
            help="The weight of a member determines the portion of requests "
                 "or connections it services compared to the other members of "
                 "the pool."
        )
        parser.add_argument(
            '--address',
            metavar='<ip_address>',
            help="The IP address of the backend member server.",
            required=True
        )
        parser.add_argument(
            '--subnet-id',
            metavar='<subnet_id>',
            help="The subnet ID the member service is accessible from."
        )
        parser.add_argument(
            '--protocol-port',
            metavar='<protocol_port>',
            type=int,
            help="The protocol port number the backend member server is "
                 "listening on.",
            required=True
        )
        parser.add_argument(
            '--monitor-port',
            metavar='<monitor_port>',
            type=int,
            help="An alternate protocol port used for health monitoring a "
                 "backend member.",
        )
        parser.add_argument(
            '--monitor-address',
            metavar='<monitor_address>',
            help="An alternate IP address used for health monitoring a "
                 "backend member."
        )
        admin_group = parser.add_mutually_exclusive_group()
        admin_group.add_argument(
            '--enable',
            action='store_true',
            default=None,
            help="Enable member (default)."
        )
        admin_group.add_argument(
            '--disable',
            action='store_true',
            default=None,
            help="Disable member."
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete.',
        )
        parser.add_argument(
            '--request-sriov',
            action='store_true',
            default=None,
            help='Request that the member port be created using an SR-IOV VF.',
        )

        _tag.add_tag_option_to_parser_for_create(
            parser, 'member')

        return parser

    def take_action(self, parsed_args):
        rows = const.MEMBER_ROWS
        attrs = v2_utils.get_member_attrs(self.app.client_manager, parsed_args)

        validate.check_member_attrs(attrs)

        pool_id = attrs.pop('pool_id')

        body = {"member": attrs}
        data = self.app.client_manager.load_balancer.member_create(
            pool_id=pool_id,
            json=body
        )

        if parsed_args.wait:
            pool = self.app.client_manager.load_balancer.pool_show(pool_id)
            v2_utils.wait_for_active(
                status_f=(self.app.client_manager.load_balancer.
                          load_balancer_show),
                res_id=pool['loadbalancers'][0]['id']
            )
            data = {
                'member': (
                    self.app.client_manager.load_balancer.member_show(
                        pool_id, data['member']['id']))
            }

        # Handle older API versions that did not have the vnic_type
        if not data['member'].get('vnic_type', False):
            data['member']['vnic_type'] = 'normal'

        formatters = {'tags': v2_utils.FlatListColumn}

        return (rows,
                (utils.get_dict_properties(
                    data['member'], rows, formatters=formatters)))


class SetMember(command.Command):
    """Update a member"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'pool',
            metavar='<pool>',
            help="Pool that the member to update belongs to (name or ID)."
        )
        parser.add_argument(
            'member',
            metavar='<member>',
            help="Name or ID of the member to update."
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help="Set the name of the member."
        )
        backup = parser.add_mutually_exclusive_group()
        backup.add_argument(
            '--disable-backup',
            action='store_true',
            default=None,
            help="Disable member backup (default)."
        )
        backup.add_argument(
            '--enable-backup',
            action='store_true',
            default=None,
            help="Enable member backup."
        )
        parser.add_argument(
            '--weight',
            metavar='<weight>',
            type=int,
            help="Set the weight of member in the pool."
        )
        parser.add_argument(
            '--monitor-port',
            metavar='<monitor_port>',
            type=int,
            help="An alternate protocol port used for health monitoring a "
                 "backend member.",
        )
        parser.add_argument(
            '--monitor-address',
            metavar='<monitor_address>',
            help="An alternate IP address used for health monitoring a "
                 "backend member."
        )
        admin_group = parser.add_mutually_exclusive_group()
        admin_group.add_argument(
            '--enable',
            action='store_true',
            default=None,
            help="Set the admin_state_up to True."
        )
        admin_group.add_argument(
            '--disable',
            action='store_true',
            default=None,
            help="Set the admin_state_up to False.")
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete.',
        )

        _tag.add_tag_option_to_parser_for_set(parser, 'member')

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_member_attrs(self.app.client_manager, parsed_args)

        validate.check_member_attrs(attrs)

        pool_id = attrs.pop('pool_id')
        member_id = attrs.pop('member_id')

        member_show = functools.partial(
            self.app.client_manager.load_balancer.member_show,
            pool_id
        )
        v2_utils.set_tags_for_set(
            member_show, member_id, attrs, clear_tags=parsed_args.no_tag)

        post_data = {"member": attrs}

        self.app.client_manager.load_balancer.member_set(
            pool_id=pool_id,
            member_id=member_id,
            json=post_data
        )

        if parsed_args.wait:
            v2_utils.wait_for_active(
                status_f=member_show,
                res_id=member_id
            )


class DeleteMember(command.Command):
    """Delete a member from a pool """

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'pool',
            metavar='<pool>',
            help="Pool name or ID to delete the member from."
        )

        parser.add_argument(
            'member',
            metavar='<member>',
            help="Name or ID of the member to be deleted."
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete.',
        )

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_member_attrs(self.app.client_manager, parsed_args)
        id = attrs.pop('member_id')
        pool_id = attrs.pop('pool_id')

        self.app.client_manager.load_balancer.member_delete(
            pool_id=pool_id,
            member_id=id
        )

        if parsed_args.wait:
            member_show = functools.partial(
                self.app.client_manager.load_balancer.member_show,
                pool_id
            )
            v2_utils.wait_for_delete(
                status_f=member_show,
                res_id=id
            )


class UnsetMember(command.Command):
    """Clear member settings"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'pool',
            metavar='<pool>',
            help="Pool that the member to update belongs to (name or ID)."
        )
        parser.add_argument(
            'member',
            metavar="<member>",
            help="Member to modify (name or ID)."
        )
        parser.add_argument(
            '--backup',
            action='store_true',
            help="Clear the backup member flag."
        )
        parser.add_argument(
            '--monitor-address',
            action='store_true',
            help="Clear the member monitor address."
        )
        parser.add_argument(
            '--monitor-port',
            action='store_true',
            help="Clear the member monitor port."
        )
        parser.add_argument(
            '--name',
            action='store_true',
            help="Clear the member name."
        )
        parser.add_argument(
            '--weight',
            action='store_true',
            help="Reset the member weight to the API default."
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete.',
        )
        _tag.add_tag_option_to_parser_for_unset(parser, 'member')

        return parser

    def take_action(self, parsed_args):
        unset_args = v2_utils.get_unsets(parsed_args)
        if not unset_args and not parsed_args.all_tag:
            return

        pool_id = v2_utils.get_resource_id(
            self.app.client_manager.load_balancer.pool_list,
            'pools', parsed_args.pool)

        member_show = functools.partial(
            self.app.client_manager.load_balancer.member_show,
            pool_id
        )

        member_dict = {'pool_id': pool_id, 'member_id': parsed_args.member}
        member_id = v2_utils.get_resource_id(
            self.app.client_manager.load_balancer.member_list,
            'members', member_dict)

        v2_utils.set_tags_for_unset(
            member_show, member_id, unset_args,
            clear_tags=parsed_args.all_tag)

        body = {'member': unset_args}

        self.app.client_manager.load_balancer.member_set(
            pool_id=pool_id, member_id=member_id, json=body)

        if parsed_args.wait:
            v2_utils.wait_for_active(
                status_f=member_show,
                res_id=member_id
            )
