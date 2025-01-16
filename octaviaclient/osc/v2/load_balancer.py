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
from osc_lib import exceptions
from osc_lib import utils
from osc_lib.utils import tags as _tag
from oslo_serialization import jsonutils
from oslo_utils import uuidutils

from octaviaclient.osc.v2 import constants as const
from octaviaclient.osc.v2 import utils as v2_utils

PROVISIONING_STATUS = ['ACTIVE', 'ERROR', 'PENDING_CREATE',
                       'PENDING_UPDATE', 'PENDING_DELETE']

OPERATING_STATUS = ['ONLINE', 'DRAINING', 'OFFLINE', 'DEGRADED', 'ERROR',
                    'NO_MONITOR']


class CreateLoadBalancer(command.ShowOne):
    """Create a load balancer"""

    @staticmethod
    def _check_attrs(attrs):
        verify_args = ['vip_subnet_id', 'vip_network_id', 'vip_port_id']
        if not any(i in attrs for i in verify_args):
            msg = ("Missing required argument: Requires one of "
                   "--vip-subnet-id, --vip-network-id or --vip-port-id")
            raise exceptions.CommandError(msg)
        if all(i in attrs for i in ('vip_network_id', 'vip_port_id')):
            msg = ("Argument error: --vip-port-id can not be used with "
                   "--vip-network-id")
            raise exceptions.CommandError(msg)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

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

        vip_group = parser.add_argument_group(
            "VIP Network",
            description="At least one of the following arguments is required."
        )
        vip_group.add_argument(
            '--vip-port-id',
            metavar='<vip_port_id>',
            help="Set Port for the load balancer (name or ID)."
        )
        vip_group.add_argument(
            '--vip-subnet-id',
            metavar='<vip_subnet_id>',
            help="Set subnet for the load balancer (name or ID)."
        )
        vip_group.add_argument(
            '--vip-network-id',
            metavar='<vip_network_id>',
            help="Set network for the load balancer (name or ID)."
        )
        parser.add_argument(
            '--vip-qos-policy-id',
            metavar='<vip_qos_policy_id>',
            help="Set QoS policy ID for VIP port. Unset with 'None'.",
        )
        parser.add_argument(
            '--additional-vip',
            metavar='subnet-id=<name-or-uuid>[,ip-address=<ip>]',
            action='append',
            help="Expose an additional VIP on the load balancer. This "
                 "parameter can be provided more than once."
        )
        parser.add_argument(
            '--vip-sg-id',
            metavar='<vip_sg_id>',
            action='append',
            help="Set a Custom Security Group for VIP port. This "
                 "parameter can be provided more than once."
        )

        parser.add_argument(
            '--project',
            metavar='<project>',
            help="Project for the load balancer (name or ID)."
        )

        parser.add_argument(
            '--provider',
            metavar='<provider>',
            help="Provider name for the load balancer."
        )

        parser.add_argument(
            '--availability-zone',
            metavar='<availability_zone>',
            default=None,
            help="Availability zone for the load balancer."
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
        parser.add_argument(
            '--flavor',
            metavar='<flavor>',
            help="The name or ID of the flavor for the load balancer."
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete.',
        )

        _tag.add_tag_option_to_parser_for_create(
            parser, 'load balancer')

        return parser

    def take_action(self, parsed_args):
        rows = const.LOAD_BALANCER_ROWS
        attrs = v2_utils.get_loadbalancer_attrs(self.app.client_manager,
                                                parsed_args)
        self._check_attrs(attrs)
        body = {'loadbalancer': attrs}

        data = self.app.client_manager.load_balancer.load_balancer_create(
            json=body)

        if parsed_args.wait:
            v2_utils.wait_for_active(
                status_f=(self.app.client_manager.load_balancer.
                          load_balancer_show),
                res_id=data['loadbalancer']['id']
            )
            data = {
                'loadbalancer': (
                    self.app.client_manager.load_balancer.load_balancer_show(
                        data['loadbalancer']['id']))
            }

        # Handle older API versions that did not have the vip_vnic_type
        if not data['loadbalancer'].get('vip_vnic_type', False):
            data['loadbalancer']['vip_vnic_type'] = 'normal'

        formatters = {
            'listeners': v2_utils.format_list,
            'pools': v2_utils.format_list,
            'l7policies': v2_utils.format_list,
            'tags': v2_utils.format_list_flat
        }

        return (rows,
                (utils.get_dict_properties(
                    data['loadbalancer'], rows, formatters=formatters)))


class DeleteLoadBalancer(command.Command):
    """Delete a load balancer"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'loadbalancer',
            metavar='<load_balancer>',
            help="Load balancers to delete (name or ID)."
        )
        parser.add_argument(
            '--cascade',
            action='store_true',
            default=None,
            help="Cascade the delete to all child elements of the load "
                 "balancer."
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete.',
        )

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_loadbalancer_attrs(self.app.client_manager,
                                                parsed_args)
        lb_id = attrs.pop('loadbalancer_id')

        self.app.client_manager.load_balancer.load_balancer_delete(
            lb_id=lb_id, **attrs)

        if parsed_args.wait:
            v2_utils.wait_for_delete(
                status_f=(self.app.client_manager.load_balancer.
                          load_balancer_show),
                res_id=lb_id
            )


class FailoverLoadBalancer(command.Command):
    """Trigger load balancer failover"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'loadbalancer',
            metavar='<load_balancer>',
            help="Name or UUID of the load balancer."
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete.',
        )

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_loadbalancer_attrs(self.app.client_manager,
                                                parsed_args)
        lb_id = attrs.pop('loadbalancer_id')
        self.app.client_manager.load_balancer.load_balancer_failover(
            lb_id=lb_id)

        if parsed_args.wait:
            v2_utils.wait_for_active(
                status_f=(self.app.client_manager.load_balancer.
                          load_balancer_show),
                res_id=lb_id
            )


