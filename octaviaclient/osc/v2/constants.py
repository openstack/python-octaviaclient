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

LOAD_BALANCER_ROWS = (
    'admin_state_up',
    'created_at',
    'description',
    'flavor',
    'id',
    'listeners',
    'name',
    'operating_status',
    'pools',
    'project_id',
    'provider',
    'provisioning_status',
    'updated_at',
    'vip_Address',
    'vip_network_id',
    'vip_port_id',
    'vip_subnet_id')

LOAD_BALANCER_COLUMNS = (
    'id',
    'name',
    'project_id',
    'vip_address',
    'provisioning_status',
    'provider')

LISTENER_ROWS = (
    'admin_state_up',
    'connection_limit',
    'created_at',
    'default_pool_id',
    'default_tls_container_ref',
    'description',
    'id',
    'insert_headers',
    'l7policies',
    'loadbalancers',
    'name',
    'operating_status',
    'project_id',
    'protocol',
    'protocol_port',
    'provisioning_status',
    'sni_container_refs',
    'updated_at')

LISTENER_COLUMNS = (
    'id',
    'default_pool_id',
    'name',
    'project_id',
    'protocol',
    'protocol_port',
    'admin_state_up')

POOL_ROWS = (
    'admin_state_up',
    'created_at',
    'description',
    'healthmonitor_id',
    'id',
    'lb_algorithm',
    'listeners',
    'loadbalancers',
    'members',
    'name',
    'operating_status',
    'project_id',
    'protocol',
    'provisioning_status',
    'session_persistence',
    'updated_at')

POOL_COLUMNS = (
    'id',
    'name',
    'project_id',
    'provisioning status',
    'protocol',
    'lb_algorithm',
    'admin_state_up')

MEMBER_ROWS = (
    'address',
    'admin_state_up',
    'created_at',
    'id',
    'name',
    'operating_status',
    'project_id',
    'protocol_port',
    'provisioning_status',
    'subnet_id',
    'updated_at',
    'weight',
    'monitor_port',
    'monitor_address')

MEMBER_COLUMNS = (
    'id',
    'name',
    'project_id',
    'provisioning_status',
    'address',
    'protocol_port',
    'operating_status',
    'weight')

L7POLICY_ROWS = (
    'listener_id',
    'description',
    'admin_state_up',
    'rules',
    'project_id',
    'created_at',
    'provisioning_status',
    'updated_at',
    'redirect_pool_id',
    'redirect_url',
    'action',
    'position',
    'id',
    'operating_status',
    'name')

L7POLICY_COLUMNS = (
    'id',
    'name',
    'project_id',
    'provisioning_status',
    'action',
    'position',
    'admin_state_up')

L7RULE_ROWS = (
    'created_at',
    'compare_type',
    'provisioning_status',
    'invert',
    'admin_state_up',
    'updated_at',
    'value',
    'key',
    'project_id',
    'type',
    'id',
    'operating_status')

L7RULE_COLUMNS = (
    'id',
    'project_id',
    'provisioning_status',
    'compare_type',
    'type',
    'key',
    'value',
    'invert',
    'admin_state_up')

MONITOR_ROWS = (
    'project_id',
    'name',
    'admin_state_up',
    'pools',
    'created_at',
    'provisioning_status',
    'updated_at',
    'delay',
    'expected_codes',
    'max_retries',
    'http_method',
    'timeout',
    'max_retries_down',
    'url_path',
    'type',
    'id',
    'operating_status'
)

MONITOR_COLUMNS = (
    'id',
    'name',
    'project_id',
    'type',
    'admin_state_up',
)
