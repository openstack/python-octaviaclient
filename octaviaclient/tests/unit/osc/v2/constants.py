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

from oslo_utils import uuidutils

AMPHORA_ATTRS = {
    "id": uuidutils.generate_uuid(dashed=True),
    "loadbalancer_id": uuidutils.generate_uuid(dashed=True),
    "compute_id": uuidutils.generate_uuid(dashed=True),
    "lb_network_ip": "192.168.1.3",
    "vrrp_ip": "192.168.1.6",
    "ha_ip": "192.168.1.10",
    "vrrp_port_id": uuidutils.generate_uuid(dashed=True),
    "ha_port_id": uuidutils.generate_uuid(dashed=True),
    "cert_expiration": "2019-09-19 00:34:51",
    "cert_busy": 0,
    "role": "BACKUP",
    "status": "ALLOCATED",
    "vrrp_interface": "eth1",
    "vrrp_id": 1,
    "vrrp_priority": 200,
    "cached_zone": "zone2",
    "image_id": uuidutils.generate_uuid(dashed=True),
}

HM_ATTRS = {
    "project_id": uuidutils.generate_uuid(dashed=True),
    "name": "hm-name-" + uuidutils.generate_uuid(dashed=True),
    "admin_state_up": True,
    "pools": [
        {
            "id": uuidutils.generate_uuid(dashed=True)
        }
    ],
    "created_at": "2017-05-10T06:11:10",
    "provisioning_status": "PENDING_CREATE",
    "delay": 10,
    "expected_codes": "200",
    "max_retries": 2,
    "http_method": "GET",
    "timeout": 10,
    "max_retries_down": 3,
    "url_path": "/some/custom/path",
    "type": "HTTP",
    "id": uuidutils.generate_uuid(dashed=True),
    "http_version": 1.1,
    "domain_name": "testlab.com"
}

LISTENER_ATTRS = {
    "id": uuidutils.generate_uuid(),
    "name": "li-name-" + uuidutils.generate_uuid(dashed=True),
    "project_id": uuidutils.generate_uuid(dashed=True),
    "protocol": "HTTP",
    "protocol_port": 80,
    "provisioning_status": "ACTIVE",
    "default_pool_id": None,
    "loadbalancers": None,
    "connection_limit": 10,
    "admin_state_up": True,
    "default_tls_container_ref": uuidutils.generate_uuid(dashed=True),
    "sni_container_refs": [uuidutils.generate_uuid(dashed=True),
                           uuidutils.generate_uuid(dashed=True)],
    "timeout_client_data": 50000,
    "timeout_member_connect": 5000,
    "timeout_member_data": 50000,
    "timeout_tcp_inspect": 0,
    'client_ca_tls_container_ref': uuidutils.generate_uuid(dashed=True),
    'client_authentication': "OPTIONAL",
    'client_crl_container_ref': uuidutils.generate_uuid(dashed=True),
    "allowed_cidrs": ['192.0.2.0/24', '198.51.100.0/24'],
    'tls_ciphers': "ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256",
    'tls_versions': ['TLSv1.1', 'TLSv1.2'],
    'alpn_protocols': ['h2', 'http/1.1'],
    "tags": ["foo", "bar"],
    'hsts_max_age': 15_000_000,
    'hsts_include_subdomains': True,
    'hsts_preload': True,
}

LOADBALANCER_ATTRS = {
    "id": uuidutils.generate_uuid(),
    "name": "lb-name-" + uuidutils.generate_uuid(dashed=True),
    "project_id": uuidutils.generate_uuid(dashed=True),
    "vip_address": "192.0.2.124",
    "vip_network_id": uuidutils.generate_uuid(dashed=True),
    "vip_subnet_id": uuidutils.generate_uuid(dashed=True),
    "vip_qos_policy_id": uuidutils.generate_uuid(dashed=True),
    "provisioning_status": "ACTIVE",
    "operating_status": "ONLINE",
    "provider": "octavia",
    "flavor_id": uuidutils.generate_uuid(dashed=True),
    "additional_vips": [{
        "subnet_id": uuidutils.generate_uuid(dashed=True),
        "ip_address": "192.0.2.156"
    }, {
        "subnet_id": uuidutils.generate_uuid(dashed=True),
        "ip_address": "192.0.2.179"
    }],
    "vip_sg_ids": [
        uuidutils.generate_uuid(dashed=True),
        uuidutils.generate_uuid(dashed=True),
    ],
    "tags": ["foo", "bar"]
}

