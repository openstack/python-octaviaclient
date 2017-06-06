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

"""Load Balancer v2 API Library Tests"""

from keystoneauth1 import session
from oslo_utils import uuidutils
from requests_mock.contrib import fixture

from octaviaclient.api import load_balancer_v2 as lb
from osc_lib.tests import utils

FAKE_ACCOUNT = 'q12we34r'
FAKE_AUTH = '11223344556677889900'
FAKE_URL = 'http://example.com/v2.0/lbaas/'

FAKE_LB = uuidutils.generate_uuid()
FAKE_LI = uuidutils.generate_uuid()
FAKE_PO = uuidutils.generate_uuid()

LIST_LB_RESP = {
    'loadbalancers':
        [{'name': 'lb1'},
         {'name': 'lb2'}]
}

LIST_LI_RESP = {
    'listeners':
        [{'name': 'lb1'},
         {'name': 'lb2'}]
}

LIST_PO_RESP = {
    'pools':
        [{'name': 'po1'},
         {'name': 'po2'}]
}

SINGLE_LB_RESP = {'loadbalancer': {'id': FAKE_LB, 'name': 'lb1'}}
SINGLE_LB_UPDATE = {"loadbalancer": {"admin_state_up": False}}

SINGLE_LI_RESP = {'listener': {'id': FAKE_LI, 'name': 'li1'}}
SINGLE_LI_UPDATE = {"listener": {"admin_state_up": False}}

SINGLE_PO_RESP = {'pool': {'id': FAKE_PO, 'name': 'li1'}}
SINGLE_PO_UPDATE = {"pool": {"admin_state_up": False}}


class TestLoadBalancerv2(utils.TestCase):

    def setUp(self):
        super(TestLoadBalancerv2, self).setUp()
        sess = session.Session()
        self.api = lb.APIv2(session=sess, endpoint=FAKE_URL)
        self.requests_mock = self.useFixture(fixture.Fixture())


class TestLoadBalancer(TestLoadBalancerv2):

    def test_list_load_balancer_no_options(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_URL + 'loadbalancers',
            json=LIST_LB_RESP,
            status_code=200,
        )
        ret = self.api.load_balancer_list()
        self.assertEqual(LIST_LB_RESP, ret)

    def test_show_load_balancer(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_URL + 'loadbalancers/' + FAKE_LB,
            json=SINGLE_LB_RESP,
            status_code=200
        )
        ret = self.api.load_balancer_show(FAKE_LB)
        self.assertEqual(SINGLE_LB_RESP['loadbalancer'], ret)

    def test_create_load_balancer(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_URL + 'loadbalancers',
            json=SINGLE_LB_RESP,
            status_code=200
        )
        ret = self.api.load_balancer_create(json=SINGLE_LB_RESP)
        self.assertEqual(SINGLE_LB_RESP, ret)

    def test_set_load_balancer(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_URL + 'loadbalancers/' + FAKE_LB,
            json=SINGLE_LB_UPDATE,
            status_code=200
        )
        ret = self.api.load_balancer_set(FAKE_LB, json=SINGLE_LB_UPDATE)
        self.assertEqual(SINGLE_LB_UPDATE, ret)

    def test_delete_load_balancer(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_URL + 'loadbalancers/' + FAKE_LB,
            status_code=200
        )
        ret = self.api.load_balancer_delete(FAKE_LB)
        self.assertEqual(200, ret.status_code)

    def test_list_listeners_no_options(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_URL + 'listeners',
            json=LIST_LI_RESP,
            status_code=200,
        )
        ret = self.api.listener_list()
        self.assertEqual(LIST_LI_RESP, ret)

    def test_show_listener(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_URL + 'listeners/' + FAKE_LI,
            json=SINGLE_LI_RESP,
            status_code=200
        )
        ret = self.api.listener_show(FAKE_LI)
        self.assertEqual(SINGLE_LI_RESP['listener'], ret)

    def test_create_listener(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_URL + 'listeners',
            json=SINGLE_LI_RESP,
            status_code=200
        )
        ret = self.api.listener_create(json=SINGLE_LI_RESP)
        self.assertEqual(SINGLE_LI_RESP, ret)

    def test_set_listeners(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_URL + 'listeners/' + FAKE_LI,
            json=SINGLE_LI_UPDATE,
            status_code=200
        )
        ret = self.api.listener_set(FAKE_LI, json=SINGLE_LI_UPDATE)
        self.assertEqual(SINGLE_LI_UPDATE, ret)

    def test_delete_listener(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_URL + 'listeners/' + FAKE_LI,
            status_code=200
        )
        ret = self.api.listener_delete(FAKE_LI)
        self.assertEqual(200, ret.status_code)

    def test_list_pool_no_options(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_URL + 'pools',
            json=LIST_PO_RESP,
            status_code=200,
        )
        ret = self.api.pool_list()
        self.assertEqual(LIST_PO_RESP, ret)

    def test_show_pool(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_URL + 'pools/' + FAKE_PO,
            json=SINGLE_PO_RESP,
            status_code=200
        )
        ret = self.api.pool_show(FAKE_PO)
        self.assertEqual(SINGLE_PO_RESP['pool'], ret)

    def test_create_pool(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_URL + 'pools',
            json=SINGLE_PO_RESP,
            status_code=200
        )
        ret = self.api.pool_create(json=SINGLE_PO_RESP)
        self.assertEqual(SINGLE_PO_RESP, ret)

    def test_set_pool(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_URL + 'pools/' + FAKE_PO,
            json=SINGLE_PO_UPDATE,
            status_code=200
        )
        ret = self.api.pool_set(FAKE_PO, json=SINGLE_PO_UPDATE)
        self.assertEqual(SINGLE_PO_UPDATE, ret)

    def test_delete_pool(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_URL + 'pools/' + FAKE_PO,
            status_code=200
        )
        ret = self.api.pool_delete(FAKE_PO)
        self.assertEqual(200, ret.status_code)
