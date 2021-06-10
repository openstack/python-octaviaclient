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

"""L7rule action implementation"""

import functools

from cliff import lister
from osc_lib.command import command
from osc_lib import exceptions
from osc_lib import utils
from osc_lib.utils import tags as _tag
from oslo_utils import uuidutils

from octaviaclient.osc.v2 import constants as const
from octaviaclient.osc.v2 import utils as v2_utils
from octaviaclient.osc.v2 import validate

COMPARE_TYPES = ['REGEX', 'EQUAL_TO', 'CONTAINS', 'ENDS_WITH', 'STARTS_WITH']
TYPES = ['FILE_TYPE', 'PATH', 'COOKIE', 'HOST_NAME', 'HEADER',
         'SSL_CONN_HAS_CERT', 'SSL_VERIFY_RESULT', 'SSL_DN_FIELD']


class CreateL7Rule(command.ShowOne):
    """Create a l7rule"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'l7policy',
            metavar='<l7policy>',
            help="l7policy to add l7rule to (name or ID)."
        )
        parser.add_argument(
            '--compare-type',
            metavar='{' + ','.join(COMPARE_TYPES) + '}',
            required=True,
            choices=COMPARE_TYPES,
            type=lambda s: s.upper(),  # case insensitive
            help="Set the compare type for the l7rule."
        )
        parser.add_argument(
            '--invert',
            action='store_true',
            default=None,
            help="Invert l7rule."
        )
        parser.add_argument(
            '--value',
            metavar='<value>',
            required=True,
            help="Set the rule value to match on."
        )
        parser.add_argument(
            '--key',
            metavar='<key>',
            help="Set the key for the l7rule's value to match on."
        )
        parser.add_argument(
            '--type',
            metavar='{' + ','.join(TYPES) + '}',
            required=True,
            choices=TYPES,
            type=lambda s: s.upper(),  # case insensitive
            help="Set the type for the l7rule."
        )
        admin_group = parser.add_mutually_exclusive_group()
        admin_group.add_argument(
            '--enable',
            action='store_true',
            default=True,
            help="Enable l7rule (default)."
        )
        admin_group.add_argument(
            '--disable',
            action='store_true',
            default=None,
            help="Disable l7rule."
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete.',
        )

        _tag.add_tag_option_to_parser_for_create(
            parser, 'l7rule')

        return parser

    def take_action(self, parsed_args):
        rows = const.L7RULE_ROWS
        attrs = v2_utils.get_l7rule_attrs(self.app.client_manager,
                                          parsed_args)
        validate.check_l7rule_attrs(attrs)

        l7policy_id = attrs.pop('l7policy_id')
        body = {"rule": attrs}
        data = self.app.client_manager.load_balancer.l7rule_create(
            l7policy_id=l7policy_id,
            json=body
        )

        if parsed_args.wait:
            l7policy = self.app.client_manager.load_balancer.l7policy_show(
                l7policy_id)
            listener = self.app.client_manager.load_balancer.listener_show(
                l7policy['listener_id'])
            v2_utils.wait_for_active(
                status_f=(self.app.client_manager.load_balancer.
                          load_balancer_show),
                res_id=listener['loadbalancers'][0]['id']
            )
            data = {
                'rule': (
                    self.app.client_manager.load_balancer.l7rule_show(
                        l7policy_id, data['rule']['id']))
            }

        formatters = {'tags': v2_utils.format_list_flat}

        return (rows, (utils.get_dict_properties(
            data['rule'], rows, formatters=formatters)))


class DeleteL7Rule(command.Command):
    """Delete a l7rule"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'l7policy',
            metavar="<l7policy>",
            help="l7policy to delete rule from (name or ID)."
        )
        parser.add_argument(
            'l7rule',
            metavar="<rule_id>",
            help="l7rule to delete."
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete.',
        )

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_l7rule_attrs(self.app.client_manager, parsed_args)

        self.app.client_manager.load_balancer.l7rule_delete(
            l7rule_id=attrs['l7rule_id'],
            l7policy_id=attrs['l7policy_id']
        )

        if parsed_args.wait:
            l7rule_show = functools.partial(
                self.app.client_manager.load_balancer.l7rule_show,
                attrs['l7rule_id']
            )
            v2_utils.wait_for_delete(
                status_f=l7rule_show,
                res_id=attrs['l7policy_id']
            )


