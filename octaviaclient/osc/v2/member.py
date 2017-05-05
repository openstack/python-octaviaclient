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


from cliff import lister
from osc_lib.command import command
from osc_lib import utils

from octaviaclient.osc.v2 import constants as const
from octaviaclient.osc.v2 import utils as v2_utils


class ListMember(lister.Lister):
    """List members in a pool"""

    def get_parser(self, prog_name):
        parser = super(ListMember, self).get_parser(prog_name)

        parser.add_argument(
            'pool',
            metavar='<pool>',
            help="Pool name or ID to list the members of."
        )

        return parser

    def take_action(self, parsed_args):
        columns = const.MEMBER_COLUMNS

        attrs = v2_utils.get_member_attrs(self.app.client_manager, parsed_args)
        pool_id = attrs.pop('pool_id')

        data = self.app.client_manager.load_balancer.member_list(
            pool_id=pool_id)

        return (columns,
                (utils.get_dict_properties(
                    s, columns,
                    formatters={},
                ) for s in data['members']))


class ShowMember(command.ShowOne):
    """Shows details of a single Member"""

    def get_parser(self, prog_name):
        parser = super(ShowMember, self).get_parser(prog_name)

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
        attrs = v2_utils.get_member_attrs(self.app.client_manager, parsed_args)

        member_id = attrs.pop('member_id')
        pool_id = attrs.pop('pool_id')

        data = self.app.client_manager.load_balancer.member_show(
            pool_id=pool_id, member_id=member_id)

        return (rows, (utils.get_dict_properties(
            data, rows, formatters={})))


class CreateMember(command.ShowOne):
    """Creating a member in a pool"""

    def get_parser(self, prog_name):
        parser = super(CreateMember, self).get_parser(prog_name)

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
        parser.add_argument(
            '--weight',
            metavar='<weight>',
            type=int,
            choices=range(0, 256),
            help="The weight of a member determines the portion of requests "
                 "or connections it services compared to the other members of "
                 "the pool."
        )
        parser.add_argument(
            '--address',
            metavar='<ip_address>',
            help="The IP address of the backend member server",
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
            choices=range(1, 65535),
            help="The protocol port number the backend member server is "
                 "listening on.",
            required=True
        )
        parser.add_argument(
            '--monitor-port',
            metavar='<monitor_port>',
            type=int,
            choices=range(1, 65535),
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
            help="Enable member (default)"
        )
        admin_group.add_argument(
            '--disable',
            action='store_true',
            default=None,
            help="Disable member"
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.MEMBER_ROWS
        attrs = v2_utils.get_member_attrs(self.app.client_manager, parsed_args)
        pool_id = attrs.pop('pool_id')

        body = {"member": attrs}
        data = self.app.client_manager.load_balancer.member_create(
            pool_id=pool_id,
            json=body
        )

        return (rows,
                (utils.get_dict_properties(
                    data['member'], rows, formatters={})))


class SetMember(command.Command):
    """Update a member"""

    def get_parser(self, prog_name):
        parser = super(SetMember, self).get_parser(prog_name)

        parser.add_argument(
            'pool',
            metavar='<pool>',
            help="Pool that the member to update belongs to (name or ID)."
        )
        parser.add_argument(
            'member',
            metavar='<member>',
            help="Name or ID of the member to update"
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help="Set the name of the member"
        )
        parser.add_argument(
            '--weight',
            metavar='<weight>',
            type=int,
            choices=range(0, 256),
            help="Set the weight of member in the pool"
        )
        parser.add_argument(
            '--monitor-port',
            metavar='<monitor_port>',
            type=int,
            choices=range(1, 65535),
            help="An alternate protocol port used for health monitoring a "
                 "backend member",
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
            help="Set the admin_state_up to True"
        )
        admin_group.add_argument(
            '--disable',
            action='store_true',
            default=None,
            help="Set the admin_state_up to False")

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_member_attrs(self.app.client_manager, parsed_args)
        pool_id = attrs.pop('pool_id')
        member_id = attrs.pop('member_id')
        post_data = {"member": attrs}

        self.app.client_manager.load_balancer.member_set(
            pool_id=pool_id,
            member_id=member_id,
            json=post_data
        )


class DeleteMember(command.Command):
    """Delete a member from a pool """

    def get_parser(self, prog_name):
        parser = super(DeleteMember, self).get_parser(prog_name)

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

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_member_attrs(self.app.client_manager, parsed_args)
        id = attrs.pop('member_id')
        pool_id = attrs.pop('pool_id')

        self.app.client_manager.load_balancer.member_delete(
            pool_id=pool_id,
            member_id=id
        )
