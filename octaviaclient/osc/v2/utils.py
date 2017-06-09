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

from osc_lib import exceptions

from openstackclient.identity import common as identity_common


def get_resource_id(resource, resource_name, name):
    """Converts a resource name into a UUID for consumption for the API

    :param callable resource:
        A client_manager callable
    :param resource_name:
        The resource key name for the dictonary returned
    :param name:
        The name of the resource to convert to UUID
    :return:
        The UUID of the found resource
    """
    try:
        # Projects can be non-uuid so we need to account for this
        if resource_name == 'project':
            if name != 'non-uuid':
                project_id = identity_common.find_project(
                    resource,
                    name
                ).id
                return project_id
            else:
                return 'non-uuid'
        elif resource_name == 'members':
            names = [re for re in resource(name['pool_id'])['members']
                     if re.get('id') == name['member_id']
                     or re.get('name') == name['member_id']]
            name = name['member_id']
            if len(names) > 1:
                msg = ("{0} {1} found with name or ID of {2}. Please try "
                       "again with UUID".format(len(names), resource_name,
                                                name))
                raise exceptions.CommandError(msg)
            else:
                return names[0].get('id')
        elif resource_name == 'l7rules':
            names = [re for re in resource(name['l7policy_id'])['rules']
                     if re.get('id') == name['l7rule_id']]
            name = name['l7rule_id']
            return names[0].get('id')
        else:
            names = [re for re in resource()[resource_name]
                     if re.get('name') == name or re.get('id') == name]
            if len(names) > 1:
                msg = ("{0} {1} found with name or ID of {2}. Please try "
                       "again with UUID".format(len(names), resource_name,
                                                name))
                raise exceptions.CommandError(msg)
            else:
                return names[0].get('id')
    except IndexError:
        msg = "Unable to locate {0} in {1}".format(name, resource_name)
        raise exceptions.CommandError(msg)


def get_loadbalancer_attrs(client_manager, parsed_args):
    attr_map = {
        'name': ('name', str),
        'description': ('description', str),
        'protocol': ('protocol', str),
        'loadbalancer': (
            'loadbalancer_id',
            'loadbalancers',
            client_manager.load_balancer.load_balancer_list
        ),
        'connection_limit': ('connection_limit', str),
        'protocol_port': ('protocol_port', int),
        'project': (
            'project_id',
            'project',
            client_manager.identity
        ),
        'vip_address': ('vip_address', str),
        'vip_port_id': (
            'vip_port_id',
            'ports',
            client_manager.neutronclient.list_ports
        ),
        'vip_subnet_id': (
            'vip_subnet_id',
            'subnets',
            client_manager.neutronclient.list_subnets
        ),
        'vip_network_id': (
            'vip_network_id',
            'networks',
            client_manager.neutronclient.list_networks
        ),
        'enable': ('admin_state_up', lambda x: True),
        'disable': ('admin_state_up', lambda x: False),
        'cascade': ('cascade', lambda x: True)
    }

    _attrs = vars(parsed_args)
    attrs = _map_attrs(_attrs, attr_map)

    return attrs


def check_loadbalancer_attrs(attrs):
    verify_args = ['vip_subnet_id', 'vip_network_id', 'vip_port_id']
    if not any(i in attrs.keys() for i in verify_args):
        msg = ("Missing required argument: Requires one of --vip-subnet-id, "
               "--vip-network-id or --vip-port-id")
        raise exceptions.CommandError(msg)
    elif 'vip_port_id' in attrs:
        if any(i in attrs.keys() for i in ['vip_subnet_id', 'vip_address']):
            msg = ("Argument error: --port-id can not be used with "
                   "--vip-network-id or --vip-subnet-id")
            raise exceptions.CommandError(msg)


