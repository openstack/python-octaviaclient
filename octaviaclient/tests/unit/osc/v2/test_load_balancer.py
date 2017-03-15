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

from octaviaclient.osc.v2 import load_balancer as load_balancer
from octaviaclient.tests.unit.osc.v2 import fakes as lb_fakes

AUTH_TOKEN = "foobar"
AUTH_URL = "http://192.0.2.2"


class TestLoadBalancer(lb_fakes.TestLoadBalancerv2):

    def setUp(self):
        super(TestLoadBalancer, self).setUp()
        self.lb_mock = self.app.client_manager.load_balancer.load_balancers
        self.lb_mock.reset_mock()


class TestLoadBalancerList(TestLoadBalancer):

    _lb = lb_fakes.FakeLoadBalancer.create_one_load_balancer()

    columns = (
        'ID',
        'Name',
        'Project ID',
        'VIP Address',
        'Provisioning Status',
    )

    datalist = (
        (
            _lb.id,
            _lb.name,
            _lb.project_id,
            _lb.vip_address,
            _lb.provisioning_status,
        ),
    )

    info = {
        'id': _lb.id,
        'name': _lb.name,
        'project_id': _lb.project_id,
        'vip_address': _lb.vip_address,
        'provisioning_status': _lb.provisioning_status,
    }
    lb_info = copy.deepcopy(info)

    def setUp(self):
        super(TestLoadBalancerList, self).setUp()
        self.api_mock = mock.Mock()
        self.api_mock.load_balancer_list.return_value = [self.lb_info]
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock

        self.cmd = load_balancer.ListLoadBalancer(self.app, None)

    def test_load_balancer_list_no_options(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)
        self.api_mock.load_balancer_list.assert_called_with()

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))
