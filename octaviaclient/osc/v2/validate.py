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

from osc_lib import exceptions


def check_l7policy_attrs(attrs):
    msg = None
    if 'action' not in attrs:
        return
    if attrs['action'] == 'REDIRECT_TO_POOL':
        if 'redirect_pool_id' not in attrs:
            msg = 'Missing argument: --redirect-pool'
    elif attrs['action'] == 'REDIRECT_TO_URL':
        if 'redirect_url' not in attrs:
            msg = 'Missing argument: --redirect-url'
    elif attrs['action'] == 'REDIRECT_PREFIX':
        if 'redirect_prefix' not in attrs:
            msg = 'Missing argument: --redirect-prefix'
    if msg is not None:
        raise exceptions.CommandError(msg)


def check_l7rule_attrs(attrs):
    if 'type' in attrs:
        if attrs['type'] in ('COOKIE', 'HEADER'):
            if 'key' not in attrs:
                msg = (
                    "Missing argument: --type {type_name} requires "
                    "--key <key>".format(type_name=attrs['type']))
                raise exceptions.CommandError(msg)
