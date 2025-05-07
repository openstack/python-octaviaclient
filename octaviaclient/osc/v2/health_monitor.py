#   Copyright 2017 GoDaddy
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

"""Health Monitor action implementation"""


from cliff import lister
from osc_lib.command import command
from osc_lib import exceptions
from osc_lib import utils
from osc_lib.utils import tags as _tag
from oslo_utils import uuidutils

from octaviaclient.osc.v2 import constants as const
from octaviaclient.osc.v2 import utils as v2_utils

HTTP_METHODS = ['GET', 'POST', 'DELETE', 'PUT', 'HEAD', 'OPTIONS', 'PATCH',
                'CONNECT', 'TRACE']
HTTP_VERSIONS = [1.0, 1.1]
TYPE_CHOICES = ['PING', 'HTTP', 'TCP', 'HTTPS', 'TLS-HELLO',
                'UDP-CONNECT', 'SCTP']


class CreateHealthMonitor(command.ShowOne):
    """Create a health monitor"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

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
            '--domain-name',
            metavar='<domain_name>',
            help=("Set the domain name, which be injected into the HTTP Host "
                  "Header to the backend server for HTTP health check.")
        )
        parser.add_argument(
            '--expected-codes',
            metavar='<codes>',
            help="Set the list of HTTP status codes expected in response from "
                 "the member to declare it healthy."
        )
        parser.add_argument(
            '--http-method',
            metavar='{' + ','.join(HTTP_METHODS) + '}',
            choices=HTTP_METHODS,
            type=lambda s: s.upper(),  # case insensitive
            help="Set the HTTP method that the health monitor uses for "
                 "requests."
        )
        parser.add_argument(
            '--http-version',
            metavar='<http_version>',
            choices=HTTP_VERSIONS,
            type=float,
            help="Set the HTTP version."
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
            metavar='{' + ','.join(TYPE_CHOICES) + '}',
            required=True,
            choices=TYPE_CHOICES,
            type=lambda s: s.upper(),  # case insensitive
            help="Set the health monitor type."
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
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete.',
        )

        _tag.add_tag_option_to_parser_for_create(
            parser, 'health monitor')

        return parser

    def take_action(self, parsed_args):
        rows = const.MONITOR_ROWS
        attrs = v2_utils.get_health_monitor_attrs(self.app.client_manager,
                                                  parsed_args)
        body = {"healthmonitor": attrs}
        data = self.app.client_manager.load_balancer.health_monitor_create(
            json=body)

        if parsed_args.wait:
            pool = self.app.client_manager.load_balancer.pool_show(
                data['healthmonitor']['pools'][0]['id'])
            v2_utils.wait_for_active(
                status_f=(self.app.client_manager.load_balancer.
                          load_balancer_show),
                res_id=pool['loadbalancers'][0]['id']
            )
            data = {
                'healthmonitor': (
                    self.app.client_manager.load_balancer.health_monitor_show(
                        data['healthmonitor']['id']))
            }

        formatters = {'pools': v2_utils.ListColumn,
                      'tags': v2_utils.FlatListColumn}

        return (rows,
                (utils.get_dict_properties(data['healthmonitor'],
                                           rows,
                                           formatters=formatters)))


class DeleteHealthMonitor(command.Command):
    """Delete a health monitor"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'health_monitor',
            metavar='<health_monitor>',
            help="Health monitor to delete (name or ID)."
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete.',
        )

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_health_monitor_attrs(self.app.client_manager,
                                                  parsed_args)

        health_monitor_id = attrs.pop('health_monitor_id')

        self.app.client_manager.load_balancer.health_monitor_delete(
            health_monitor_id=health_monitor_id)

        if parsed_args.wait:
            v2_utils.wait_for_delete(
                status_f=(self.app.client_manager.load_balancer.
                          health_monitor_show),
                res_id=health_monitor_id
            )


