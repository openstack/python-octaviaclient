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
from requests_mock.contrib import fixture

from octaviaclient.api import load_balancer_v2 as lb
from osc_lib.tests import utils

FAKE_ACCOUNT = 'q12we34r'
FAKE_AUTH = '11223344556677889900'
FAKE_URL = 'http://example.com/v2.0/lbaas/'

FAKE_LB = 'rainbarrel'

LIST_LB_RESP = [
    {'name': 'lb1'},
    {'name': 'lb2'},
]


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
            json={'loadbalancers': LIST_LB_RESP},
            status_code=200,
        )
        ret = self.api.load_balancer_list()
        self.assertEqual(LIST_LB_RESP, ret)