class ListLoadBalancer(lister.Lister):
    """List load balancers"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

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
        parser.add_argument(
            '--vip-network-id',
            metavar='<vip_network_id>',
            help="List load balancers according to their VIP network "
                 "(name or ID)."
        )
        parser.add_argument(
            '--vip-subnet-id',
            metavar='<vip_subnet_id>',
            help="List load balancers according to their VIP subnet "
                 "(name or ID)."
        )
        parser.add_argument(
            '--vip-qos-policy-id',
            metavar='<vip_qos_policy_id>',
            help="List load balancers according to their VIP Qos policy "
                 "(name or ID)."
        )
        parser.add_argument(
            '--vip-port-id',
            metavar='<vip_port_id>',
            help="List load balancers according to their VIP port "
                 "(name or ID)."
        )
        parser.add_argument(
            '--provisioning-status',
            metavar='{' + ','.join(PROVISIONING_STATUS) + '}',
            choices=PROVISIONING_STATUS,
            type=lambda s: s.upper(),
            help="List load balancers according to their provisioning status."
        )
        parser.add_argument(
            '--operating-status',
            metavar='{' + ','.join(OPERATING_STATUS) + '}',
            choices=OPERATING_STATUS,
            type=lambda s: s.upper(),
            help="List load balancers according to their operating status."
        )
        parser.add_argument(
            '--provider',
            metavar='<provider>',
            help="List load balancers according to their provider."
        )
        parser.add_argument(
            '--flavor',
            metavar='<flavor>',
            help="List load balancers according to their flavor."
        )
        parser.add_argument(
            '--availability-zone',
            metavar='<availability_zone>',
            help="List load balancers according to their availability zone."
        )

        _tag.add_tag_filtering_option_to_parser(parser, 'load balancer')

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
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'loadbalancer',
            metavar='<load_balancer>',
            help="Name or UUID of the load balancer."
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.LOAD_BALANCER_ROWS
        data = None

        if uuidutils.is_uuid_like(parsed_args.loadbalancer):
            try:
                data = (
                    self.app.client_manager.load_balancer.load_balancer_show(
                        lb_id=parsed_args.loadbalancer))
            except exceptions.NotFound:
                pass

        if data is None:
            attrs = v2_utils.get_loadbalancer_attrs(
                self.app.client_manager, parsed_args)
            lb_id = attrs.pop('loadbalancer_id')

            data = self.app.client_manager.load_balancer.load_balancer_show(
                lb_id=lb_id)

        # Handle older API versions that did not have the vip_vnic_type
        if not data.get('vip_vnic_type', False):
            data['vip_vnic_type'] = 'normal'

        formatters = {
            'listeners': v2_utils.format_list,
            'pools': v2_utils.format_list,
            'l7policies': v2_utils.format_list,
            'tags': v2_utils.format_list_flat
        }

        return (rows, (utils.get_dict_properties(
            data, rows, formatters=formatters)))


class SetLoadBalancer(command.Command):
    """Update a load balancer"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'loadbalancer',
            metavar='<load_balancer>',
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
        parser.add_argument(
            '--vip-qos-policy-id',
            metavar='<vip_qos_policy_id>',
            help="Set QoS policy ID for VIP port. Unset with 'None'.",
        )
        parser.add_argument(
            '--vip-sg-id',
            metavar='<vip_sg_id>',
            action='append',
            help="Set a Custom Security Group for VIP port. This "
                 "parameter can be provided more than once."
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
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete.',
        )

        _tag.add_tag_option_to_parser_for_set(parser, 'load balancer')

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_loadbalancer_attrs(self.app.client_manager,
                                                parsed_args)
        lb_id = attrs.pop('loadbalancer_id')

        v2_utils.set_tags_for_set(
            self.app.client_manager.load_balancer.load_balancer_show,
            lb_id, attrs, clear_tags=parsed_args.no_tag)

        body = {'loadbalancer': attrs}

        self.app.client_manager.load_balancer.load_balancer_set(
            lb_id, json=body)

        if parsed_args.wait:
            v2_utils.wait_for_active(
                status_f=(self.app.client_manager.load_balancer.
                          load_balancer_show),
                res_id=lb_id
            )


