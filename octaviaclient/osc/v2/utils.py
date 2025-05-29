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

import functools
import ipaddress

from cliff import columns
from openstackclient.identity import common as identity_common
from osc_lib import exceptions as osc_exc
from osc_lib import utils
from oslo_utils import uuidutils

from octaviaclient.api import exceptions
from octaviaclient.osc.v2 import constants


def _map_attrs(args, source_attr_map):
    res = {}
    for k, v in args.items():
        if (v is None) or (k not in source_attr_map):
            continue
        source_val = source_attr_map[k]
        # Attributes with 2 values map directly to a callable
        if len(source_val) == 2:
            res[source_val[0]] = source_val[1](v)
        # Attributes with 3 values map directly to a resource
        elif len(source_val) == 3:
            if not isinstance(v, list):
                res[source_val[0]] = get_resource_id(
                    source_val[2],
                    source_val[1],
                    v,
                )
            else:
                res[source_val[0]] = [get_resource_id(
                    source_val[2],
                    source_val[1],
                    x,
                ) for x in v]

        # Attributes with 4 values map to a resource with a parent
        elif len(source_val) == 4:
            parent = source_attr_map[source_val[2]]
            parent_id = get_resource_id(
                parent[2],
                parent[1],
                args[source_val[2]],
            )
            child = source_val
            res[child[0]] = get_resource_id(
                child[3],
                child[1],
                {child[0]: str(v), parent[0]: str(parent_id)},
            )
    return res


def _find_resource(list_funct, resource_name, root_tag, name, parent=None):
    """Search for a resource by name and ID.

    This function will search for a resource by both the name and ID,
    returning the resource once it finds a match. If no match is found,
    an exception will be raised.

    :param list_funct: The resource list method to call during searches.
    :param resource_name: The name of the resource type we are searching for.
    :param root_tag: The root tag of the resource returned from the API.
    :param name: The value we are searching for, a resource name or ID.
    :param parent: The parent resource ID, when required.
    :return: The resource found for the name or ID.
    :raises osc_exc.CommandError: If more than one match or none are found.
    """
    if parent:
        parent_args = [parent]
    else:
        parent_args = []
    # Optimize the API call order if we got a UUID-like name or not
    if uuidutils.is_uuid_like(name):
        # Try by ID first
        resource = list_funct(*parent_args, id=name)[root_tag]
        if len(resource) == 1:
            return resource[0]

        # Try by name next
        resource = list_funct(*parent_args, name=name)[root_tag]
        if len(resource) == 1:
            return resource[0]
        if len(resource) > 1:
            msg = ("{0} {1} found with name or ID of {2}. Please try "
                   "again with UUID".format(len(resource), resource_name,
                                            name))
            raise osc_exc.CommandError(msg)
    else:
        # Try by name first
        resource = list_funct(*parent_args, name=name)[root_tag]
        if len(resource) == 1:
            return resource[0]
        if len(resource) > 1:
            msg = ("{0} {1} found with name or ID of {2}. Please try "
                   "again with UUID".format(len(resource), resource_name,
                                            name))
            raise osc_exc.CommandError(msg)

        # Try by ID next
        # Availability Zones don't support the id parameter
        if resource_name != "availability_zones":
            resource = list_funct(*parent_args, id=name)[root_tag]
            if len(resource) == 1:
                return resource[0]

    # We didn't find what we were looking for, raise a consistent error.
    msg = "Unable to locate {0} in {1}".format(name, resource_name)
    raise osc_exc.CommandError(msg)


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
        # Allow None as a value
        if resource_name in ('policies',):
            if name.lower() in ('none', 'null', 'void'):
                return None

        primary_key = 'id'
        # Availability-zones don't have an id value
        if resource_name == 'availability_zones':
            primary_key = 'name'

        # Projects can be non-uuid so we need to account for this
        if resource_name == 'project':
            if name != 'non-uuid':
                project_id = identity_common.find_project(
                    resource,
                    name
                ).id
                return project_id
            return 'non-uuid'

        if resource_name == 'members':
            member = _find_resource(resource, resource_name, 'members',
                                    name['member_id'], parent=name['pool_id'])
            return member.get('id')

        if resource_name == 'l7rules':
            l7rule = _find_resource(resource, resource_name, 'rules',
                                    name['l7rule_id'],
                                    parent=name['l7policy_id'])
            return l7rule.get('id')

        resource = _find_resource(resource, resource_name, resource_name, name)
        return resource.get(primary_key)

    except IndexError as e:
        msg = "Unable to locate {0} in {1}".format(name, resource_name)
        raise osc_exc.CommandError(msg) from e


