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

"""L7policy action implementation"""

from cliff import lister
from osc_lib.command import command
from osc_lib import exceptions
from osc_lib import utils
from osc_lib.utils import tags as _tag
from oslo_utils import uuidutils

from octaviaclient.osc.v2 import constants as const
from octaviaclient.osc.v2 import utils as v2_utils
from octaviaclient.osc.v2 import validate

ACTION_CHOICES = ['REDIRECT_TO_URL', 'REDIRECT_TO_POOL',
                  'REDIRECT_PREFIX', 'REJECT']
REDIRECT_CODE_CHOICES = [301, 302, 303, 307, 308]


class CreateL7Policy(command.ShowOne):
    """Create a l7policy"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'listener',
            metavar='<listener>',
            help="Listener to add l7policy to (name or ID)."
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help="Set the l7policy name."
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help="Set l7policy description."
        )

        parser.add_argument(
            '--action',
            metavar='{' + ','.join(ACTION_CHOICES) + '}',
            required=True,
            choices=ACTION_CHOICES,
            type=lambda s: s.upper(),  # case insensitive
            help="Set the action of the policy."
        )

        redirect_group = parser.add_mutually_exclusive_group()
        redirect_group.add_argument(
            '--redirect-pool',
            metavar='<pool>',
            help="Set the pool to redirect requests to (name or ID)."
        )
        redirect_group.add_argument(
            '--redirect-url',
            metavar='<url>',
            help="Set the URL to redirect requests to."
        )
        redirect_group.add_argument(
            '--redirect-prefix',
            metavar='<url>',
            help="Set the URL Prefix to redirect requests to."
        )

        parser.add_argument(
            '--redirect-http-code',
            metavar='<redirect_http_code>',
            choices=REDIRECT_CODE_CHOICES,
            type=int,
            help="Set the HTTP response code for REDIRECT_URL or "
                 "REDIRECT_PREFIX action."
        )
        parser.add_argument(
            '--position',
            metavar='<position>',
            type=int,
            help="Sequence number of this L7 Policy."
        )
        admin_group = parser.add_mutually_exclusive_group()
        admin_group.add_argument(
            '--enable',
            action='store_true',
            default=True,
            help="Enable l7policy (default)."
        )
        admin_group.add_argument(
            '--disable',
            action='store_true',
            default=None,
            help="Disable l7policy."
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete.',
        )

        _tag.add_tag_option_to_parser_for_create(
            parser, 'l7policy')

        return parser

    def take_action(self, parsed_args):
        rows = const.L7POLICY_ROWS
        attrs = v2_utils.get_l7policy_attrs(self.app.client_manager,
                                            parsed_args)
        validate.check_l7policy_attrs(attrs)
        body = {"l7policy": attrs}

        data = self.app.client_manager.load_balancer.l7policy_create(
            json=body)

        if parsed_args.wait:
            listener = self.app.client_manager.load_balancer.listener_show(
                data['l7policy']['listener_id'])
            v2_utils.wait_for_active(
                status_f=(self.app.client_manager.load_balancer.
                          load_balancer_show),
                res_id=listener['loadbalancers'][0]['id']
            )
            data = {
                'l7policy': (
                    self.app.client_manager.load_balancer.l7policy_show(
                        data['l7policy']['id']))
            }

        formatters = {'rules': v2_utils.ListColumn,
                      'tags': v2_utils.FlatListColumn}

        return (rows, (utils.get_dict_properties(
            data['l7policy'], rows, formatters=formatters)))


class DeleteL7Policy(command.Command):
    """Delete a l7policy"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'l7policy',
            metavar="<policy>",
            help="l7policy to delete (name or ID)."
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete.',
        )

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_l7policy_attrs(self.app.client_manager,
                                            parsed_args)

        l7policy_id = attrs.pop('l7policy_id')

        self.app.client_manager.load_balancer.l7policy_delete(
            l7policy_id=l7policy_id)

        if parsed_args.wait:
            v2_utils.wait_for_delete(
                status_f=(self.app.client_manager.load_balancer.
                          l7policy_show),
                res_id=l7policy_id
            )


