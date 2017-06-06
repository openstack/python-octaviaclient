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

from osc_lib import exceptions

from octaviaclient.osc.v2 import load_balancer as load_balancer
from octaviaclient.tests.unit.osc.v2 import fakes as lb_fakes

AUTH_TOKEN = "foobar"
AUTH_URL = "http://192.0.2.2"


class TestLoadBalancer(lb_fakes.TestLoadBalancerv2):

    _lb = lb_fakes.FakeLoadBalancer.create_one_load_balancer()

    columns = (
        'id',
        'name',
        'project_id',
        'vip_address',
        'provisioning_status',
        'provider'
    )

    datalist = (
        (
            _lb.id,
            _lb.name,
            _lb.project_id,
            _lb.vip_address,
            _lb.provisioning_status,
            _lb.provider
        ),
    )

    info = {
        'loadbalancers':
            [{'id': _lb.id,
              'name': _lb.name,
              'project_id': _lb.project_id,
              'vip_address': _lb.vip_address,
              'vip_network_id': _lb.vip_network_id,
              'provisioning_status': _lb.provisioning_status,
              'provider': _lb.provider
              }]
    }
    lb_info = copy.deepcopy(info)

    def setUp(self):
        super(TestLoadBalancer, self).setUp()
        self.lb_mock = self.app.client_manager.load_balancer.load_balancers
        self.lb_mock.reset_mock()

        self.api_mock = mock.Mock()
        self.api_mock.load_balancer_list.return_value = self.lb_info
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock
        lb_client.neutronclient = mock.MagicMock()


class TestLoadBalancerList(TestLoadBalancer):

    def setUp(self):
        super(TestLoadBalancerList, self).setUp()
        self.cmd = load_balancer.ListLoadBalancer(self.app, None)

    def test_load_balancer_list_no_options(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)
        self.api_mock.load_balancer_list.assert_called_with()

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))

    def test_load_balancer_list_with_options(self):
        arglist = ['--name', 'rainbarrel']
        verifylist = [('name', 'rainbarrel')]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)
        self.api_mock.load_balancer_list.assert_called_with(name='rainbarrel')

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))


class TestLoadBalancerDelete(TestLoadBalancer):

    def setUp(self):
        super(TestLoadBalancerDelete, self).setUp()
        self.cmd = load_balancer.DeleteLoadBalancer(self.app, None)

    def test_load_balancer_delete(self):
        arglist = [self._lb.id]
        verifylist = [
            ('loadbalancer', self._lb.id)
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.load_balancer_delete.assert_called_with(
            lb_id=self._lb.id)

    def test_load_balancer_delete_failure(self):
        arglist = ['unknown_lb']
        verifylist = [
            ('loadbalancer', 'unknown_lb')
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.assertRaises(exceptions.CommandError, self.cmd.take_action,
                          parsed_args)
        self.assertNotCalled(self.api_mock.load_balancer_delete)


class TestLoadBalancerCreate(TestLoadBalancer):

    def setUp(self):
        super(TestLoadBalancerCreate, self).setUp()
        self.api_mock = mock.Mock()
        self.api_mock.load_balancer_create.return_value = {
            'loadbalancer': self.lb_info['loadbalancers'][0]
        }
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock

        self.cmd = load_balancer.CreateLoadBalancer(self.app, None)

    @mock.patch('octaviaclient.osc.v2.utils.get_loadbalancer_attrs')
    def test_load_balancer_create(self, mock_client):
        mock_client.return_value = self.lb_info['loadbalancers'][0]
        arglist = ['--name', self._lb.name,
                   '--vip-network-id', self._lb.vip_network_id,
                   '--project', self._lb.project_id]
        verifylist = [
            ('name', self._lb.name),
            ('vip_network_id', self._lb.vip_network_id),
            ('project', self._lb.project_id)
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.load_balancer_create.assert_called_with(
            json={'loadbalancer': self.lb_info['loadbalancers'][0]})


class TestLoadBalancerShow(TestLoadBalancer):

    def setUp(self):
        super(TestLoadBalancerShow, self).setUp()
        self.api_mock = mock.Mock()
        self.api_mock.load_balancer_list.return_value = self.lb_info
        self.api_mock.load_balancer_show.return_value = {
            'loadbalancer': self.lb_info['loadbalancers'][0]}
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock

        self.cmd = load_balancer.ShowLoadBalancer(self.app, None)

    def test_load_balancer_show(self):
        arglist = [self._lb.id]
        verifylist = [
            ('loadbalancer', self._lb.id),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.load_balancer_show.assert_called_with(lb_id=self._lb.id)


class TestLoadBalancerSet(TestLoadBalancer):

    def setUp(self):
        super(TestLoadBalancerSet, self).setUp()
        self.cmd = load_balancer.SetLoadBalancer(self.app, None)

    def test_load_balancer_set(self):
        arglist = [self._lb.id, '--name', 'new_name']
        verifylist = [
            ('loadbalancer', self._lb.id),
            ('name', 'new_name')
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.load_balancer_set.assert_called_with(
            self._lb.id, json={'loadbalancer': {'name': 'new_name'}})