class ListL7Rule(lister.Lister):
    """List l7rules for l7policy"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'l7policy',
            metavar='<l7policy>',
            help='l7policy to list rules for (name or ID).'
        )

        _tag.add_tag_filtering_option_to_parser(parser, 'l7rule')

        return parser

    def take_action(self, parsed_args):
        columns = const.L7RULE_COLUMNS
        attrs = v2_utils.get_l7rule_attrs(self.app.client_manager, parsed_args)

        data = self.app.client_manager.load_balancer.l7rule_list(
            **attrs
        )

        return (columns,
                (utils.get_dict_properties(
                    s, columns, formatters={}) for s in data['rules']))


class ShowL7Rule(command.ShowOne):
    """Show the details of a single l7rule"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'l7policy',
            metavar="<l7policy>",
            help="l7policy to show rule from (name or ID)."
        )
        parser.add_argument(
            'l7rule',
            metavar="<l7rule_id>",
            help="l7rule to show."
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.L7RULE_ROWS
        data = None
        if (uuidutils.is_uuid_like(parsed_args.l7policy) and
                uuidutils.is_uuid_like(parsed_args.l7rule)):
            try:
                data = self.app.client_manager.load_balancer.l7rule_show(
                    l7rule_id=parsed_args.l7rule,
                    l7policy_id=parsed_args.l7policy)
            except exceptions.NotFound:
                pass
        if data is None:
            attrs = v2_utils.get_l7rule_attrs(self.app.client_manager,
                                              parsed_args)
            data = self.app.client_manager.load_balancer.l7rule_show(
                l7rule_id=attrs['l7rule_id'],
                l7policy_id=attrs['l7policy_id']
            )
        formatters = {'tags': v2_utils.format_list_flat}

        return (rows, (utils.get_dict_properties(
            data, rows, formatters=formatters)))


class SetL7Rule(command.Command):
    """Update a l7rule"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'l7policy',
            metavar='<l7policy>',
            help="L7policy to update l7rule on (name or ID)."
        )
        parser.add_argument(
            'l7rule',
            metavar='<l7rule_id>',
            help="l7rule to update."
        )
        parser.add_argument(
            '--compare-type',
            metavar='{' + ','.join(COMPARE_TYPES) + '}',
            choices=COMPARE_TYPES,
            type=lambda s: s.upper(),  # case insensitive
            help="Set the compare type for the l7rule."
        )
        parser.add_argument(
            '--invert',
            action='store_true',
            default=None,
            help="Invert l7rule."
        )
        parser.add_argument(
            '--value',
            metavar='<value>',
            help="Set the rule value to match on."
        )
        parser.add_argument(
            '--key',
            metavar='<key>',
            help="Set the key for the l7rule's value to match on."
        )
        parser.add_argument(
            '--type',
            metavar='{' + ','.join(TYPES) + '}',
            choices=TYPES,
            type=lambda s: s.upper(),  # case insensitive
            help="Set the type for the l7rule."
        )
        admin_group = parser.add_mutually_exclusive_group()
        admin_group.add_argument(
            '--enable',
            action='store_true',
            default=None,
            help="Enable l7rule."
        )
        admin_group.add_argument(
            '--disable',
            action='store_true',
            default=None,
            help="Disable l7rule."
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete.',
        )

        _tag.add_tag_option_to_parser_for_set(parser, 'l7rule')

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_l7rule_attrs(self.app.client_manager, parsed_args)
        validate.check_l7rule_attrs(attrs)

        l7policy_id = attrs.pop('l7policy_id')
        l7rule_id = attrs.pop('l7rule_id')

        # l7rule_id is the first argument in l7rule_show
        l7rule_show = functools.partial(
            self.app.client_manager.load_balancer.l7rule_show,
            l7rule_id
        )

        v2_utils.set_tags_for_set(
            l7rule_show, l7policy_id, attrs, clear_tags=parsed_args.no_tag)

        body = {'rule': attrs}

        self.app.client_manager.load_balancer.l7rule_set(
            l7rule_id=l7rule_id,
            l7policy_id=l7policy_id,
            json=body
        )

        if parsed_args.wait:
            v2_utils.wait_for_active(
                status_f=l7rule_show,
                res_id=l7policy_id
            )


class UnsetL7Rule(command.Command):
    """Clear l7rule settings"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'l7policy',
            metavar='<l7policy>',
            help="L7policy to update (name or ID)."
        )
        parser.add_argument(
            'l7rule_id',
            metavar='<l7rule_id>',
            help="l7rule to update."
        )
        parser.add_argument(
            '--invert',
            action='store_true',
            help="Reset the l7rule invert to the API default."
        )
        parser.add_argument(
            '--key',
            action='store_true',
            help="Clear the l7rule key."
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for action to complete.',
        )
        _tag.add_tag_option_to_parser_for_unset(parser, 'l7rule')

        return parser

    def take_action(self, parsed_args):
        unset_args = v2_utils.get_unsets(parsed_args)
        if not unset_args and not parsed_args.all_tag:
            return

        policy_id = v2_utils.get_resource_id(
            self.app.client_manager.load_balancer.l7policy_list,
            'l7policies', parsed_args.l7policy)

        l7rule_show = functools.partial(
            self.app.client_manager.load_balancer.l7rule_show,
            parsed_args.l7rule_id
        )

        v2_utils.set_tags_for_unset(
            l7rule_show, policy_id, unset_args,
            clear_tags=parsed_args.all_tag)

        body = {'rule': unset_args}

        self.app.client_manager.load_balancer.l7rule_set(
            l7policy_id=policy_id, l7rule_id=parsed_args.l7rule_id, json=body)

        if parsed_args.wait:
            v2_utils.wait_for_active(
                status_f=l7rule_show,
                res_id=policy_id,
            )