def add_tags_attr_map(attr_map):
    tags_attr_map = {
        'tags': ('tags', list),
        'any_tags': ('tags-any', list),
        'not_tags': ('not-tags', list),
        'not_any_tags': ('not-tags-any', list),
    }
    attr_map.update(tags_attr_map)


def validate_vip_dict(vip_dict, client_manager):
    # We have validation in two places -- _map_attrs checks sub-resources, and
    # later _check_attrs does further api-specific validation. We need both for
    # additional vips, so we may as well just do both here while we're at it.
    if 'subnet_id' not in vip_dict:
        raise osc_exc.CommandError(
            'Additional VIPs must include a subnet-id.')
    subnet_id = get_resource_id(client_manager.neutronclient.list_subnets,
                                'subnets', vip_dict['subnet_id'])
    vip_dict['subnet_id'] = subnet_id
    if 'ip_address' in vip_dict:
        try:
            ipaddress.ip_address(vip_dict['ip_address'])
        except ValueError as e:
            raise osc_exc.CommandError(str(e))


def handle_additional_vips(vips, client_manager):
    additional_vips = []
    for vip in vips:
        vip_dict = {}
        parts = vip.split(',')
        for part in parts:
            k, v = part.split('=')
            vip_dict[k.replace('-', '_')] = v
        validate_vip_dict(vip_dict, client_manager)
        additional_vips.append(vip_dict)

    return additional_vips


def handle_vip_sg_ids(vip_sgs, client_manager):
    vip_sg_ids = []
    for sg in vip_sgs:
        sg_id = get_resource_id(
            client_manager.neutronclient.list_security_groups,
            'security_groups', sg)
        vip_sg_ids.append(sg_id)
    return vip_sg_ids


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
        'vip_qos_policy_id': (
            'vip_qos_policy_id',
            'policies',
            client_manager.neutronclient.list_qos_policies,
        ),
        'vip_vnic_type': ('vip_vnic_type', str),
        'enable': ('admin_state_up', lambda x: True),
        'disable': ('admin_state_up', lambda x: False),
        'cascade': ('cascade', lambda x: True),
        'provisioning_status': ('provisioning_status', str),
        'operating_status': ('operating_status', str),
        'provider': ('provider', str),
        'flavor': (
            'flavor_id',
            'flavors',
            client_manager.load_balancer.flavor_list
        ),
        'availability_zone': ('availability_zone', str),
        'additional_vip': (
            'additional_vips',
            functools.partial(
                handle_additional_vips, client_manager=client_manager)
        ),
        'vip_sg_id': (
            'vip_sg_ids',
            functools.partial(
                handle_vip_sg_ids, client_manager=client_manager),
        )
    }
    add_tags_attr_map(attr_map)

    _attrs = vars(parsed_args)
    attrs = _map_attrs(_attrs, attr_map)

    return attrs


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
        'insert_headers': ('insert_headers', _format_kv),
        'default_tls_container_ref': ('default_tls_container_ref', str),
        'sni_container_refs': ('sni_container_refs', list),
        'timeout_client_data': ('timeout_client_data', int),
        'timeout_member_connect': ('timeout_member_connect', int),
        'timeout_member_data': ('timeout_member_data', int),
        'timeout_tcp_inspect': ('timeout_tcp_inspect', int),
        'client_ca_tls_container_ref': ('client_ca_tls_container_ref',
                                        _format_str_if_need_treat_unset),
        'client_authentication': ('client_authentication', str),
        'client_crl_container_ref': ('client_crl_container_ref',
                                     _format_str_if_need_treat_unset),
        'allowed_cidrs': ('allowed_cidrs', list),
        'tls_ciphers': ('tls_ciphers', str),
        'tls_versions': ('tls_versions', list),
        'alpn_protocols': ('alpn_protocols', list),
        'hsts_max_age': ('hsts_max_age', int),
        'hsts_include_subdomains': ('hsts_include_subdomains', bool),
        'hsts_preload': ('hsts_preload', bool),
    }
    add_tags_attr_map(attr_map)

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
        'disable': ('admin_state_up', lambda x: False),
        'tls_container_ref': ('tls_container_ref',
                              _format_str_if_need_treat_unset),
        'ca_tls_container_ref': ('ca_tls_container_ref',
                                 _format_str_if_need_treat_unset),
        'crl_container_ref': ('crl_container_ref',
                              _format_str_if_need_treat_unset),

        'enable_tls': ('tls_enabled', lambda x: True),
        'disable_tls': ('tls_enabled', lambda x: False),
        'tls_ciphers': ('tls_ciphers', str),
        'tls_versions': ('tls_versions', list),
        'alpn_protocols': ('alpn_protocols', list),
    }
    add_tags_attr_map(attr_map)

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
        'enable_backup': ('backup', lambda x: True),
        'disable_backup': ('backup', lambda x: False),
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
        'request_sriov': ('request_sriov', lambda x: True),
        'vnic_type': ('vnic_type', str),
    }
    add_tags_attr_map(attr_map)

    _attrs = vars(parsed_args)
    attrs = _map_attrs(_attrs, attr_map)

    return attrs


