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

import copy
import mock
import uuid

from octaviaclient.tests import fakes
from osc_lib.tests import utils


LOADBALANCER = {
    'id': 'lbid',
    'name': 'lb1',
    'project_id': 'dummyproject',
    'vip_address': '192.0.2.2',
    'provisioning_status': 'ONLINE',
    'provider': 'octavia'
}


class FakeLoadBalancerv2Client(object):
    def __init__(self, **kwargs):
        self.load_balancers = mock.Mock()
        self.load_balancers.resource_class = fakes.FakeResource(None, {})
        self.auth_token = kwargs['token']
        self.management_url = kwargs['endpoint']


class TestLoadBalancerv2(utils.TestCommand):

    def setUp(self):
        super(TestLoadBalancerv2, self).setUp()
        self.app.client_manager.load_balancer = FakeLoadBalancerv2Client(
            endpoint=fakes.AUTH_URL,
            token=fakes.AUTH_TOKEN,
        )


class FakeLoadBalancer(object):
    """Fake one or more load balancers."""

    @staticmethod
    def create_one_load_balancer(attrs=None):
        """Create one load balancer.

        :param Dictionary attrs:
            A dictionary with all load balancer attributes
        :return:
            A FakeResource object
        """
        attrs = attrs or {}

        # Set default attribute
        lb_info = {
            'id': str(uuid.uuid4()),
            'name': 'lb-name-' + uuid.uuid4().hex,
            'project_id': uuid.uuid4().hex,
            'vip_address': '192.0.2.124',
            'vip_network_id': uuid.uuid4().hex,
            'provisioning_status': 'ONLINE',
            'provider': 'octavia'
        }

        lb_info.update(attrs)

        lb = fakes.FakeResource(
            info=copy.deepcopy(lb_info),
            loaded=True)

        return lb


class FakeListener(object):
    """Fake one or more listeners."""

    @staticmethod
    def create_one_listener(attrs=None):
        attrs = attrs or {}

        li_info = {
            'id': str(uuid.uuid4()),
            'name': 'li-name-' + uuid.uuid4().hex,
            'project_id': uuid.uuid4().hex,
            'protocol': 'HTTP',
            'protocol_port': 80,
            'provisioning_status': 'ACTIVE',
            'default_pool_id': None,
            'connection_limit': 10,
            'admin_state_up': True,
        }

        li_info.update(attrs)

        li = fakes.FakeResource(
            info=copy.deepcopy(li_info),
            loaded=True)

        return li


class FakePool(object):
    """Fake one or more pool."""

    @staticmethod
    def create_one_pool(attrs=None):
        attrs = attrs or {}

        po_info = {
            'admin_state_up': True,
            'description': 'fake desc',
            'id': str(uuid.uuid4()),
            'lb_algorithm': 'ROUND_ROBIN',
            'listeners': [{'id': str(uuid.uuid4())}],
            'loadbalancers': [{'id': str(uuid.uuid4())}],
            'members': [{'id': str(uuid.uuid4())}],
            'name': 'po-name-' + uuid.uuid4().hex,
            'project_id': uuid.uuid4().hex,
            'protocol': 'HTTP',
            'provisioning_status': 'ACTIVE',
        }

        po_info.update(attrs)

        po = fakes.FakeResource(
            info=copy.deepcopy(po_info),
            loaded=True)

        return po


class FakeMember(object):

    @staticmethod
    def create_member(attrs=None):
        attrs = attrs or {}

        member = {
            "project_id": uuid.uuid4().hex,
            "name": "test-member",
            "weight": 1,
            "admin_state_up": True,
            "subnet_id": uuid.uuid4().hex,
            "tenant_id": uuid.uuid4().hex,
            "provisioning_status": "ACTIVE",
            "address": "192.0.2.122",
            "protocol_port": 80,
            "id": uuid.uuid4().hex,
            "operating_status": "NO_MONITOR",
            "pool_id": uuid.uuid4().hex
        }

        member.update(attrs)

        mem = fakes.FakeResource(info=copy.deepcopy(member), loaded=True)

        return mem


class FakeL7Policy(object):
    """Fake one or more L7policy."""

    @staticmethod
    def create_one_l7policy(attrs=None):
        attrs = attrs or {}

        l7po_info = {
            "listener_id": str(uuid.uuid4()),
            "description": 'fake desc',
            "admin_state_up": True,
            "rules": [{'id': str(uuid.uuid4())}],
            "provisioning_status": 'active',
            "redirect_pool_id": str(uuid.uuid4()),
            "action": 'POOL_REDIRECT',
            "position": 1,
            "project_id": str(uuid.uuid4()),
            "id": str(uuid.uuid4()),
            "name": 'l7po-name-' + uuid.uuid4().hex
        }
        l7po_info.update(attrs)

        l7po = fakes.FakeResource(
            info=copy.deepcopy(l7po_info),
            loaded=True)

        return l7po


class FakeL7Rule(object):
    """Fake one or more L7policy."""

    @staticmethod
    def create_one_l7rule(attrs=None):
        attrs = attrs or {}

        l7ru_info = {
            "created_at": "2017-05-04T18:46:35",
            "compare_type": "ENDS_WITH",
            "provisioning_status": "ACTIVE",
            "invert": False,
            "admin_state_up": True,
            "value": ".example.com",
            "key": None,
            "project_id": str(uuid.uuid4()),
            "type": "HOST_NAME",
            "id": str(uuid.uuid4()),
            "operating_status": "ONLINE"
        }

        l7ru_info.update(attrs)

        l7ru = fakes.FakeResource(
            info=copy.deepcopy(l7ru_info),
            loaded=True)

        return l7ru


class FakeHM(object):
    """Fake one or more L7policy."""

    @staticmethod
    def create_one_health_monitor(attrs=None):
        attrs = attrs or {}

        hm_info = {
            "project_id": uuid.uuid4().hex,
            "name": 'hm-name-' + uuid.uuid4().hex,
            "admin_state_up": True,
            "pools": [
                {
                    "id": uuid.uuid4().hex
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
            "id": uuid.uuid4().hex
        }

        hm_info.update(attrs)

        hm = fakes.FakeResource(
            info=copy.deepcopy(hm_info),
            loaded=True)

        return hm