class UnsetLoadBalancer(command.Command):
    """Clear load balancer settings"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'loadbalancer',
            metavar='<load_balancer>',
            help='Name or UUID of the load balancer to update.'
        )
        parser.add_argument(
            '--name',
            action='store_true',
            help="Clear the load balancer name."
        )
        parser.add_argument(
            '--description',
            action='store_true',
            help="Clear the load balancer description."
        )
        parser.add_argument(
            '--vip-qos-policy-id',
            action='store_true',
            help="Clear the load balancer QoS policy.",
        )
        parser.add_argument(
            '--vip-sg-id',
            dest='vip_sg_ids',
            action='store_true',
            help="Clear the Custom Security Groups.",
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete.',
        )

        _tag.add_tag_option_to_parser_for_unset(parser, 'load balancer')

        return parser

    def take_action(self, parsed_args):
        unset_args = v2_utils.get_unsets(parsed_args)
        if not unset_args and not parsed_args.all_tag:
            return

        lb_id = v2_utils.get_resource_id(
            self.app.client_manager.load_balancer.load_balancer_list,
            'loadbalancers', parsed_args.loadbalancer)

        v2_utils.set_tags_for_unset(
            self.app.client_manager.load_balancer.load_balancer_show,
            lb_id, unset_args, clear_tags=parsed_args.all_tag)

        body = {'loadbalancer': unset_args}

        self.app.client_manager.load_balancer.load_balancer_set(
            lb_id, json=body)

        if parsed_args.wait:
            v2_utils.wait_for_active(
                status_f=(self.app.client_manager.load_balancer.
                          load_balancer_show),
                res_id=lb_id
            )


class ShowLoadBalancerStats(command.ShowOne):
    """Shows the current statistics for a load balancer"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'loadbalancer',
            metavar='<load_balancer>',
            help="Name or UUID of the load balancer."
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.LOAD_BALANCER_STATS_ROWS
        attrs = v2_utils.get_loadbalancer_attrs(self.app.client_manager,
                                                parsed_args)
        lb_id = attrs.pop('loadbalancer_id')

        data = self.app.client_manager.load_balancer.load_balancer_stats_show(
            lb_id=lb_id
        )

        return (rows, (utils.get_dict_properties(
            data['stats'], rows, formatters={})))


class ShowLoadBalancerStatus(command.Command):
    """Display load balancer status tree in json format"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'loadbalancer',
            metavar='<load_balancer>',
            help="Name or UUID of the load balancer."
        )

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_loadbalancer_attrs(self.app.client_manager,
                                                parsed_args)
        lb_id = attrs.pop('loadbalancer_id')

        data = self.app.client_manager.load_balancer.load_balancer_status_show(
            lb_id=lb_id
        )
        res = data.get('statuses', {})
        print(jsonutils.dumps(res, indent=4))
