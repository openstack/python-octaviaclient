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
