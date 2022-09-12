#   Copyright 2017 GoDaddy
#   Copyright 2019 Red Hat, Inc. All rights reserved.
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
from osc_lib import exceptions
from osc_lib import utils
from osc_lib.utils import tags as _tag
from oslo_utils import uuidutils

from octaviaclient.osc.v2 import constants as const
from octaviaclient.osc.v2 import utils as v2_utils

PROTOCOL_CHOICES = ['TCP', 'HTTP', 'HTTPS', 'PROXY', 'PROXYV2', 'UDP',
                    'SCTP']
ALGORITHM_CHOICES = ['SOURCE_IP', 'ROUND_ROBIN', 'LEAST_CONNECTIONS',
                     'SOURCE_IP_PORT']


class CreatePool(command.ShowOne):
    """Create a pool"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

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
            metavar='{' + ','.join(PROTOCOL_CHOICES) + '}',
            required=True,
            choices=PROTOCOL_CHOICES,
            type=lambda s: s.upper(),  # case insensitive
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
            help="Load balancer to add the pool to (name or ID)."
        )
        parser.add_argument(
            '--session-persistence',
            metavar='<session persistence>',
            help="Set the session persistence for the listener (key=value)."
        )
        parser.add_argument(
            '--lb-algorithm',
            metavar='{' + ','.join(ALGORITHM_CHOICES) + '}',
            required=True,
            choices=ALGORITHM_CHOICES,
            type=lambda s: s.upper(),  # case insensitive
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
        parser.add_argument(
            '--tls-container-ref',
            metavar='<container-ref>',
            help="The reference to the key manager service secrets container "
                 "containing the certificate and key for ``tls_enabled`` "
                 "pools to re-encrpt the traffic to backend member servers."
        )
        parser.add_argument(
            '--ca-tls-container-ref',
            metavar='<ca_tls_container_ref>',
            help="The reference to the key manager service secrets container "
                 "containing the CA certificate for ``tls_enabled`` pools "
                 "to check the backend member servers certificates."
        )
        parser.add_argument(
            '--crl-container-ref',
            metavar='<crl_container_ref>',
            help="The reference to the key manager service secrets container "
                 "containting the CA revocation list file for ``tls_enabled`` "
                 "pools to validate the backend member servers certificates."
        )
        tls_enable = parser.add_mutually_exclusive_group()
        tls_enable.add_argument(
            '--enable-tls',
            action='store_true',
            default=None,
            help="Enable backend member re-encryption."
        )
        tls_enable.add_argument(
            '--disable-tls',
            action='store_true',
            default=None,
            help="Disable backend member re-encryption."
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete.',
        )
        parser.add_argument(
            '--tls-ciphers',
            metavar='<tls_ciphers>',
            help="Set the TLS ciphers to be used by the pool "
                 "in OpenSSL cipher string format."
        )
        parser.add_argument(
            '--tls-version',
            dest='tls_versions',
            metavar='<tls_versions>',
            nargs='?',
            action='append',
            help="Set the TLS protocol version to be used "
                 "by the pool (can be set multiple times)."
        )
        parser.add_argument(
            '--alpn-protocol',
            dest='alpn_protocols',
            metavar='<alpn_protocols>',
            nargs='?',
            action='append',
            help="Set the ALPN protocol to be used "
                 "by the pool (can be set multiple times)."
        )

        _tag.add_tag_option_to_parser_for_create(
            parser, 'pool')

        return parser

    def take_action(self, parsed_args):
        rows = const.POOL_ROWS
        attrs = v2_utils.get_pool_attrs(self.app.client_manager, parsed_args)

        body = {"pool": attrs}
        data = self.app.client_manager.load_balancer.pool_create(
            json=body)

        if parsed_args.wait:
            v2_utils.wait_for_active(
                status_f=(self.app.client_manager.load_balancer.
                          load_balancer_show),
                res_id=data['pool']['loadbalancers'][0]['id']
            )
            data = {
                'pool': (
                    self.app.client_manager.load_balancer.pool_show(
                        data['pool']['id']))
            }

        formatters = {'loadbalancers': v2_utils.format_list,
                      'members': v2_utils.format_list,
                      'listeners': v2_utils.format_list,
                      'session_persistence': v2_utils.format_hash,
                      'tags': v2_utils.format_list_flat}

        return (rows, (utils.get_dict_properties(
            data['pool'], rows, formatters=formatters,
            mixed_case_fields=['enable-tls'])))


class DeletePool(command.Command):
    """Delete a pool"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'pool',
            metavar="<pool>",
            help="Pool to delete (name or ID)."
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete.',
        )

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_pool_attrs(self.app.client_manager, parsed_args)
        pool_id = attrs.pop('pool_id')
        self.app.client_manager.load_balancer.pool_delete(
            pool_id=pool_id)

        if parsed_args.wait:
            v2_utils.wait_for_delete(
                status_f=self.app.client_manager.load_balancer.pool_show,
                res_id=pool_id
            )