class ListHealthMonitor(lister.Lister):
    """List health monitors"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        _tag.add_tag_filtering_option_to_parser(parser, 'health monitor')

        return parser

    def take_action(self, parsed_args):
        columns = const.MONITOR_COLUMNS
        attrs = v2_utils.get_health_monitor_attrs(self.app.client_manager,
                                                  parsed_args)
        data = self.app.client_manager.load_balancer.health_monitor_list(
            **attrs)

        formatters = {'pools': v2_utils.ListColumn}
        return (columns,
                (utils.get_dict_properties(s, columns, formatters=formatters)
                 for s in data['healthmonitors']))


class ShowHealthMonitor(command.ShowOne):
    """Show the details of a single health monitor"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'health_monitor',
            metavar='<health_monitor>',
            help='Name or UUID of the health monitor.'
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.MONITOR_ROWS
        data = None
        if uuidutils.is_uuid_like(parsed_args.health_monitor):
            try:
                data = (
                    self.app.client_manager.load_balancer.health_monitor_show(
                        health_monitor_id=parsed_args.health_monitor))
            except exceptions.NotFound:
                pass
        if data is None:
            attrs = v2_utils.get_health_monitor_attrs(self.app.client_manager,
                                                      parsed_args)

            health_monitor_id = attrs.pop('health_monitor_id')

            data = self.app.client_manager.load_balancer.health_monitor_show(
                health_monitor_id=health_monitor_id,
            )
        formatters = {'pools': v2_utils.ListColumn,
                      'tags': v2_utils.FlatListColumn}

        return (rows,
                (utils.get_dict_properties(data, rows, formatters=formatters)))


class SetHealthMonitor(command.Command):
    """Update a health monitor"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

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
            '--domain-name',
            metavar='<domain_name>',
            help=("Set the domain name, which be injected into the HTTP Host "
                  "Header to the backend server for HTTP health check.")
        )
        parser.add_argument(
            '--expected-codes',
            metavar='<codes>',
            help="Set the list of HTTP status codes expected in response from "
                 "the member to declare it healthy."
        )
        parser.add_argument(
            '--http-method',
            metavar='{' + ','.join(HTTP_METHODS) + '}',
            choices=HTTP_METHODS,
            type=lambda s: s.upper(),  # case insensitive
            help="Set the HTTP method that the health monitor uses for "
                 "requests."
        )
        parser.add_argument(
            '--http-version',
            metavar='<http_version>',
            choices=HTTP_VERSIONS,
            type=float,
            help="Set the HTTP version."
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
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete.',
        )

        _tag.add_tag_option_to_parser_for_set(parser, 'health monitor')

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_health_monitor_attrs(self.app.client_manager,
                                                  parsed_args)

        hm_id = attrs.pop('health_monitor_id')

        v2_utils.set_tags_for_set(
            self.app.client_manager.load_balancer.health_monitor_show,
            hm_id, attrs, clear_tags=parsed_args.no_tag)

        body = {'healthmonitor': attrs}

        self.app.client_manager.load_balancer.health_monitor_set(
            hm_id, json=body)

        if parsed_args.wait:
            v2_utils.wait_for_active(
                status_f=(self.app.client_manager.load_balancer.
                          health_monitor_show),
                res_id=hm_id
            )


class UnsetHealthMonitor(command.Command):
    """Clear health monitor settings"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'health_monitor',
            metavar='<health_monitor>',
            help="Health monitor to update (name or ID)."
        )
        parser.add_argument(
            '--domain-name',
            action='store_true',
            help="Clear the health monitor domain name."
        )
        parser.add_argument(
            '--expected-codes',
            action='store_true',
            help="Reset the health monitor expected codes to the API default."
        )
        parser.add_argument(
            '--http-method',
            action='store_true',
            help="Reset the health monitor HTTP method to the API default."
        )
        parser.add_argument(
            '--http-version',
            action='store_true',
            help="Reset the health monitor HTTP version to the API default."
        )
        parser.add_argument(
            '--max-retries-down',
            action='store_true',
            help="Reset the health monitor max retries down to the API "
                 "default."
        )
        parser.add_argument(
            '--name',
            action='store_true',
            help="Clear the health monitor name."
        )
        parser.add_argument(
            '--url-path',
            action='store_true',
            help="Clear the health monitor URL path."
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete.',
        )

        _tag.add_tag_option_to_parser_for_unset(parser, 'health monitor')

        return parser

    def take_action(self, parsed_args):
        unset_args = v2_utils.get_unsets(parsed_args)
        if not unset_args and not parsed_args.all_tag:
            return

        hm_id = v2_utils.get_resource_id(
            self.app.client_manager.load_balancer.health_monitor_list,
            'healthmonitors', parsed_args.health_monitor)

        v2_utils.set_tags_for_unset(
            self.app.client_manager.load_balancer.health_monitor_show,
            hm_id, unset_args, clear_tags=parsed_args.all_tag)

        body = {'healthmonitor': unset_args}

        self.app.client_manager.load_balancer.health_monitor_set(
            hm_id, json=body)

        if parsed_args.wait:
            v2_utils.wait_for_active(
                status_f=(self.app.client_manager.load_balancer.
                          health_monitor_show),
                res_id=hm_id
            )
