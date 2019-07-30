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

"""Quota action implementation"""


from cliff import lister
from osc_lib.command import command
from osc_lib import exceptions
from osc_lib import utils

from octaviaclient.osc.v2 import constants as const
from octaviaclient.osc.v2 import utils as v2_utils


class ListQuota(lister.Lister):
    """List quotas"""

    def get_parser(self, prog_name):
        parser = super(ListQuota, self).get_parser(prog_name)

        parser.add_argument(
            '--project',
            metavar='<project-id>',
            help="Name or UUID of the project."
        )

        return parser

    def take_action(self, parsed_args):
        columns = const.QUOTA_COLUMNS
        attrs = v2_utils.get_listener_attrs(self.app.client_manager,
                                            parsed_args)
        data = self.app.client_manager.load_balancer.quota_list(**attrs)
        formatters = {'quotas': v2_utils.format_list}
        return (columns,
                (utils.get_dict_properties(s, columns, formatters=formatters)
                 for s in data['quotas']))


class ShowQuota(command.ShowOne):
    """Show the quota details for a project"""

    def get_parser(self, prog_name):
        parser = super(ShowQuota, self).get_parser(prog_name)

        parser.add_argument(
            'project',
            metavar='<project>',
            help="Name or UUID of the project."
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.QUOTA_ROWS
        attrs = v2_utils.get_quota_attrs(self.app.client_manager,
                                         parsed_args)
        project_id = attrs.pop('project_id')

        data = self.app.client_manager.load_balancer.quota_show(
            project_id=project_id
        )

        return (rows, (utils.get_dict_properties(data, rows)))


class ShowQuotaDefaults(command.ShowOne):
    """Show quota defaults"""

    def take_action(self, parsed_args):
        rows = const.QUOTA_ROWS
        data = self.app.client_manager.load_balancer.quota_defaults_show()
        return (rows, (utils.get_dict_properties(data['quota'], rows)))


class SetQuota(command.ShowOne):
    """Update a quota"""

    @staticmethod
    def _check_attrs(attrs):
        args = ['health_monitor', 'listener', 'load_balancer', 'member',
                'pool']

        if not any(arg in attrs for arg in args):
            args = [arg.replace('_', '') for arg in args]
            msg = ('Missing required argument. Requires at least one of:%s' %
                   ','.join((' --%s' % arg) for arg in args))
            raise exceptions.CommandError(msg)

    def get_parser(self, prog_name):
        parser = super(SetQuota, self).get_parser(prog_name)

        quota_group = parser.add_argument_group(
            "Quota limits",
            description='At least one of the following arguments is required.'
        )

        quota_group.add_argument(
            '--healthmonitor',
            dest='health_monitor',
            metavar='<health_monitor>',
            help=('New value for the health monitor quota. Value -1 means '
                  'unlimited.')
        )
        quota_group.add_argument(
            '--listener',
            metavar='<listener>',
            help=('New value for the listener quota. Value -1 means '
                  'unlimited.')
        )
        quota_group.add_argument(
            '--loadbalancer',
            dest='load_balancer',
            metavar='<load_balancer>',
            help=('New value for the load balancer quota limit. Value -1 '
                  'means unlimited.')
        )
        quota_group.add_argument(
            '--member',
            metavar='<member>',
            help=('New value for the member quota limit. Value -1 means '
                  'unlimited.')
        )
        quota_group.add_argument(
            '--pool',
            metavar='<pool>',
            help=('New value for the pool quota limit. Value -1 means '
                  'unlimited.')
        )

        parser.add_argument(
            'project',
            metavar='<project>',
            help="Name or UUID of the project."
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.QUOTA_ROWS
        attrs = v2_utils.get_quota_attrs(self.app.client_manager,
                                         parsed_args)
        self._check_attrs(attrs)
        project_id = attrs.pop('project_id')
        body = {'quota': attrs}

        data = self.app.client_manager.load_balancer.quota_set(project_id,
                                                               json=body)

        return (rows, (utils.get_dict_properties(data['quota'], rows)))


class ResetQuota(command.Command):
    """Resets quotas to default quotas"""

    def get_parser(self, prog_name):
        parser = super(ResetQuota, self).get_parser(prog_name)

        parser.add_argument(
            'project',
            metavar="<project>",
            help="Project to reset quotas (name or ID)"
        )

        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_quota_attrs(self.app.client_manager,
                                         parsed_args)

        project_id = attrs.pop('project_id')

        self.app.client_manager.load_balancer.quota_reset(
            project_id=project_id)


class UnsetQuota(command.Command):
    """Clear quota settings"""

    def get_parser(self, prog_name):
        parser = super(UnsetQuota, self).get_parser(prog_name)

        parser.add_argument(
            'project',
            metavar='<project>',
            help="Name or UUID of the project."
        )
        parser.add_argument(
            '--loadbalancer',
            action='store_true',
            help="Reset the load balancer quota to the default."
        )
        parser.add_argument(
            '--listener',
            action='store_true',
            help="Reset the listener quota to the default."
        )
        parser.add_argument(
            '--pool',
            action='store_true',
            help="Reset the pool quota to the default."
        )
        parser.add_argument(
            '--member',
            action='store_true',
            help="Reset the member quota to the default."
        )
        parser.add_argument(
            '--healthmonitor',
            action='store_true',
            help="Reset the health monitor quota to the default."
        )
        return parser

    def take_action(self, parsed_args):
        unset_args = v2_utils.get_unsets(parsed_args)
        if not len(unset_args):
            return

        project_id = v2_utils.get_resource_id(
            self.app.client_manager.identity,
            'project', parsed_args.project)

        body = {'quota': unset_args}

        self.app.client_manager.load_balancer.quota_set(
            project_id, json=body)
