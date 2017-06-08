#   Copyright 2017 GoDaddy
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

"""Pool action implementation"""

from cliff import lister
from osc_lib.command import command
from osc_lib import utils

from octaviaclient.osc.v2 import constants as const
from octaviaclient.osc.v2 import utils as v2_utils


class CreatePool(command.ShowOne):
    """Create a pool"""

    def get_parser(self, prog_name):
        parser = super(CreatePool, self).get_parser(prog_name)

        parser.add_argument(
            '--name',
            metavar='<name>',
            help="Set pool name."
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help="Set pool description."
        )
        parser.add_argument(
            '--protocol',
            metavar="{TCP,HTTP,HTTPS,TERMINATED_HTTPS,PROXY}",
            required=True,
            choices=['TCP', 'HTTP', 'HTTPS', 'TERMINATED_HTTPS', 'PROXY'],
            help="Set the pool protocol."
        )
        parent_group = parser.add_mutually_exclusive_group(required=True)
        parent_group.add_argument(
            '--listener',
            metavar='<listener>',
            help="Listener to add the pool to (name or ID)."
        )
        parent_group.add_argument(
            '--loadbalancer',
            metavar='<load_balancer>',
            help="Load balncer to add the pool to (name or ID)"
        )
        parser.add_argument(
            '--session-persistence',
            metavar='<session persistence>',
            help="Set the session persistence for the listener (key=value)."
        )
        parser.add_argument(
            '--lb-algorithm',
            metavar="{SOURCE_IP,ROUND_ROBIN,LEAST_CONNECTIONS}",
            required=True,
            choices=['SOURCE_IP', 'ROUND_ROBIN', 'LEAST_CONNECTIONS'],
            help="Load balancing algorithm to use."
        )
        admin_group = parser.add_mutually_exclusive_group()
        admin_group.add_argument(
            '--enable',
            action='store_true',
            default=True,
            help="Enable pool (default)."
        )
        admin_group.add_argument(
            '--disable',
            action='store_true',
            default=None,
            help="Disable pool."
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.POOL_ROWS
        attrs = v2_utils.get_pool_attrs(self.app.client_manager, parsed_args)

        body = {"pool": attrs}
        data = self.app.client_manager.load_balancer.pool_create(
            json=body)
        formatters = {'loadbalancers': v2_utils.format_list,
                      'members': v2_utils.format_list,
                      'listeners': v2_utils.format_list,
                      'session_persistence': v2_utils.format_hash}

        return (rows, (utils.get_dict_properties(
            data['pool'], rows, formatters=formatters)))


class DeletePool(command.Command):
    """Delete a pool"""

    def get_parser(self, prog_name):
        parser = super(DeletePool, self).get_parser(prog_name)

        parser.add_argument(
            'pool',
            metavar="<pool>",
            help="Pool to delete (name or ID)."
        )

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_pool_attrs(self.app.client_manager, parsed_args)
        pool_id = attrs.pop('pool_id')
        self.app.client_manager.load_balancer.pool_delete(
            pool_id=pool_id)


class ListPool(lister.Lister):
    """List pools"""

    def get_parser(self, prog_name):
        parser = super(ListPool, self).get_parser(prog_name)

        return parser

    def take_action(self, parsed_args):
        columns = const.POOL_COLUMNS

        data = self.app.client_manager.load_balancer.pool_list()
        formatters = {'loadbalancers': v2_utils.format_list,
                      'members': v2_utils.format_list,
                      'listeners': v2_utils.format_list}

        return (columns,
                (utils.get_dict_properties(
                    s, columns, formatters=formatters) for s in data['pools']))


class ShowPool(command.ShowOne):
    """Show the details of a single pool"""

    def get_parser(self, prog_name):
        parser = super(ShowPool, self).get_parser(prog_name)

        parser.add_argument(
            'pool',
            metavar='<pool>',
            help='Name or UUID of the pool.'
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.POOL_ROWS

        attrs = v2_utils.get_pool_attrs(self.app.client_manager, parsed_args)
        pool_id = attrs.pop('pool_id')

        data = self.app.client_manager.load_balancer.pool_show(
            pool_id=pool_id,
        )
        formatters = {'loadbalancers': v2_utils.format_list,
                      'members': v2_utils.format_list,
                      'listeners': v2_utils.format_list,
                      'session_persistence': v2_utils.format_hash}

        return (rows, (utils.get_dict_properties(
            data, rows, formatters=formatters)))


class SetPool(command.Command):
    """Update a pool"""

    def get_parser(self, prog_name):
        parser = super(SetPool, self).get_parser(prog_name)

        parser.add_argument(
            'pool',
            metavar="<pool>",
            help="Pool to update (name or ID)."
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help="Set the name of the pool."
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help="Set the description of the pool."
        )
        parser.add_argument(
            '--session-persistence',
            metavar='<session_persistence>',
            help="Set the session persistence for the listener (key=value)."
        )
        parser.add_argument(
            '--lb-algorithm',
            metavar="{SOURCE_IP,ROUND_ROBIN,LEAST_CONNECTIONS}",
            choices=['SOURCE_IP', 'ROUND_ROBIN', 'LEAST_CONNECTIONS'],
            help="Set the load balancing algorithm to use."
        )
        admin_group = parser.add_mutually_exclusive_group()
        admin_group.add_argument(
            '--enable',
            action='store_true',
            default=None,
            help="Enable pool."
        )
        admin_group.add_argument(
            '--disable',
            action='store_true',
            default=None,
            help="Disable pool."
        )

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_pool_attrs(self.app.client_manager, parsed_args)
        pool_id = attrs.pop('pool_id')

        body = {'pool': attrs}

        self.app.client_manager.load_balancer.pool_set(
            pool_id, json=body)
