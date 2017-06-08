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

"""Health Monitor action implementation"""


from cliff import lister
from osc_lib.command import command
from osc_lib import utils

from octaviaclient.osc.v2 import constants as const
from octaviaclient.osc.v2 import utils as v2_utils

HTTP_METHODS = ['GET', 'POST', 'DELETE', 'PUT', 'HEAD', 'OPTIONS', 'PATCH',
                'CONNECT', 'TRACE']


class CreateHealthMonitor(command.ShowOne):
    """Create a health monitor"""

    def get_parser(self, prog_name):
        parser = super(CreateHealthMonitor, self).get_parser(prog_name)

        parser.add_argument(
            'pool',
            metavar='<pool>',
            help="Set the pool for the health monitor (name or ID)."
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help="Set the health monitor name."
        )
        parser.add_argument(
            '--delay',
            metavar='<delay>',
            required=True,
            help="Set the time in seconds, between sending probes to members."
        )
        parser.add_argument(
            '--expected-codes',
            metavar='<codes>',
            help="Set the list of HTTP status codes expected in response from "
                 "the member to declare it healthy."
        )
        parser.add_argument(
            '--http_method',
            metavar='<method>',
            choices=HTTP_METHODS,
            help="Set the HTTP method that the health monitor uses for "
                 "requests."
        )
        parser.add_argument(
            '--timeout',
            metavar='<timeout>',
            required=True,
            help="Set the maximum time, in seconds, that a monitor waits to "
                 "connect before it times out. This value must be less than "
                 "the delay value."
        )
        parser.add_argument(
            '--max-retries',
            metavar='<max_retries>',
            type=int,
            choices=range(1, 10),
            required=True,
            help="The number of successful checks before changing the "
                 "operating status of the member to ONLINE."
        )
        parser.add_argument(
            '--url-path',
            metavar='<url_path>',
            help="Set the HTTP URL path of the request sent by the monitor to "
                 "test the health of a backend member."
        )
        parser.add_argument(
            '--type',
            metavar="{'PING','HTTP','TCP','HTTPS'}",
            required=True,
            choices=['PING', 'HTTP', 'TCP', 'HTTPS'],
            help="Set the type of health monitor."
        )
        parser.add_argument(
            '--max-retries-down',
            metavar='<max_retries_down>',
            type=int,
            choices=range(1, 10),
            help="Set the number of allowed check failures before changing "
                 "the operating status of the member to ERROR."
        )
        admin_group = parser.add_mutually_exclusive_group()
        admin_group.add_argument(
            '--enable',
            action='store_true',
            default=True,
            help="Enable health monitor (default)."
        )
        admin_group.add_argument(
            '--disable',
            action='store_true',
            default=None,
            help="Disable health monitor."
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.MONITOR_ROWS
        attrs = v2_utils.get_health_monitor_attrs(self.app.client_manager,
                                                  parsed_args)
        body = {"healthmonitor": attrs}
        data = self.app.client_manager.load_balancer.health_monitor_create(
            json=body)

        formatters = {'pools': v2_utils.format_list}

        return (rows,
                (utils.get_dict_properties(data['healthmonitor'],
                                           rows,
                                           formatters=formatters)))


class DeleteHealthMonitor(command.Command):
    """Delete a health monitor"""

    def get_parser(self, prog_name):
        parser = super(DeleteHealthMonitor, self).get_parser(prog_name)

        parser.add_argument(
            'health_monitor',
            metavar='<health_monitor>',
            help="Health monitor to delete (name or ID)."
        )

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_health_monitor_attrs(self.app.client_manager,
                                                  parsed_args)

        health_monitor_id = attrs.pop('health_monitor_id')

        self.app.client_manager.load_balancer.health_monitor_delete(
            health_monitor_id=health_monitor_id)


class ListHealthMonitor(lister.Lister):
    """List health monitors"""

    def get_parser(self, prog_name):
        parser = super(ListHealthMonitor, self).get_parser(prog_name)

        return parser

    def take_action(self, parsed_args):
        columns = const.MONITOR_COLUMNS
        attrs = v2_utils.get_health_monitor_attrs(self.app.client_manager,
                                                  parsed_args)
        data = self.app.client_manager.load_balancer.health_monitor_list(
            **attrs)

        formatters = {'pools': v2_utils.format_list}
        return (columns,
                (utils.get_dict_properties(s, columns, formatters=formatters)
                 for s in data['healthmonitors']))


class ShowHealthMonitor(command.ShowOne):
    """Show the details of a single health monitor"""

    def get_parser(self, prog_name):
        parser = super(ShowHealthMonitor, self).get_parser(prog_name)

        parser.add_argument(
            'health_monitor',
            metavar='<health_monitor>',
            help='Name or UUID of the health monitor.'
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.MONITOR_ROWS
        attrs = v2_utils.get_health_monitor_attrs(self.app.client_manager,
                                                  parsed_args)

        health_monitor_id = attrs.pop('health_monitor_id')

        data = self.app.client_manager.load_balancer.health_monitor_show(
            health_monitor_id=health_monitor_id,
        )
        formatters = {'pools': v2_utils.format_list}

        return (rows,
                (utils.get_dict_properties(data, rows, formatters=formatters)))


class SetHealthMonitor(command.Command):
    """Update a health monitor"""

    def get_parser(self, prog_name):
        parser = super(SetHealthMonitor, self).get_parser(prog_name)

        parser.add_argument(
            'health_monitor',
            metavar='<health_monitor>',
            help="Health monitor to update (name or ID)."
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help="Set health monitor name."
        )
        parser.add_argument(
            '--delay',
            metavar='<delay>',
            help="Set the time in seconds, between sending probes to members."
        )
        parser.add_argument(
            '--expected-codes',
            metavar='<codes>',
            help="Set the list of HTTP status codes expected in response from "
                 "the member to declare it healthy."
        )
        parser.add_argument(
            '--http_method',
            metavar='<method>',
            choices=HTTP_METHODS,
            help="Set the HTTP method that the health monitor uses for "
                 "requests."
        )
        parser.add_argument(
            '--timeout',
            metavar='<timeout>',
            help="Set the maximum time, in seconds, that a monitor waits to "
                 "connect before it times out. This value must be less than "
                 "the delay value."
        )
        parser.add_argument(
            '--max-retries',
            metavar='<max_retries>',
            type=int,
            choices=range(1, 10),
            help="Set the number of successful checks before changing the "
                 "operating status of the member to ONLINE."
        )
        parser.add_argument(
            '--max-retries-down',
            metavar='<max_retries_down>',
            type=int,
            choices=range(1, 10),
            help="Set the number of allowed check failures before changing "
                 "the operating status of the member to ERROR."
        )
        parser.add_argument(
            '--url-path',
            metavar='<url_path>',
            help="Set the HTTP URL path of the request sent by the monitor to "
                 "test the health of a backend member."
        )
        admin_group = parser.add_mutually_exclusive_group()
        admin_group.add_argument(
            '--enable',
            action='store_true',
            default=None,
            help="Enable health monitor."
        )
        admin_group.add_argument(
            '--disable',
            action='store_true',
            default=None,
            help="Disable health monitor."
        )

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_health_monitor_attrs(self.app.client_manager,
                                                  parsed_args)

        listener_id = attrs.pop('health_monitor_id')

        body = {'healthmonitor': attrs}

        self.app.client_manager.load_balancer.health_monitor_set(
            listener_id, json=body)
