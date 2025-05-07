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

"""Listener action implementation"""
import argparse

from cliff import lister
from osc_lib.command import command
from osc_lib import exceptions
from osc_lib import utils
from osc_lib.utils import tags as _tag
from oslo_utils import uuidutils

from octaviaclient.osc.v2 import constants as const
from octaviaclient.osc.v2 import utils as v2_utils
from octaviaclient.osc.v2 import validate

PROTOCOL_CHOICES = ['TCP', 'HTTP', 'HTTPS', 'TERMINATED_HTTPS', 'UDP', 'SCTP',
                    'PROMETHEUS']
CLIENT_AUTH_CHOICES = ['NONE', 'OPTIONAL', 'MANDATORY']


class CreateListener(command.ShowOne):
    """Create a listener"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'loadbalancer',
            metavar='<loadbalancer>',
            help="Load balancer for the listener (name or ID)."
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help="Set the listener name."
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help="Set the description of this listener."
        )
        parser.add_argument(
            '--protocol',
            metavar='{' + ','.join(PROTOCOL_CHOICES) + '}',
            choices=PROTOCOL_CHOICES,
            type=lambda s: s.upper(),  # case insensitive
            required=True,
            help="The protocol for the listener."
        )
        parser.add_argument(
            '--connection-limit',
            type=int,
            metavar='<limit>',
            help="Set the maximum number of connections permitted for this "
                 "listener."
        )
        parser.add_argument(
            '--default-pool',
            metavar='<pool>',
            help="Set the name or ID of the pool used by the listener if no "
                 "L7 policies match."
        )
        parser.add_argument(
            '--default-tls-container-ref',
            metavar='<container_ref>',
            help="The URI to the key manager service secrets container "
                 "containing the certificate and key for TERMINATED_TLS "
                 "listeners."
        )
        parser.add_argument(
            '--sni-container-refs',
            metavar='<container_ref>',
            nargs='*',
            help="A list of URIs to the key manager service secrets "
                 "containers containing the certificates and keys for "
                 "TERMINATED_TLS the listener using Server Name Indication."
        )
        parser.add_argument(
            '--insert-headers',
            metavar='<header=value,...>',
            help="A dictionary of optional headers to insert into the request "
                 "before it is sent to the backend member."
        )
        parser.add_argument(
            '--protocol-port',
            metavar='<port>',
            required=True,
            type=int,
            help="Set the protocol port number for the listener."
        )
        parser.add_argument(
            '--timeout-client-data',
            type=int,
            metavar='<timeout>',
            help="Frontend client inactivity timeout in milliseconds. "
                 "Default: 50000."
        )
        parser.add_argument(
            '--timeout-member-connect',
            type=int,
            metavar='<timeout>',
            help="Backend member connection timeout in milliseconds. "
                 "Default: 5000."
        )
        parser.add_argument(
            '--timeout-member-data',
            type=int,
            metavar='<timeout>',
            help="Backend member inactivity timeout in milliseconds. "
                 "Default: 50000."
        )
        parser.add_argument(
            '--timeout-tcp-inspect',
            type=int,
            metavar='<timeout>',
            help="Time, in milliseconds, to wait for additional TCP packets "
                 "for content inspection. Default: 0."
        )
        admin_group = parser.add_mutually_exclusive_group()
        admin_group.add_argument(
            '--enable',
            action='store_true',
            default=True,
            help="Enable listener (default)."
        )
        admin_group.add_argument(
            '--disable',
            action='store_true',
            default=None,
            help="Disable listener."
        )
        parser.add_argument(
            '--client-ca-tls-container-ref',
            metavar='<container_ref>',
            help="The URI to the key manager service secrets container "
                 "containing the CA certificate for TERMINATED_TLS listeners."
        )
        parser.add_argument(
            '--client-authentication',
            metavar='{' + ','.join(CLIENT_AUTH_CHOICES) + '}',
            choices=CLIENT_AUTH_CHOICES,
            type=lambda s: s.upper(),  # case insensitive
            help="The TLS client authentication verify options for "
                 "TERMINATED_TLS listeners."
        )
        parser.add_argument(
            '--client-crl-container-ref',
            metavar='<client_crl_container_ref>',
            help="The URI to the key manager service secrets container "
                 "containting the CA revocation list file for TERMINATED_TLS "
                 "listeners."
        )
        parser.add_argument(
            '--allowed-cidr',
            dest='allowed_cidrs',
            metavar='<allowed_cidr>',
            nargs='?',
            action='append',
            help="CIDR to allow access to the listener (can be set multiple "
                 "times)."
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete.',
        )
        parser.add_argument(
            '--tls-ciphers',
            metavar='<tls_ciphers>',
            help="Set the TLS ciphers to be used "
                 "by the listener in OpenSSL format."
        )
        parser.add_argument(
            '--tls-version',
            dest='tls_versions',
            metavar='<tls_versions>',
            nargs='?',
            action='append',
            help="Set the TLS protocol version to be used "
                 "by the listener (can be set multiple times)."
        )
        parser.add_argument(
            '--alpn-protocol',
            dest='alpn_protocols',
            metavar='<alpn_protocols>',
            nargs='?',
            action='append',
            help="Set the ALPN protocol to be used "
                 "by the listener (can be set multiple times)."
        )
        parser.add_argument(
            '--hsts-max-age',
            dest='hsts_max_age',
            metavar='<hsts_max_age>',
            type=int,
            help="The value of the max_age directive for the "
                 "Strict-Transport-Security HTTP response header. "
                 "Setting this enables HTTP Strict Transport "
                 "Security (HSTS) for the TLS-terminated listener."
        )
        parser.add_argument(
            '--hsts-include-subdomains',
            action='store_true',
            dest='hsts_include_subdomains',
            default=None,
            help="Define whether the includeSubDomains directive should be "
                 "added to the Strict-Transport-Security HTTP response "
                 "header."
        )
        parser.add_argument(
            '--hsts-preload',
            action='store_true',
            dest='hsts_preload',
            default=None,
            help="Define whether the preload directive should be "
                 "added to the Strict-Transport-Security HTTP response "
                 "header."
        )

        _tag.add_tag_option_to_parser_for_create(
            parser, 'listener')

        return parser

    def take_action(self, parsed_args):
        rows = const.LISTENER_ROWS
        attrs = v2_utils.get_listener_attrs(self.app.client_manager,
                                            parsed_args)

        validate.check_listener_attrs(attrs)

        body = {"listener": attrs}
        data = self.app.client_manager.load_balancer.listener_create(
            json=body)

        if parsed_args.wait:
            v2_utils.wait_for_active(
                status_f=(self.app.client_manager.load_balancer.
                          load_balancer_show),
                res_id=data['listener']['loadbalancers'][0]['id']
            )
            data = {
                'listener': (
                    self.app.client_manager.load_balancer.listener_show(
                        data['listener']['id']))
            }

        formatters = {'loadbalancers': v2_utils.ListColumn,
                      'pools': v2_utils.ListColumn,
                      'l7policies': v2_utils.ListColumn,
                      'insert_headers': v2_utils.HashColumn,
                      'allowed_cidrs': v2_utils.FlatListColumn,
                      'tags': v2_utils.FlatListColumn}

        return (rows,
                (utils.get_dict_properties(data['listener'],
                                           rows,
                                           formatters=formatters)))


class DeleteListener(command.Command):
    """Delete a listener"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'listener',
            metavar="<listener>",
            help="Listener to delete (name or ID)."
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete.',
        )

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_listener_attrs(self.app.client_manager,
                                            parsed_args)

        listener_id = attrs.pop('listener_id')

        self.app.client_manager.load_balancer.listener_delete(
            listener_id=listener_id)

        if parsed_args.wait:
            v2_utils.wait_for_delete(
                status_f=self.app.client_manager.load_balancer.listener_show,
                res_id=listener_id
            )


