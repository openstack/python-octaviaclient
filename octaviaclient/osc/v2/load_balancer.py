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

"""Load Balancer action implementation"""


from cliff import lister
from osc_lib.command import command
from osc_lib import utils

from octaviaclient.osc.v2 import constants as const
from octaviaclient.osc.v2 import utils as v2_utils


class CreateLoadBalancer(command.ShowOne):
    """Create a load balancer"""

    def get_parser(self, prog_name):
        parser = super(CreateLoadBalancer, self).get_parser(prog_name)

        parser.add_argument(
            '--name',
            metavar='<name>',
            help="New load balancer name."
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help="Set load balancer description."
        )
        parser.add_argument(
            '--vip-address',
            metavar='<vip_address>',
            help="Set the VIP IP Address."
        )
        parser.add_argument(
            '--vip-port-id',
            metavar='<vip_port_id>',
            help="Set Port for the load balancer (name or ID)."
        )
        parser.add_argument(
            '--vip-subnet-id',
            metavar='<vip_subnet_id>',
            help="Set subnet for the load balancer (name or ID)."
        )
        parser.add_argument(
            '--vip-network-id',
            metavar='<vip_network_id>',
            help="Set network for the load balancer (name or ID)."
        )
        parser.add_argument(
            '--project',
            metavar='<project>',
            help="Project for the load balancer (name or ID)."
        )
        admin_group = parser.add_mutually_exclusive_group()
        admin_group.add_argument(
            '--enable',
            action='store_true',
            default=True,
            help="Enable load balancer (default)."
        )
        admin_group.add_argument(
            '--disable',
            action='store_true',
            default=None,
            help="Disable load balancer."
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.LOAD_BALANCER_ROWS
        attrs = v2_utils.get_loadbalancer_attrs(self.app.client_manager,
                                                parsed_args)
        v2_utils.check_loadbalancer_attrs(attrs)
        body = {'loadbalancer': attrs}

        data = self.app.client_manager.load_balancer.load_balancer_create(
            json=body)

        formatters = {
            'listeners': v2_utils.format_list,
            'pools': v2_utils.format_list,
            'l7policies': v2_utils.format_list
        }

        return (rows,
                (utils.get_dict_properties(
                    data['loadbalancer'], rows, formatters=formatters)))


class DeleteLoadBalancer(command.Command):
    """Delete a load balancer"""

    def get_parser(self, prog_name):
        parser = super(DeleteLoadBalancer, self).get_parser(prog_name)

        parser.add_argument(
            'loadbalancer',
            metavar='<load_balancer>',
            help="Load balancers to delete (name or ID)"
        )
        parser.add_argument(
            '--cascade',
            action='store_true',
            default=None,
            help="Cascade the delete to all child elements of the load "
                 "balancer."
        )

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_loadbalancer_attrs(self.app.client_manager,
                                                parsed_args)
        lb_id = attrs.pop('loadbalancer_id')

        self.app.client_manager.load_balancer.load_balancer_delete(
            lb_id=lb_id, **attrs)


class ListLoadBalancer(lister.Lister):
    """List load balancers"""

    def get_parser(self, prog_name):
        parser = super(ListLoadBalancer, self).get_parser(prog_name)

        parser.add_argument(
            '--name',
            metavar='<name>',
            help="List load balancers according to their name."
        )
        admin_state_group = parser.add_mutually_exclusive_group()
        admin_state_group.add_argument(
            '--enable',
            action='store_true',
            default=None,
            help="List enabled load balancers."
        )
        admin_state_group.add_argument(
            '--disable',
            action='store_true',
            default=None,
            help="List disabled load balancers."
        )
        parser.add_argument(
            '--project',
            metavar='<project-id>',
            help="List load balancers according to their project (name or ID)."
        )

        return parser

    def take_action(self, parsed_args):
        columns = const.LOAD_BALANCER_COLUMNS
        attrs = v2_utils.get_loadbalancer_attrs(self.app.client_manager,
                                                parsed_args)

        data = self.app.client_manager.load_balancer.load_balancer_list(
            **attrs)

        return (columns,
                (utils.get_dict_properties(
                    s, columns,
                    formatters={},
                ) for s in data['loadbalancers']))


class ShowLoadBalancer(command.ShowOne):
    """Show the details for a single load balancer"""

    def get_parser(self, prog_name):
        parser = super(ShowLoadBalancer, self).get_parser(prog_name)

        parser.add_argument(
            'loadbalancer',
            metavar='<load_balancer>',
            help="Name or UUID of the load balancer."
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.LOAD_BALANCER_ROWS
        attrs = v2_utils.get_loadbalancer_attrs(self.app.client_manager,
                                                parsed_args)
        lb_id = attrs.pop('loadbalancer_id')

        data = self.app.client_manager.load_balancer.load_balancer_show(
            lb_id=lb_id
        )

        formatters = {
            'listeners': v2_utils.format_list,
            'pools': v2_utils.format_list,
            'l7policies': v2_utils.format_list
        }

        return (rows, (utils.get_dict_properties(
            data, rows, formatters=formatters)))


class SetLoadBalancer(command.Command):
    """Update a load balancer"""

    def get_parser(self, prog_name):
        parser = super(SetLoadBalancer, self).get_parser(prog_name)

        parser.add_argument(
            'loadbalancer',
            metavar='<load balancer>',
            help='Name or UUID of the load balancer to update.'
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help="Set load balancer name."
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help="Set load balancer description."
        )
        admin_group = parser.add_mutually_exclusive_group()
        admin_group.add_argument(
            '--enable',
            action='store_true',
            default=None,
            help="Enable load balancer."
        )
        admin_group.add_argument(
            '--disable',
            action='store_true',
            default=None,
            help="Disable load balancer."
        )

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_loadbalancer_attrs(self.app.client_manager,
                                                parsed_args)
        lb_id = attrs.pop('loadbalancer_id')
        body = {'loadbalancer': attrs}

        self.app.client_manager.load_balancer.load_balancer_set(
            lb_id, json=body)