def get_l7policy_attrs(client_manager, parsed_args):
    attr_map = {
        'name': ('name', str),
        'description': ('description', str),
        'redirect_url': ('redirect_url', str),
        'redirect_http_code': ('redirect_http_code', int),
        'redirect_prefix': ('redirect_prefix', str),
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
    add_tags_attr_map(attr_map)

    _attrs = vars(parsed_args)
    attrs = _map_attrs(_attrs, attr_map)

    return attrs


def get_l7rule_attrs(client_manager, parsed_args):
    attr_map = {
        'action': ('action', str),
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
        'compare_type': ('compare_type', str),
        'enable': ('admin_state_up', lambda x: True),
        'disable': ('admin_state_up', lambda x: False)
    }
    add_tags_attr_map(attr_map)

    _attrs = vars(parsed_args)
    attrs = _map_attrs(_attrs, attr_map)

    return attrs


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
        'disable': ('admin_state_up', lambda x: False),
        'http_version': ('http_version', float),
        'domain_name': ('domain_name', str)
    }
    add_tags_attr_map(attr_map)

    _attrs = vars(parsed_args)
    attrs = _map_attrs(_attrs, attr_map)

    return attrs


def get_quota_attrs(client_manager, parsed_args):
    attr_map = {
        'health_monitor': ('health_monitor', int),
        'listener': ('listener', int),
        'load_balancer': ('load_balancer', int),
        'member': ('member', int),
        'pool': ('pool', int),
        'l7policy': ('l7policy', int),
        'l7rule': ('l7rule', int),
        'project': (
            'project_id',
            'project',
            client_manager.identity
        ),
    }

    _attrs = vars(parsed_args)
    attrs = _map_attrs(_attrs, attr_map)

    return attrs


def get_amphora_attrs(client_manager, parsed_args):
    attr_map = {
        'amphora_id': (
            'amphora_id',
            'amphorae',
            client_manager.load_balancer.amphora_list,
        ),
        'loadbalancer': (
            'loadbalancer_id',
            'loadbalancers',
            client_manager.load_balancer.load_balancer_list,
        ),
        'compute_id': ('compute_id', str),
        'role': ('role', str),
        'status': ('status', str),
        'image_id': ('image_id', str),
    }

    return _map_attrs(vars(parsed_args), attr_map)


def get_provider_attrs(parsed_args):
    attr_map = {
        'provider': ('provider_name', str),
        'description': ('description', str),
        'flavor': ('flavor', bool),
        'availability_zone': ('availability_zone', bool),
    }

    return _map_attrs(vars(parsed_args), attr_map)


def get_flavor_attrs(client_manager, parsed_args):
    attr_map = {
        'name': ('name', str),
        'flavor': (
            'flavor_id',
            'flavors',
            client_manager.load_balancer.flavor_list,
        ),
        'flavorprofile': (
            'flavor_profile_id',
            'flavorprofiles',
            client_manager.load_balancer.flavorprofile_list,
        ),
        'enable': ('enabled', lambda x: True),
        'disable': ('enabled', lambda x: False),
        'description': ('description', str),
    }

    _attrs = vars(parsed_args)
    attrs = _map_attrs(_attrs, attr_map)

    return attrs