L7POLICY_ATTRS = {
    "listener_id": uuidutils.generate_uuid(),
    "description": "fake desc",
    "admin_state_up": True,
    "rules": [{"id": uuidutils.generate_uuid()}],
    "provisioning_status": "active",
    "redirect_pool_id": uuidutils.generate_uuid(),
    "action": "POOL_REDIRECT",
    "position": 1,
    "project_id": uuidutils.generate_uuid(),
    "id": uuidutils.generate_uuid(),
    "name": "l7po-name-" + uuidutils.generate_uuid(dashed=True),
}

L7RULE_ATTRS = {
    "created_at": "2017-05-04T18:46:35",
    "compare_type": "ENDS_WITH",
    "provisioning_status": "ACTIVE",
    "invert": False,
    "admin_state_up": True,
    "value": ".example.com",
    "key": None,
    "project_id": uuidutils.generate_uuid(),
    "type": "HOST_NAME",
    "id": uuidutils.generate_uuid(),
    "operating_status": "ONLINE",
}

MEMBER_ATTRS = {
    "project_id": uuidutils.generate_uuid(dashed=True),
    "name": "test-member",
    "backup": False,
    "weight": 1,
    "admin_state_up": True,
    "subnet_id": uuidutils.generate_uuid(dashed=True),
    "tenant_id": uuidutils.generate_uuid(dashed=True),
    "provisioning_status": "ACTIVE",
    "address": "192.0.2.122",
    "protocol_port": 80,
    "id": uuidutils.generate_uuid(dashed=True),
    "operating_status": "NO_MONITOR",
    "pool_id": uuidutils.generate_uuid(dashed=True),
}

POOL_ATTRS = {
    "admin_state_up": True,
    "description": "fake desc",
    "id": uuidutils.generate_uuid(),
    "lb_algorithm": "ROUND_ROBIN",
    "listeners": [{"id": uuidutils.generate_uuid()}],
    "loadbalancers": [{"id": uuidutils.generate_uuid()}],
    "members": [{"id": uuidutils.generate_uuid()}],
    "name": "po-name-" + uuidutils.generate_uuid(dashed=True),
    "project_id": uuidutils.generate_uuid(dashed=True),
    "protocol": "HTTP",
    "provisioning_status": "ACTIVE",
    "tls_container_ref": uuidutils.generate_uuid(),
    "ca_tls_container_ref": uuidutils.generate_uuid(),
    "crl_container_ref": uuidutils.generate_uuid(),
    "tls_enabled": True,
    "tls_ciphers": "ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256",
    "tls_versions": ['TLSv1.1', 'TLSv1.2'],
    "tags": ["foo", "bar"],
    "alpn_protocols": ['h2', 'http/1.1']
}

QUOTA_ATTRS = {
    "health_monitor": -1,
    "listener": None,
    "load_balancer": 5,
    "member": 50,
    "pool": None,
    "l7policy": 20,
    "l7rule": 30,
    "project_id": uuidutils.generate_uuid(dashed=True),
}

PROVIDER_ATTRS = {
    "name": "provider1",
    "description": "Description of provider1."
}

CAPABILITY_ATTRS = {
    "name": "some_capability",
    "description": "Description of capability."
}

FLAVOR_ATTRS = {
    "id": uuidutils.generate_uuid(),
    "name": "fv-name-" + uuidutils.generate_uuid(dashed=True),
    "flavor_profile_id": None,
    "enabled": True,
}

FLAVORPROFILE_ATTRS = {
    "id": uuidutils.generate_uuid(),
    "name": "fvpf-name-" + uuidutils.generate_uuid(dashed=True),
    "provider_name": "mock_provider",
    "flavor_data": '{"mock_key": "mock_value"}',
}

AVAILABILITY_ZONE_ATTRS = {
    "name": "az-name-" + uuidutils.generate_uuid(dashed=True),
    "availability_zone_profile_id": None,
    "enabled": True,
    "description": "Description of AZ",
}

AVAILABILITY_ZONE_PROFILE_ATTRS = {
    "id": uuidutils.generate_uuid(),
    "name": "azpf-name-" + uuidutils.generate_uuid(dashed=True),
    "provider_name": "mock_provider",
    "availabilityzone_data": '{"mock_key": "mock_value"}',
}
