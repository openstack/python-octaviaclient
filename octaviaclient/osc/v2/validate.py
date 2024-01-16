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

from octaviaclient.osc.v2 import constants


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


# Handling these range validations here instead of "choices" as "choices" will
# output every possible option in the error message.
def _validate_TCP_UDP_SCTP_port_range(port_number, parameter_name):
    if (port_number < constants.MIN_PORT_NUMBER or
            port_number > constants.MAX_PORT_NUMBER):
        msg = ("Invalid input for field/attribute '{name}', Value: "
               "'{port}'. Value must be between {pmin} and {pmax}.".format(
                   name=parameter_name, port=port_number,
                   pmin=constants.MIN_PORT_NUMBER,
                   pmax=constants.MAX_PORT_NUMBER))
        raise exceptions.InvalidValue(msg)


def check_listener_attrs(attrs):
    if 'protocol_port' in attrs:
        _validate_TCP_UDP_SCTP_port_range(attrs['protocol_port'],
                                          'protocol-port')

    extra_hsts_opts_set = attrs.get('hsts_preload') or attrs.get(
        'hsts_include_subdomains')
    if extra_hsts_opts_set and 'hsts_max_age' not in attrs:
        raise exceptions.InvalidValue(
            "Argument hsts_max_age is required when using hsts_preload or "
            "hsts_include_subdomains arguments.")


def check_member_attrs(attrs):
    if 'protocol_port' in attrs:
        _validate_TCP_UDP_SCTP_port_range(attrs['protocol_port'],
                                          'protocol-port')

    if 'member_port' in attrs:
        _validate_TCP_UDP_SCTP_port_range(attrs['member_port'], 'member-port')

    if 'weight' in attrs:
        if (attrs['weight'] < constants.MIN_WEIGHT or
                attrs['weight'] > constants.MAX_WEIGHT):
            msg = ("Invalid input for field/attribute 'weight', Value: "
                   "'{weight}'. Value must be between {wmin} and "
                   "{wmax}.".format(weight=attrs['weight'],
                                    wmin=constants.MIN_WEIGHT,
                                    wmax=constants.MAX_WEIGHT))
            raise exceptions.InvalidValue(msg)
