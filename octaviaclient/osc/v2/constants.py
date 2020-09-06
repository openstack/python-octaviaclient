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
    'availability_zone',
    'created_at',
    'description',
    'flavor_id',
    'id',
    'listeners',
    'name',
    'operating_status',
    'pools',
    'project_id',
    'provider',
    'provisioning_status',
    'updated_at',
    'vip_address',
    'vip_network_id',
    'vip_port_id',
    'vip_qos_policy_id',
    'vip_subnet_id',
)

LOAD_BALANCER_COLUMNS = (
    'id',
    'name',
    'project_id',
    'vip_address',
    'provisioning_status',
    'operating_status',
    'provider')

LOAD_BALANCER_STATS_ROWS = (
    'active_connections',
    'bytes_in',
    'bytes_out',
    'request_errors',
    'total_connections')

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
    'timeout_client_data',
    'timeout_member_connect',
    'timeout_member_data',
    'timeout_tcp_inspect',
    'updated_at',
    'client_ca_tls_container_ref',
    'client_authentication',
    'client_crl_container_ref',
    'allowed_cidrs',
    'tls_ciphers',
    'tls_versions',
    'alpn_protocols')

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
    'updated_at',
    'tls_container_ref',
    'ca_tls_container_ref',
    'crl_container_ref',
    'tls_enabled',
    'tls_ciphers',
    'tls_versions')

POOL_COLUMNS = (
    'id',
    'name',
    'project_id',
    'provisioning_status',
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
    'monitor_address',
    'backup'
)

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
    'redirect_prefix',
    'action',
    'position',
    'id',
    'operating_status',
    'name',
    'redirect_http_code')

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
    'operating_status',
    'http_version',
    'domain_name'
)

MONITOR_COLUMNS = (
    'id',
    'name',
    'project_id',
    'type',
    'admin_state_up',
)

QUOTA_ROWS = (
    'load_balancer',
    'listener',
    'pool',
    'health_monitor',
    'member',
    'l7policy',
    'l7rule',
)

QUOTA_COLUMNS = (
    'project_id',
    'load_balancer',
    'listener',
    'pool',
    'health_monitor',
    'member',
    'l7policy',
    'l7rule',
)

AMPHORA_ROWS = (
    'id',
    'loadbalancer_id',
    'compute_id',
    'lb_network_ip',
    'vrrp_ip',
    'ha_ip',
    'vrrp_port_id',
    'ha_port_id',
    'cert_expiration',
    'cert_busy',
    'role',
    'status',
    'vrrp_interface',
    'vrrp_id',
    'vrrp_priority',
    'cached_zone',
    'created_at',
    'updated_at',
    'image_id',
    'compute_flavor',
)

AMPHORA_COLUMNS = (
    'id',
    'loadbalancer_id',
    'status',
    'role',
    'lb_network_ip',
    'ha_ip',
)

AMPHORA_COLUMNS_LONG = (
    'id',
    'loadbalancer_id',
    'status',
    'role',
    'lb_network_ip',
    'ha_ip',
    'compute_id',
    'cached_zone',
    'image_id',
)

PROVIDER_COLUMNS = (
    'name',
    'description',
)

PROVIDER_CAPABILITY_COLUMNS = (
    'type',
    'name',
    'description',
)

FLAVOR_ROWS = (
    'id',
    'name',
    'flavor_profile_id',
    'enabled',
    'description',
)

FLAVOR_COLUMNS = (
    'id',
    'name',
    'flavor_profile_id',
    'enabled',
)

FLAVORPROFILE_ROWS = (
    'id',
    'name',
    'provider_name',
    'flavor_data'
)

FLAVORPROFILE_COLUMNS = (
    'id',
    'name',
    'provider_name',
)

AVAILABILITYZONE_ROWS = (
    'name',
    'availability_zone_profile_id',
    'enabled',
    'description',
)

AVAILABILITYZONE_COLUMNS = (
    'name',
    'availability_zone_profile_id',
    'enabled',
)

AVAILABILITYZONEPROFILE_ROWS = (
    'id',
    'name',
    'provider_name',
    'availability_zone_data'
)

AVAILABILITYZONEPROFILE_COLUMNS = (
    'id',
    'name',
    'provider_name',
)

PROVISIONING_STATUS = 'provisioning_status'
STATUS = 'status'

# TCP/UDP port min/max
MIN_PORT_NUMBER = 1
MAX_PORT_NUMBER = 65535

# Member weight min/max
MIN_WEIGHT = 0
MAX_WEIGHT = 256
