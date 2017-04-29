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
