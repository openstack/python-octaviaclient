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

"""L7rule action implementation"""

from cliff import lister
from osc_lib.command import command
from osc_lib import utils

from octaviaclient.osc.v2 import constants as const
from octaviaclient.osc.v2 import utils as v2_utils

COMPARE_TYPES = ['REGEX', 'EQUAL_TO', 'CONTAINS', 'ENDS_WITH', 'STARTS_WITH']
TYPES = ['FILE_TYPE', 'PATH', 'COOKIE', 'HOST_NAME', 'HEADER']


class CreateL7Rule(command.ShowOne):
    """Create a l7rule"""

    def get_parser(self, prog_name):
        parser = super(CreateL7Rule, self).get_parser(prog_name)
        parser.add_argument(
            'l7policy',
            metavar='<l7policy>',
            help="l7policy to add l7rule to (name or ID)."
        )
        parser.add_argument(
            '--compare-type',
            metavar="{REGEX,EQUAL_TO,CONTAINS,ENDS_WITH,STARTS_WITH}",
            required=True,
            choices=COMPARE_TYPES,
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
            metavar="{FILE_TYPE,PATH,COOKIE,HOST_NAME,HEADER}",
            required=True,
            choices=TYPES,
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

        return parser

    def take_action(self, parsed_args):
        rows = const.L7RULE_ROWS
        attrs = v2_utils.get_l7rule_attrs(self.app.client_manager,
                                          parsed_args)
        v2_utils.check_l7rule_attrs(attrs)

        l7policy_id = attrs.pop('l7policy_id')
        body = {"rule": attrs}
        data = self.app.client_manager.load_balancer.l7rule_create(
            l7policy_id=l7policy_id,
            json=body
        )

        return (rows, (utils.get_dict_properties(
            data['rule'], rows, formatters={})))


class DeleteL7Rule(command.Command):
    """Delete a l7rule"""

    def get_parser(self, prog_name):
        parser = super(DeleteL7Rule, self).get_parser(prog_name)

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

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_l7rule_attrs(self.app.client_manager, parsed_args)

        self.app.client_manager.load_balancer.l7rule_delete(
            l7rule_id=attrs['l7rule_id'],
            l7policy_id=attrs['l7policy_id']
        )


class ListL7Rule(lister.Lister):
    """List l7rules for l7policy"""

    def get_parser(self, prog_name):
        parser = super(ListL7Rule, self).get_parser(prog_name)

        parser.add_argument(
            'l7policy',
            metavar='<l7policy>',
            help='l7policy to list rules for (name or ID).'
        )

        return parser

    def take_action(self, parsed_args):
        columns = const.L7RULE_COLUMNS
        attrs = v2_utils.get_l7rule_attrs(self.app.client_manager, parsed_args)

        data = self.app.client_manager.load_balancer.l7rule_list(
            l7policy_id=attrs['l7policy_id']
        )

        return (columns,
                (utils.get_dict_properties(
                    s, columns, formatters={}) for s in data['rules']))


class ShowL7Rule(command.ShowOne):
    """Show the details of a single l7rule"""

    def get_parser(self, prog_name):
        parser = super(ShowL7Rule, self).get_parser(prog_name)

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

        attrs = v2_utils.get_l7rule_attrs(self.app.client_manager, parsed_args)
        data = self.app.client_manager.load_balancer.l7rule_show(
            l7rule_id=attrs['l7rule_id'],
            l7policy_id=attrs['l7policy_id']
        )

        return (rows, (utils.get_dict_properties(
            data, rows, formatters={})))


class SetL7Rule(command.Command):
    """Update a l7rule"""

    def get_parser(self, prog_name):
        parser = super(SetL7Rule, self).get_parser(prog_name)

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
            metavar="{REGEX,EQUAL_TO,CONTAINS,ENDS_WITH,STARTS_WITH}",
            choices=COMPARE_TYPES,
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
            metavar="{FILE_TYPE,PATH,COOKIE,HOST_NAME,HEADER}",
            choices=TYPES,
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

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_l7rule_attrs(self.app.client_manager, parsed_args)
        v2_utils.check_l7rule_attrs(attrs)

        l7policy_id = attrs.pop('l7policy_id')
        l7rule_id = attrs.pop('l7rule_id')

        body = {'rule': attrs}

        self.app.client_manager.load_balancer.l7rule_set(
            l7rule_id=l7rule_id,
            l7policy_id=l7policy_id,
            json=body
        )
