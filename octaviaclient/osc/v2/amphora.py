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

"""Amphora action implementation"""


from cliff import lister
from osc_lib.command import command
from osc_lib import utils

from octaviaclient.osc.v2 import constants as const
from octaviaclient.osc.v2 import utils as v2_utils


class ListAmphora(lister.Lister):
    """List amphorae"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            '--loadbalancer',
            metavar='<loadbalancer>',
            dest='loadbalancer',
            help="Filter by load balancer (name or ID).",
        )
        parser.add_argument(
            '--compute-id',
            metavar='<compute-id>',
            help="Filter by compute ID.",
        )

        role_choices = {'MASTER', 'BACKUP', 'STANDALONE'}
        parser.add_argument(
            '--role',
            metavar='{' + ','.join(sorted(role_choices)) + '}',
            choices=role_choices,
            type=lambda s: s.upper(),  # case insensitive
            help="Filter by role."
        )

        status_choices = {
            'ALLOCATED', 'BOOTING', 'DELETED', 'ERROR',
            'PENDING_CREATE', 'PENDING_DELETE', 'READY', 'FAILOVER_STOPPED',
        }
        parser.add_argument(
            '--status', '--provisioning-status',
            dest='status',
            metavar='{' + ','.join(sorted(status_choices)) + '}',
            choices=status_choices,
            type=lambda s: s.upper(),  # case insensitive
            help="Filter by amphora provisioning status."
        )

        parser.add_argument(
            '--image-id',
            metavar='<image-id>',
            help="Filter by image ID.",
        )

        parser.add_argument(
            '--long',
            action='store_true',
            help='Show additional fields.',
        )

        return parser

    def take_action(self, parsed_args):
        columns = const.AMPHORA_COLUMNS
        if parsed_args.long:
            columns = const.AMPHORA_COLUMNS_LONG

        attrs = v2_utils.get_amphora_attrs(self.app.client_manager,
                                           parsed_args)

        data = self.app.client_manager.load_balancer.amphora_list(**attrs)

        formatters = {
            'amphorae': v2_utils.format_list,
        }

        return (
            columns,
            (utils.get_dict_properties(
                amp,
                columns,
                formatters=formatters) for amp in data['amphorae']),
        )


class ShowAmphora(command.ShowOne):
    """Show the details of a single amphora"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'amphora_id',
            metavar='<amphora-id>',
            help='UUID of the amphora.',
        )

        return parser

    def take_action(self, parsed_args):

        data = self.app.client_manager.load_balancer.amphora_show(
            amphora_id=parsed_args.amphora_id,
        )

        rows = const.AMPHORA_ROWS
        formatters = {
            'loadbalancers': v2_utils.format_list,
            'amphorae': v2_utils.format_list,
        }

        return (rows, utils.get_dict_properties(data, rows,
                                                formatters=formatters))


class ConfigureAmphora(command.Command):
    """Update the amphora agent configuration"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'amphora_id',
            metavar='<amphora-id>',
            help='UUID of the amphora to configure.',
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete.',
        )

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_amphora_attrs(self.app.client_manager,
                                           parsed_args)
        amp_id = attrs.pop('amphora_id')
        self.app.client_manager.load_balancer.amphora_configure(
            amphora_id=amp_id)

        if parsed_args.wait:
            amphora = self.app.client_manager.load_balancer.amphora_show(
                amp_id)
            lb_id = amphora.get('loadbalancer_id')
            # TODO(rm_work): No status change if the amp isn't linked to an LB?
            if lb_id:
                v2_utils.wait_for_active(
                    status_f=(self.app.client_manager.load_balancer.
                              load_balancer_show),
                    res_id=lb_id
                )


class FailoverAmphora(command.Command):
    """Force failover an amphora"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'amphora_id',
            metavar='<amphora-id>',
            help='UUID of the amphora.',
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete.',
        )

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_amphora_attrs(self.app.client_manager,
                                           parsed_args)
        amp_id = attrs.pop('amphora_id')
        amphora = self.app.client_manager.load_balancer.amphora_show(amp_id)
        self.app.client_manager.load_balancer.amphora_failover(
            amphora_id=amp_id)

        if parsed_args.wait:
            lb_id = amphora.get('loadbalancer_id')
            if lb_id:
                v2_utils.wait_for_active(
                    status_f=(self.app.client_manager.load_balancer.
                              load_balancer_show),
                    res_id=lb_id
                )
            else:
                v2_utils.wait_for_delete(
                    status_f=(self.app.client_manager.load_balancer.
                              amphora_show),
                    res_id=amp_id
                )


class ShowAmphoraStats(command.ShowOne):
    """Shows the current statistics for an amphora."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            '--listener',
            metavar='<listener>',
            help='Filter by listener (name or ID).',
        )
        parser.add_argument(
            'amphora_id',
            metavar='<amphora-id>',
            help='UUID of the amphora.'
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.LOAD_BALANCER_STATS_ROWS

        listener_id = None

        if parsed_args.listener is not None:
            attrs = v2_utils.get_listener_attrs(
                self.app.client_manager,
                parsed_args)
            listener_id = attrs.pop('listener_id')

        data = self.app.client_manager.load_balancer.amphora_stats_show(
            amphora_id=parsed_args.amphora_id
        )

        total_stats = {
            key: 0
            for key in rows
        }
        for stats in data['amphora_stats']:
            if listener_id is None or listener_id == stats['listener_id']:
                for key in stats:
                    if key in rows:
                        total_stats[key] += stats[key]

        return (rows, (utils.get_dict_properties(
            total_stats, rows, formatters={})))


class DeleteAmphora(command.Command):
    """Delete a amphora"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'amphora_id',
            metavar='<amphora-id>',
            help='UUID of the amphora to delete.',
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete.',
        )

        return parser

    def take_action(self, parsed_args):

        self.app.client_manager.load_balancer.amphora_delete(
            amphora_id=parsed_args.amphora_id)

        if parsed_args.wait:
            v2_utils.wait_for_delete(
                status_f=self.app.client_manager.load_balancer.amphora_show,
                res_id=parsed_args.amphora_id, status_field=const.STATUS
            )
