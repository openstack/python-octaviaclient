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
        parser = super(ListAmphora, self).get_parser(prog_name)

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
            'PENDING_CREATE', 'PENDING_DELETE', 'READY',
        }
        parser.add_argument(
            '--status', '--provisioning-status',
            dest='status',
            metavar='{' + ','.join(sorted(status_choices)) + '}',
            choices=status_choices,
            type=lambda s: s.upper(),  # case insensitive
            help="Filter by amphora provisioning status."
        )

        return parser

    def take_action(self, parsed_args):
        columns = const.AMPHORA_COLUMNS
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
                formatters=formatters,
                ) for amp in data['amphorae']),
        )


class ShowAmphora(command.ShowOne):
    """Show the details of a single amphora"""

    def get_parser(self, prog_name):
        parser = super(ShowAmphora, self).get_parser(prog_name)

        parser.add_argument(
            'amphora_id',
            metavar='<amphora-id>',
            help='UUID of the amphora.',
        )

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_amphora_attrs(self.app.client_manager,
                                           parsed_args)

        data = self.app.client_manager.load_balancer.amphora_show(
            amphora_id=attrs.pop('amphora_id'),
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
        parser = super(ConfigureAmphora, self).get_parser(prog_name)

        parser.add_argument(
            'amphora_id',
            metavar='<amphora-id>',
            help='UUID of the amphora to configure.',
        )

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_amphora_attrs(self.app.client_manager,
                                           parsed_args)

        self.app.client_manager.load_balancer.amphora_configure(
            amphora_id=attrs.pop('amphora_id'))


class FailoverAmphora(command.Command):
    """Force failover an amphora"""

    def get_parser(self, prog_name):
        parser = super(FailoverAmphora, self).get_parser(prog_name)

        parser.add_argument(
            'amphora_id',
            metavar='<amphora-id>',
            help='UUID of the amphora.',
        )

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_amphora_attrs(self.app.client_manager,
                                           parsed_args)

        self.app.client_manager.load_balancer.amphora_failover(
            amphora_id=attrs.pop('amphora_id'))