def get_listener_attrs(client_manager, parsed_args):
    attr_map = {
        'name': ('name', str),
        'description': ('description', str),
        'protocol': ('protocol', str),
        'listener': (
            'listener_id',
            'listeners',
            client_manager.load_balancer.listener_list
        ),
        'loadbalancer': (
            'loadbalancer_id',
            'loadbalancers',
            client_manager.load_balancer.load_balancer_list
        ),
        'connection_limit': ('connection_limit', str),
        'protocol_port': ('protocol_port', int),
        'default_pool': (
            'default_pool_id',
            'pools',
            client_manager.load_balancer.pool_list
        ),
        'project': (
            'project_id',
            'project',
            client_manager.identity
        ),
        'enable': ('admin_state_up', lambda x: True),
        'disable': ('admin_state_up', lambda x: False),
        'insert_headers': ('insert_headers', _format_kv)
    }

    _attrs = vars(parsed_args)
    attrs = _map_attrs(_attrs, attr_map)

    return attrs


def get_pool_attrs(client_manager, parsed_args):
    attr_map = {
        'name': ('name', str),
        'description': ('description', str),
        'protocol': ('protocol', str),
        'pool': (
            'pool_id',
            'pools',
            client_manager.load_balancer.pool_list
        ),
        'loadbalancer': (
            'loadbalancer_id',
            'loadbalancers',
            client_manager.load_balancer.load_balancer_list
        ),
        'lb_algorithm': ('lb_algorithm', str),
        'listener': (
            'listener_id',
            'listeners',
            client_manager.load_balancer.listener_list
        ),
        'project': (
            'project_id',
            'project',
            client_manager.identity
        ),
        'session_persistence': ('session_persistence', _format_kv),
        'enable': ('admin_state_up', lambda x: True),
        'disable': ('admin_state_up', lambda x: False)
    }

    _attrs = vars(parsed_args)
    attrs = _map_attrs(_attrs, attr_map)

    return attrs


def get_member_attrs(client_manager, parsed_args):
    attr_map = {
        'name': ('name', str),
        'address': ('address', str),
        'protocol_port': ('protocol_port', int),
        'project_id': (
            'project_id',
            'project',
            client_manager.identity
        ),
        'pool': (
            'pool_id',
            'pools',
            client_manager.load_balancer.pool_list
        ),
        'member': (
            'member_id',
            'members',
            'pool',
            client_manager.load_balancer.member_list
        ),
        'weight': ('weight', int),
        'subnet_id': (
            'subnet_id',
            'subnets',
            client_manager.neutronclient.list_subnets
        ),
        'monitor_port': ('monitor_port', int),
        'monitor_address': ('monitor_address', str),
        'enable': ('admin_state_up', lambda x: True),
        'disable': ('admin_state_up', lambda x: False),
    }

    _attrs = vars(parsed_args)
    attrs = _map_attrs(_attrs, attr_map)

    return attrs


def get_l7policy_attrs(client_manager, parsed_args):
    attr_map = {
        'name': ('name', str),
        'description': ('description', str),
        'redirect_url': ('redirect_url', str),
        'l7policy': (
            'l7policy_id',
            'l7policies',
            client_manager.load_balancer.l7policy_list
        ),
        'redirect_pool': (
            'redirect_pool_id',
            'pools',
            client_manager.load_balancer.pool_list
        ),
        'listener': (
            'listener_id',
            'listeners',
            client_manager.load_balancer.listener_list
        ),
        'action': ('action', str),
        'project': (
            'project_id',
            'projects',
            client_manager.identity
        ),
        'position': ('position', int),
        'enable': ('admin_state_up', lambda x: True),
        'disable': ('admin_state_up', lambda x: False)
    }

    _attrs = vars(parsed_args)
    attrs = _map_attrs(_attrs, attr_map)

    return attrs


def check_l7policy_attrs(attrs):
    msg = None
    if attrs['action'] == 'REDIRECT_TO_POOL':
        if 'redirect_pool_id' not in attrs:
            msg = 'Missing argument: --redirect-pool'
    elif attrs['action'] == 'REDIRECT_TO_URL':
        if 'redirect_url' not in attrs:
            msg = 'Missing argument: --redirect-url'
    if msg is not None:
        raise exceptions.CommandError(msg)


