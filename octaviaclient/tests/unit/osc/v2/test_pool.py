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

from octaviaclient.osc.v2 import pool as pool
from octaviaclient.tests.unit.osc.v2 import fakes as po_fakes

AUTH_TOKEN = "foobar"
AUTH_URL = "http://192.0.2.2"


class TestPool(po_fakes.TestLoadBalancerv2):

    _po = po_fakes.FakePool.create_one_pool()

    columns = ('id',
               'name',
               'project_id',
               'provisioning status',
               'protocol',
               'lb_algorithm',
               'admin_state_up')

    datalist = (
        (
            _po.id,
            _po.name,
            _po.project_id,
            _po.provisioning_status,
            _po.protocol,
            _po.lb_algorithm,
            True
        ),
    )

    info = {
        'pools':
            [{'id': _po.id,
                'name': _po.name,
                'project_id': _po.project_id,
                'provisioning_status': _po.provisioning_status,
                'members': _po.members,
                'protocol': _po.protocol,
                'lb_algorithm': _po.lb_algorithm,
                'loadbalancers': _po.loadbalancers,
                'listeners': _po.listeners,
                'pool_id': _po.id,
                'admin_state_up': True,
                'session_persistance': {'k': 'v'}
              }]
    }
    po_info = copy.deepcopy(info)

    def setUp(self):
        super(TestPool, self).setUp()
        self.li_mock = self.app.client_manager.load_balancer.load_balancers
        self.li_mock.reset_mock()

        self.api_mock = mock.Mock()
        self.api_mock.pool_list.return_value = self.po_info
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock


class TestPoolList(TestPool):

    def setUp(self):
        super(TestPoolList, self).setUp()
        self.cmd = pool.ListPool(self.app, None)

    def test_pool_list_no_options(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        self.api_mock.pool_list.assert_called_with()
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))


class TestPoolDelete(TestPool):

    def setUp(self):
        super(TestPoolDelete, self).setUp()
        self.cmd = pool.DeletePool(self.app, None)

    def test_pool_delete(self):
        arglist = [self._po.id]
        verifylist = [
            ('pool', self._po.id)
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.pool_delete.assert_called_with(
            pool_id=self._po.id)

    def test_listener_delete_failure(self):
        arglist = ['unknown_pool']
        verifylist = [
            ('pool', 'unknown_pool')
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.assertRaises(exceptions.CommandError, self.cmd.take_action,
                          parsed_args)
        self.assertNotCalled(self.api_mock.pool_delete)


class TestPoolCreate(TestPool):

    def setUp(self):
        super(TestPoolCreate, self).setUp()
        self.api_mock = mock.Mock()
        self.api_mock.pool_create.return_value = {
            'pool': self.po_info}
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock

        self.cmd = pool.CreatePool(self.app, None)

    @mock.patch('octaviaclient.osc.v2.utils.get_pool_attrs')
    def test_pool_create(self, mock_attrs):
        mock_attrs.return_value = self.po_info
        arglist = ['--loadbalancer', 'mock_lb_id',
                   '--name', self._po.name,
                   '--protocol', 'HTTP',
                   '--lb-algorithm', 'ROUND_ROBIN']

        verifylist = [
            ('loadbalancer', 'mock_lb_id'),
            ('name', self._po.name),
            ('protocol', 'HTTP'),
            ('lb_algorithm', 'ROUND_ROBIN')
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.pool_create.assert_called_with(
            json={'pool': self.po_info})


class TestPoolShow(TestPool):

    def setUp(self):
        super(TestPoolShow, self).setUp()
        self.api_mock = mock.Mock()
        self.api_mock.pool_list.return_value = self.po_info
        self.api_mock.pool_show.return_value = {
            'pool': self.po_info['pools'][0]}
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock

        self.cmd = pool.ShowPool(self.app, None)

    def test_pool_show(self,):
        arglist = [self._po.id]
        verifylist = [
            ('pool', self._po.id),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.pool_show.assert_called_with(pool_id=self._po.id)


class TestPoolSet(TestPool):

    def setUp(self):
        super(TestPoolSet, self).setUp()
        self.cmd = pool.SetPool(self.app, None)

    def test_pool_set(self):
        arglist = [self._po.id, '--name', 'new_name']
        verifylist = [
            ('pool', self._po.id),
            ('name', 'new_name')
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.pool_set.assert_called_with(
            self._po.id, json={'pool': {'name': 'new_name'}})