class ListPool(lister.Lister):
    """List pools"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            '--loadbalancer',
            metavar='<loadbalancer>',
            help="Filter by load balancer (name or ID).",
        )

        _tag.add_tag_filtering_option_to_parser(parser, 'pool')

        return parser

    def take_action(self, parsed_args):
        columns = const.POOL_COLUMNS
        attrs = v2_utils.get_pool_attrs(self.app.client_manager, parsed_args)
        data = self.app.client_manager.load_balancer.pool_list(**attrs)
        formatters = {'loadbalancers': v2_utils.format_list,
                      'members': v2_utils.format_list,
                      'listeners': v2_utils.format_list}

        return (columns,
                (utils.get_dict_properties(
                    s, columns, formatters=formatters) for s in data['pools']))


class ShowPool(command.ShowOne):
    """Show the details of a single pool"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'pool',
            metavar='<pool>',
            help='Name or UUID of the pool.'
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.POOL_ROWS
        data = None
        if uuidutils.is_uuid_like(parsed_args.pool):
            try:
                data = self.app.client_manager.load_balancer.pool_show(
                    pool_id=parsed_args.pool)
            except exceptions.NotFound:
                pass
        if data is None:
            attrs = v2_utils.get_pool_attrs(self.app.client_manager,
                                            parsed_args)
            pool_id = attrs.pop('pool_id')

            data = self.app.client_manager.load_balancer.pool_show(
                pool_id=pool_id,
            )
        formatters = {'loadbalancers': v2_utils.format_list,
                      'members': v2_utils.format_list,
                      'listeners': v2_utils.format_list,
                      'session_persistence': v2_utils.format_hash,
                      'tags': v2_utils.format_list_flat}

        return (rows, (utils.get_dict_properties(
            data, rows, formatters=formatters,
            mixed_case_fields=['enable-tls'])))


