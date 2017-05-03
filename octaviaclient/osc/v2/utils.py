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
        if resource_name == 'project':
            if name != 'non-uuid':
                project_id = identity_common.find_project(
                    resource,
                    name
                ).id
                return project_id
            else:
                return 'non-uuid'
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
        msg = "Missing required argument: Requires one of " \
              "--vip-subnet-id, --vip-network-id or --vip-port-id"
        raise exceptions.CommandError(msg)
    elif 'vip_port_id' in attrs:
        if any(i in attrs.keys() for i in ['vip_subnet_id', 'vip_address']):
            msg = "Argument error: --port-id can not be used with " \
                  "--vip-network-id or --vip-subnet-id"
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
            if len(attr_map[k]) < 3:
                mapped_attrs[attr_map[k][0]] = attr_map[k][1](v)
            else:
                mapped_attrs[attr_map[k][0]] = get_resource_id(
                    attr_map[k][2], attr_map[k][1], v)

    return mapped_attrs