class ListListener(lister.Lister):
    """List listeners"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            '--name',
            metavar='<name>',
            help="List listeners by listener name."
        )
        parser.add_argument(
            '--loadbalancer',
            metavar='<loadbalancer>',
            help="Filter by load balancer (name or ID).",
        )

        admin_group = parser.add_mutually_exclusive_group()
        admin_group.add_argument(
            '--enable',
            action='store_true',
            default=None,
            help="List enabled listeners."
        )
        admin_group.add_argument(
            '--disable',
            action='store_true',
            default=None,
            help="List disabled listeners."
        )

        parser.add_argument(
            '--project',
            metavar='<project>',
            help="List listeners by project ID."
        )

        _tag.add_tag_filtering_option_to_parser(parser, 'listener')

        return parser

    def take_action(self, parsed_args):
        columns = const.LISTENER_COLUMNS
        attrs = v2_utils.get_listener_attrs(self.app.client_manager,
                                            parsed_args)
        data = self.app.client_manager.load_balancer.listener_list(**attrs)
        formatters = {'loadbalancers': v2_utils.ListColumn}
        return (columns,
                (utils.get_dict_properties(s, columns, formatters=formatters)
                 for s in data['listeners']))


class ShowListener(command.ShowOne):
    """Show the details of a single listener"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'listener',
            metavar='<listener>',
            help='Name or UUID of the listener.'
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.LISTENER_ROWS
        data = None
        if uuidutils.is_uuid_like(parsed_args.listener):
            try:
                data = self.app.client_manager.load_balancer.listener_show(
                    listener_id=parsed_args.listener)
            except exceptions.NotFound:
                pass
        if data is None:
            attrs = v2_utils.get_listener_attrs(self.app.client_manager,
                                                parsed_args)

            listener_id = attrs.pop('listener_id')

            data = self.app.client_manager.load_balancer.listener_show(
                listener_id=listener_id,
            )
        formatters = {'loadbalancers': v2_utils.ListColumn,
                      'pools': v2_utils.ListColumn,
                      'l7policies': v2_utils.ListColumn,
                      'insert_headers': v2_utils.HashColumn,
                      'allowed_cidrs': v2_utils.FlatListColumn,
                      'tags': v2_utils.FlatListColumn}

        return rows, utils.get_dict_properties(data, rows,
                                               formatters=formatters)