class SetPool(command.Command):
    """Update a pool"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

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
            metavar='{' + ','.join(ALGORITHM_CHOICES) + '}',
            choices=ALGORITHM_CHOICES,
            type=lambda s: s.upper(),  # case insensitive
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
        parser.add_argument(
            '--tls-container-ref',
            metavar='<container-ref>',
            help="The URI to the key manager service secrets container "
                 "containing the certificate and key for TERMINATED_TLS "
                 "pools to re-encrpt the traffic from TERMINATED_TLS "
                 "listener to backend servers."
        )
        parser.add_argument(
            '--ca-tls-container-ref',
            metavar='<ca_tls_container_ref>',
            help="The URI to the key manager service secrets container "
                 "containing the CA certificate for TERMINATED_TLS listeners "
                 "to check the backend servers certificates in ssl traffic."
        )
        parser.add_argument(
            '--crl-container-ref',
            metavar='<crl_container_ref>',
            help="The URI to the key manager service secrets container "
                 "containting the CA revocation list file for TERMINATED_TLS "
                 "listeners to valid the backend servers certificates in ssl "
                 "traffic."
        )
        tls_enable = parser.add_mutually_exclusive_group()
        tls_enable.add_argument(
            '--enable-tls',
            action='store_true',
            default=None,
            help="Enable backend associated members re-encryption."
        )
        tls_enable.add_argument(
            '--disable-tls',
            action='store_true',
            default=None,
            help="disable backend associated members re-encryption."
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete.',
        )
        parser.add_argument(
            '--tls-ciphers',
            metavar='<tls_ciphers>',
            help="Set the TLS ciphers to be used by the pool "
                 "in OpenSSL cipher string format."
        )
        parser.add_argument(
            '--tls-version',
            dest='tls_versions',
            metavar='<tls_versions>',
            nargs='?',
            action='append',
            help="Set the TLS protocol version to be used "
                 "by the pool (can be set multiple times)."
        )
        parser.add_argument(
            '--alpn-protocol',
            dest='alpn_protocols',
            metavar='<alpn_protocols>',
            nargs='?',
            action='append',
            help="Set the ALPN protocol to be used "
                 "by the pool (can be set multiple times)."
        )

        _tag.add_tag_option_to_parser_for_set(parser, 'pool')

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_pool_attrs(self.app.client_manager, parsed_args)
        pool_id = attrs.pop('pool_id')

        v2_utils.set_tags_for_set(
            self.app.client_manager.load_balancer.pool_show,
            pool_id, attrs, clear_tags=parsed_args.no_tag)

        body = {'pool': attrs}

        self.app.client_manager.load_balancer.pool_set(
            pool_id, json=body)

        if parsed_args.wait:
            v2_utils.wait_for_active(
                status_f=self.app.client_manager.load_balancer.pool_show,
                res_id=pool_id
            )


class UnsetPool(command.Command):
    """Clear pool settings"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'pool',
            metavar="<pool>",
            help="Pool to modify (name or ID)."
        )
        parser.add_argument(
            '--name',
            action='store_true',
            help="Clear the pool name."
        )
        parser.add_argument(
            '--description',
            action='store_true',
            help="Clear the description of this pool."
        )
        parser.add_argument(
            '--ca-tls-container-ref',
            action='store_true',
            help="Clear the certificate authority certificate reference on "
                 "this pool."
        )
        parser.add_argument(
            '--crl-container-ref',
            action='store_true',
            help="Clear the certificate revocation list reference on "
                 "this pool."
        )
        parser.add_argument(
            '--session-persistence',
            action='store_true',
            help="Disables session persistence on the pool."
        )
        parser.add_argument(
            '--tls-container-ref',
            action='store_true',
            help="Clear the certificate reference for this pool."
        )
        parser.add_argument(
            '--tls-versions',
            action='store_true',
            help='Clear all TLS versions from the pool.',
        )
        parser.add_argument(
            '--tls-ciphers',
            action='store_true',
            help='Clear all TLS ciphers from the pool.',
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete.',
        )
        parser.add_argument(
            '--alpn-protocols',
            action='store_true',
            help="Clear all ALPN protocols from the pool."
        )

        _tag.add_tag_option_to_parser_for_unset(parser, 'pool')

        return parser

    def take_action(self, parsed_args):
        unset_args = v2_utils.get_unsets(parsed_args)
        if not unset_args and not parsed_args.all_tag:
            return

        pool_id = v2_utils.get_resource_id(
            self.app.client_manager.load_balancer.pool_list,
            'pools', parsed_args.pool)

        v2_utils.set_tags_for_unset(
            self.app.client_manager.load_balancer.pool_show,
            pool_id, unset_args, clear_tags=parsed_args.all_tag)

        body = {'pool': unset_args}

        self.app.client_manager.load_balancer.pool_set(
            pool_id, json=body)

        if parsed_args.wait:
            v2_utils.wait_for_active(
                status_f=self.app.client_manager.load_balancer.pool_show,
                res_id=pool_id
            )