def get_l7rule_attrs(client_manager, parsed_args):
    attr_map = {
        'action': ('action', str.upper),
        'project': (
            'project_id',
            'project',
            client_manager.identity
        ),
        'invert': ('invert', lambda x: True),
        'l7rule': (
            'l7rule_id',
            'l7rules',
            'l7policy',  # parent attr
            client_manager.load_balancer.l7rule_list
        ),
        'l7policy': (
            'l7policy_id',
            'l7policies',
            client_manager.load_balancer.l7policy_list
        ),
        'value': ('value', str),
        'key': ('key', str),
        'type': ('type', str),
        'compare_type': ('compare_type', str.upper),
        'enable': ('admin_state_up', lambda x: True),
        'disable': ('admin_state_up', lambda x: False)
    }

    _attrs = vars(parsed_args)
    attrs = _map_attrs(_attrs, attr_map)

    return attrs


def check_l7rule_attrs(attrs):
    msg = None
    if 'type' in attrs.keys() and attrs['type'] == 'COOKIE':
        if 'key' not in attrs:
            msg = 'Missing argument: --type COOKIE requires --key <key>'
    elif 'type' in attrs.keys() and attrs['type'] == 'HEADER':
        if 'key' not in attrs:
            msg = 'Missing argument: --type HEADER requires --key <key>'
    if msg is not None:
        raise exceptions.CommandError(msg)


def get_health_monitor_attrs(client_manager, parsed_args):
    attr_map = {
        'health_monitor': (
            'health_monitor_id',
            'healthmonitors',
            client_manager.load_balancer.health_monitor_list
        ),
        'project': (
            'project_id',
            'project',
            client_manager.identity
        ),
        'name': ('name', str),
        'pool': (
            'pool_id',
            'pools',
            client_manager.load_balancer.pool_list
        ),
        'delay': ('delay', int),
        'expected_codes': ('expected_codes', str),
        'max_retries': ('max_retries', int),
        'http_method': ('http_method', str),
        'type': ('type', str),
        'timeout': ('timeout', int),
        'max_retries_down': ('max_retries_down', int),
        'url_path': ('url_path', str),
        'enable': ('admin_state_up', lambda x: True),
        'disable': ('admin_state_up', lambda x: False)
    }

    _attrs = vars(parsed_args)
    attrs = _map_attrs(_attrs, attr_map)

    return attrs


def format_list(data):
    return '\n'.join(i['id'] for i in data)


def format_hash(data):
    if data:
        return '\n'.join('{}={}'.format(k, v) for k, v in data.items())
    else:
        return None


def _format_kv(data):
    formatted_kv = {}
    values = data.split(',')
    for value in values:
        k, v = value.split('=')
        formatted_kv[k] = v

    return formatted_kv


def _map_attrs(attrs, attr_map):
    mapped_attrs = {}
    for k, v in attrs.items():
        if v is not None and k in attr_map.keys():
            # Attributes with 2 values map directly to a callable
            if len(attr_map[k]) is 2:
                mapped_attrs[attr_map[k][0]] = attr_map[k][1](v)
            # Attributes with 3 values map directly to a resource
            elif len(attr_map[k]) is 3:
                mapped_attrs[attr_map[k][0]] = get_resource_id(
                    attr_map[k][2],
                    attr_map[k][1],
                    v
                )
            # Attributes with 4 values map to a resource with a parent
            else:
                parent = attr_map[attr_map[k][2]]
                parent_id = get_resource_id(
                    parent[2],
                    parent[1],
                    attrs[attr_map[k][2]]
                )
                child = attr_map[k]
                mapped_attrs[child[0]] = get_resource_id(
                    child[3],
                    child[1],
                    {child[0]: str(v), parent[0]: str(parent_id)}
                )

    return mapped_attrs