class SetListener(command.Command):
    """Update a listener"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'listener',
            metavar="<listener>",
            help="Listener to modify (name or ID)."
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help="Set the listener name."
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help="Set the description of this listener."
        )
        parser.add_argument(
            '--connection-limit',
            metavar='<limit>',
            help="The maximum number of connections permitted for this "
                 "listener. Default value is -1 which represents infinite "
                 "connections."
        )
        parser.add_argument(
            '--default-pool',
            metavar='<pool>',
            help="The ID of the pool used by the listener if no L7 policies "
                 "match."
        )
        parser.add_argument(
            '--default-tls-container-ref',
            metavar='<container-ref>',
            help="The URI to the key manager service secrets container "
                 "containing the certificate and key for TERMINATED_TLS "
                 "listeners."
        )
        parser.add_argument(
            '--sni-container-refs',
            metavar='<container-ref>',
            nargs='*',
            help="A list of URIs to the key manager service secrets "
                 "containers containing the certificates and keys for "
                 "TERMINATED_TLS the listener using Server Name Indication."
        )
        parser.add_argument(
            '--insert-headers',
            metavar='<header=value>',
            help="A dictionary of optional headers to insert into the request "
                 "before it is sent to the backend member."
        )
        parser.add_argument(
            '--timeout-client-data',
            type=int,
            metavar='<timeout>',
            help="Frontend client inactivity timeout in milliseconds. "
                 "Default: 50000."
        )
        parser.add_argument(
            '--timeout-member-connect',
            type=int,
            metavar='<timeout>',
            help="Backend member connection timeout in milliseconds. "
                 "Default: 5000."
        )
        parser.add_argument(
            '--timeout-member-data',
            type=int,
            metavar='<timeout>',
            help="Backend member inactivity timeout in milliseconds. "
                 "Default: 50000."
        )
        parser.add_argument(
            '--timeout-tcp-inspect',
            type=int,
            metavar='<timeout>',
            help="Time, in milliseconds, to wait for additional TCP packets "
                 "for content inspection. Default: 0."
        )
        admin_group = parser.add_mutually_exclusive_group()
        admin_group.add_argument(
            '--enable',
            action='store_true',
            default=None,
            help="Enable listener."
        )
        admin_group.add_argument(
            '--disable',
            action='store_true',
            default=None,
            help="Disable listener."
        )
        parser.add_argument(
            '--client-ca-tls-container-ref',
            metavar='<container_ref>',
            help="The URI to the key manager service secrets container "
                 "containing the CA certificate for TERMINATED_TLS listeners."
        )
        parser.add_argument(
            '--client-authentication',
            metavar='{' + ','.join(CLIENT_AUTH_CHOICES) + '}',
            choices=CLIENT_AUTH_CHOICES,
            type=lambda s: s.upper(),  # case insensitive
            help="The TLS client authentication verify options for "
                 "TERMINATED_TLS listeners."
        )
        parser.add_argument(
            '--client-crl-container-ref',
            metavar='<client_crl_container_ref>',
            help="The URI to the key manager service secrets container "
                 "containting the CA revocation list file for TERMINATED_TLS "
                 "listeners."
        )
        parser.add_argument(
            '--allowed-cidr',
            dest='allowed_cidrs',
            metavar='<allowed_cidr>',
            nargs='?',
            action='append',
            help="CIDR to allow access to the listener (can be set multiple "
                 "times)."
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete.',
        )
        parser.add_argument(
            '--tls-ciphers',
            metavar='<tls_ciphers>',
            help="Set the TLS ciphers to be used "
                 "by the listener in OpenSSL format."
        )
        parser.add_argument(
            '--tls-version',
            dest='tls_versions',
            metavar='<tls_versions>',
            nargs='?',
            action='append',
            help="Set the TLS protocol version to be used "
                 "by the listener (can be set multiple times)."
        )
        parser.add_argument(
            '--alpn-protocol',
            dest='alpn_protocols',
            metavar='<alpn_protocols>',
            nargs='?',
            action='append',
            help="Set the ALPN protocol to be used "
                 "by the listener (can be set multiple times)."
        )
        parser.add_argument(
            '--hsts-max-age',
            dest='hsts_max_age',
            metavar='<hsts_max_age>',
            type=int,
            default=argparse.SUPPRESS,
            help="The value of the max_age directive for the "
                 "Strict-Transport-Security HTTP response header. "
                 "Setting this enables HTTP Strict Transport "
                 "Security (HSTS) for the TLS-terminated listener."
        )
        parser.add_argument(
            '--hsts-include-subdomains',
            action='store_true',
            default=argparse.SUPPRESS,
            dest='hsts_include_subdomains',
            help="Defines whether the includeSubDomains directive should be "
                 "added to the Strict-Transport-Security HTTP response "
                 "header."
        )
        parser.add_argument(
            '--hsts-preload',
            action='store_true',
            default=argparse.SUPPRESS,
            dest='hsts_preload',
            help="Defines whether the preload directive should be "
                 "added to the Strict-Transport-Security HTTP response "
                 "header."
        )

        _tag.add_tag_option_to_parser_for_set(parser, 'listener')

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_listener_attrs(self.app.client_manager,
                                            parsed_args)

        listener_id = attrs.pop('listener_id')

        v2_utils.set_tags_for_set(
            self.app.client_manager.load_balancer.listener_show,
            listener_id, attrs, clear_tags=parsed_args.no_tag)

        body = {'listener': attrs}

        self.app.client_manager.load_balancer.listener_set(
            listener_id, json=body)

        if parsed_args.wait:
            v2_utils.wait_for_active(
                status_f=self.app.client_manager.load_balancer.listener_show,
                res_id=listener_id
            )


class UnsetListener(command.Command):
    """Clear listener settings"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'listener',
            metavar="<listener>",
            help="Listener to modify (name or ID)."
        )
        parser.add_argument(
            '--name',
            action='store_true',
            help="Clear the listener name."
        )
        parser.add_argument(
            '--description',
            action='store_true',
            help="Clear the description of this listener."
        )
        parser.add_argument(
            '--connection-limit',
            action='store_true',
            help="Reset the connection limit to the API default."
        )
        parser.add_argument(
            '--default-pool',
            dest='default_pool_id',
            action='store_true',
            help="Clear the default pool from the listener."
        )
        parser.add_argument(
            '--default-tls-container-ref',
            action='store_true',
            help="Remove the default TLS container reference from the "
                 "listener."
        )
        parser.add_argument(
            '--sni-container-refs',
            action='store_true',
            help="Remove the TLS SNI container references from the listener."
        )
        parser.add_argument(
            '--insert-headers',
            action='store_true',
            help="Clear the insert headers from the listener."
        )
        parser.add_argument(
            '--timeout-client-data',
            action='store_true',
            help="Reset the client data timeout to the API default."
        )
        parser.add_argument(
            '--timeout-member-connect',
            action='store_true',
            help="Reset the member connect timeout to the API default."
        )
        parser.add_argument(
            '--timeout-member-data',
            action='store_true',
            help="Reset the member data timeout to the API default."
        )
        parser.add_argument(
            '--timeout-tcp-inspect',
            action='store_true',
            help="Reset the TCP inspection timeout to the API default."
        )
        parser.add_argument(
            '--client-ca-tls-container-ref',
            action='store_true',
            help="Clear the client CA TLS container reference from the "
                 "listener."
        )
        parser.add_argument(
            '--client-authentication',
            action='store_true',
            help="Reset the client authentication setting to the API default."
        )
        parser.add_argument(
            '--client-crl-container-ref',
            action='store_true',
            help="Clear the client CRL container reference from the listener."
        )
        parser.add_argument(
            '--allowed-cidrs',
            action='store_true',
            help="Clear all allowed CIDRs from the listener."
        )
        parser.add_argument(
            '--tls-versions',
            action='store_true',
            help='Clear all TLS versions from the listener.',
        )
        parser.add_argument(
            '--tls-ciphers',
            action='store_true',
            help='Clear all TLS ciphers from the listener.',
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete.',
        )
        parser.add_argument(
            '--alpn-protocols',
            action='store_true',
            help="Clear all ALPN protocols from the listener."
        )
        parser.add_argument(
            '--hsts-max-age',
            dest='hsts_max_age',
            action='store_true',
            help="Disables HTTP Strict Transport "
                 "Security (HSTS) for the TLS-terminated listener."
        )
        parser.add_argument(
            '--hsts-include-subdomains',
            action='store_true',
            dest='hsts_include_subdomains',
            help="Removes the includeSubDomains directive from the "
                 "Strict-Transport-Security HTTP response header."
        )
        parser.add_argument(
            '--hsts-preload',
            action='store_true',
            dest='hsts_preload',
            help="Removes the preload directive from the "
                 "Strict-Transport-Security HTTP response header."
        )
        _tag.add_tag_option_to_parser_for_unset(parser, 'listener')

        return parser

    def take_action(self, parsed_args):
        unset_args = v2_utils.get_unsets(parsed_args)
        if not unset_args and not parsed_args.all_tag:
            return

        listener_id = v2_utils.get_resource_id(
            self.app.client_manager.load_balancer.listener_list,
            'listeners', parsed_args.listener)

        v2_utils.set_tags_for_unset(
            self.app.client_manager.load_balancer.listener_show,
            listener_id, unset_args, clear_tags=parsed_args.all_tag)

        body = {'listener': unset_args}

        self.app.client_manager.load_balancer.listener_set(
            listener_id, json=body)

        if parsed_args.wait:
            v2_utils.wait_for_active(
                status_f=self.app.client_manager.load_balancer.listener_show,
                res_id=listener_id
            )


class ShowListenerStats(command.ShowOne):
    """Shows the current statistics for a listener."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'listener',
            metavar='<listener>',
            help='Name or UUID of the listener.'
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.LOAD_BALANCER_STATS_ROWS
        attrs = v2_utils.get_listener_attrs(self.app.client_manager,
                                            parsed_args)

        listener_id = attrs.pop('listener_id')

        data = self.app.client_manager.load_balancer.listener_stats_show(
            listener_id=listener_id,
        )

        return (rows, (utils.get_dict_properties(
            data['stats'], rows, formatters={})))