def get_flavorprofile_attrs(client_manager, parsed_args):
    attr_map = {
        'name': ('name', str),
        'flavorprofile': (
            'flavorprofile_id',
            'flavorprofiles',
            client_manager.load_balancer.flavorprofile_list,
        ),
        'provider': ('provider_name', str),
        'flavor_data': ('flavor_data', str),
    }

    _attrs = vars(parsed_args)
    attrs = _map_attrs(_attrs, attr_map)

    return attrs


def get_availabilityzone_attrs(client_manager, parsed_args):
    attr_map = {
        'name': ('name', str),
        'availabilityzone': (
            'availabilityzone_name',
            'availability_zones',
            client_manager.load_balancer.availabilityzone_list,
        ),
        'availabilityzoneprofile': (
            'availability_zone_profile_id',
            'availability_zone_profiles',
            client_manager.load_balancer.availabilityzoneprofile_list,
        ),
        'enable': ('enabled', lambda x: True),
        'disable': ('enabled', lambda x: False),
        'description': ('description', str),
    }

    _attrs = vars(parsed_args)
    attrs = _map_attrs(_attrs, attr_map)

    return attrs


def get_availabilityzoneprofile_attrs(client_manager, parsed_args):
    attr_map = {
        'name': ('name', str),
        'availabilityzoneprofile': (
            'availability_zone_profile_id',
            'availability_zone_profiles',
            client_manager.load_balancer.availabilityzoneprofile_list,
        ),
        'provider': ('provider_name', str),
        'availability_zone_data': ('availability_zone_data', str),
    }

    _attrs = vars(parsed_args)
    attrs = _map_attrs(_attrs, attr_map)

    return attrs


def format_list(data):
    if data:
        return '\n'.join(i['id'] for i in data)
    return None


class ListColumn(columns.FormattableColumn):
    def human_readable(self):
        return format_list(self._value)


def format_list_flat(data):
    if data:
        return '\n'.join(i for i in data)
    return None


class FlatListColumn(columns.FormattableColumn):
    def human_readable(self):
        return format_list_flat(self._value)


def format_hash(data):
    if data:
        return '\n'.join('{}={}'.format(k, v) for k, v in data.items())
    return None


class HashColumn(columns.FormattableColumn):
    def human_readable(self):
        return format_hash(self._value)


def _format_kv(data):
    formatted_kv = {}
    values = data.split(',')
    for value in values:
        k, v = value.split('=')
        formatted_kv[k] = v

    return formatted_kv


def _format_str_if_need_treat_unset(data):
    if data.lower() in ('none', 'null', 'void'):
        return None
    return str(data)


def get_unsets(parsed_args):
    unsets = {}
    for arg, value in vars(parsed_args).items():
        if value and arg == 'tags':
            unsets[arg] = value
        elif value is True and arg not in ('wait', 'all_tag'):
            unsets[arg] = None
    return unsets


class _Munch(dict):
    __getattr__ = dict.get


def wait_for_active(status_f, res_id):
    success = utils.wait_for_status(
        status_f=lambda x: _Munch(status_f(x)),
        res_id=res_id,
        status_field=constants.PROVISIONING_STATUS,
        sleep_time=3
    )
    if not success:
        raise exceptions.OctaviaClientException(
            code="n/a",
            message="The resource did not successfully reach ACTIVE status.")


def wait_for_delete(status_f, res_id,
                    status_field=constants.PROVISIONING_STATUS):
    class Getter(object):
        @staticmethod
        def get(id):
            return _Munch(status_f(id))

    try:
        success = utils.wait_for_delete(
            manager=Getter,
            res_id=res_id,
            status_field=status_field,
            sleep_time=3
        )
        if not success:
            raise exceptions.OctaviaClientException(
                code="n/a",
                message="The resource could not be successfully deleted.")
    except exceptions.OctaviaClientException as e:
        if e.code != 404:
            raise


def set_tags_for_set(resource_get, resource_id, attrs, clear_tags=False):
    if attrs.get('tags'):
        resource = resource_get(resource_id)
        tags = set([] if clear_tags else resource['tags'])
        tags |= set(attrs['tags'])
        attrs['tags'] = list(tags)
    elif clear_tags:
        attrs['tags'] = []


def set_tags_for_unset(resource_get, resource_id, attrs, clear_tags=False):
    if clear_tags:
        attrs['tags'] = []
    elif attrs.get('tags'):
        resource = resource_get(resource_id)
        tags = set(resource['tags'])
        tags -= set(attrs['tags'])
        attrs['tags'] = list(tags)