class ListL7Policy(lister.Lister):
    """List l7policies"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            '--listener',
            help="List l7policies that applied to the given listener "
                 "(name or ID)."
        )

        _tag.add_tag_filtering_option_to_parser(parser, 'l7policy')

        return parser

    def take_action(self, parsed_args):
        columns = const.L7POLICY_COLUMNS

        attrs = v2_utils.get_l7policy_attrs(self.app.client_manager,
                                            parsed_args)

        data = self.app.client_manager.load_balancer.l7policy_list(**attrs)
        formatters = {'rules': v2_utils.ListColumn}

        return (columns,
                (utils.get_dict_properties(
                    s, columns,
                    formatters=formatters) for s in data['l7policies']))


class ShowL7Policy(command.ShowOne):
    """Show the details of a single l7policy"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'l7policy',
            metavar='<policy>',
            help='Name or UUID of the l7policy.'
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.L7POLICY_ROWS
        data = None
        if uuidutils.is_uuid_like(parsed_args.l7policy):
            try:
                data = self.app.client_manager.load_balancer.l7policy_show(
                    l7policy_id=parsed_args.l7policy)
            except exceptions.NotFound:
                pass
        if data is None:
            attrs = v2_utils.get_l7policy_attrs(self.app.client_manager,
                                                parsed_args)

            l7policy_id = attrs.pop('l7policy_id')

            data = self.app.client_manager.load_balancer.l7policy_show(
                l7policy_id=l7policy_id,
            )
        formatters = {'rules': v2_utils.ListColumn,
                      'tags': v2_utils.FlatListColumn}

        return (rows, (utils.get_dict_properties(
            data, rows, formatters=formatters)))


class SetL7Policy(command.Command):
    """Update a l7policy"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'l7policy',
            metavar='<policy>',
            help="L7policy to update (name or ID)."
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help="Set l7policy name."
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help="Set l7policy description."
        )
        parser.add_argument(
            '--action',
            metavar='{' + ','.join(ACTION_CHOICES) + '}',
            choices=ACTION_CHOICES,
            type=lambda s: s.upper(),  # case insensitive
            help="Set the action of the policy."
        )

        redirect_group = parser.add_mutually_exclusive_group()
        redirect_group.add_argument(
            '--redirect-pool',
            metavar='<pool>',
            help="Set the pool to redirect requests to (name or ID)."
        )
        redirect_group.add_argument(
            '--redirect-url',
            metavar='<url>',
            help="Set the URL to redirect requests to."
        )
        redirect_group.add_argument(
            '--redirect-prefix',
            metavar='<url>',
            help="Set the URL Prefix to redirect requests to."
        )
        parser.add_argument(
            '--redirect-http-code',
            metavar='<redirect_http_code>',
            choices=REDIRECT_CODE_CHOICES,
            type=int,
            help="Set the HTTP response code for REDIRECT_URL or "
                 "REDIRECT_PREFIX action."
        )
        parser.add_argument(
            '--position',
            metavar='<position>',
            type=int,
            help="Set sequence number of this L7 Policy."
        )
        admin_group = parser.add_mutually_exclusive_group()
        admin_group.add_argument(
            '--enable',
            action='store_true',
            default=None,
            help="Enable l7policy."
        )
        admin_group.add_argument(
            '--disable',
            action='store_true',
            default=None,
            help="Disable l7policy."
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete.',
        )

        _tag.add_tag_option_to_parser_for_set(parser, 'l7policy')

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_l7policy_attrs(self.app.client_manager,
                                            parsed_args)

        validate.check_l7policy_attrs(attrs)
        l7policy_id = attrs.pop('l7policy_id')

        v2_utils.set_tags_for_set(
            self.app.client_manager.load_balancer.l7policy_show,
            l7policy_id, attrs, clear_tags=parsed_args.no_tag)

        body = {'l7policy': attrs}

        self.app.client_manager.load_balancer.l7policy_set(
            l7policy_id, json=body)

        if parsed_args.wait:
            v2_utils.wait_for_active(
                status_f=(self.app.client_manager.load_balancer.
                          l7policy_show),
                res_id=l7policy_id
            )


class UnsetL7Policy(command.Command):
    """Clear l7policy settings"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'l7policy',
            metavar='<policy>',
            help="L7policy to update (name or ID)."
        )
        parser.add_argument(
            '--description',
            action='store_true',
            help="Clear the l7policy description."
        )
        parser.add_argument(
            '--name',
            action='store_true',
            help="Clear the l7policy name."
        )
        parser.add_argument(
            '--redirect-http-code',
            action='store_true',
            help="Clear the l7policy redirect HTTP code."
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete.',
        )

        _tag.add_tag_option_to_parser_for_unset(parser, 'l7policy')

        return parser

    def take_action(self, parsed_args):
        unset_args = v2_utils.get_unsets(parsed_args)
        if not unset_args and not parsed_args.all_tag:
            return

        policy_id = v2_utils.get_resource_id(
            self.app.client_manager.load_balancer.l7policy_list,
            'l7policies', parsed_args.l7policy)

        v2_utils.set_tags_for_unset(
            self.app.client_manager.load_balancer.l7policy_show,
            policy_id, unset_args, clear_tags=parsed_args.all_tag)

        body = {'l7policy': unset_args}

        self.app.client_manager.load_balancer.l7policy_set(
            policy_id, json=body)

        if parsed_args.wait:
            v2_utils.wait_for_active(
                status_f=(self.app.client_manager.load_balancer.
                          l7policy_show),
                res_id=policy_id
            )
