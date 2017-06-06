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

from octaviaclient.osc.v2 import listener as listener
from octaviaclient.tests.unit.osc.v2 import fakes as li_fakes

AUTH_TOKEN = "foobar"
AUTH_URL = "http://192.0.2.2"


class TestListener(li_fakes.TestLoadBalancerv2):

    _li = li_fakes.FakeListener.create_one_listener()

    columns = (
        'id',
        'default_pool_id',
        'name',
        'project_id',
        'protocol',
        'protocol_port',
        'admin_state_up')

    datalist = (
        (
            _li.id,
            _li.default_pool_id,
            _li.name,
            _li.project_id,
            _li.protocol,
            _li.protocol_port,
            _li.admin_state_up
        ),
    )

    info = {
        'listeners':
            [{
                'id': _li.id,
                'name': _li.name,
                'project_id': _li.project_id,
                'loadbalancers': None,
                'provisioning_status': _li.provisioning_status,
                'default_pool_id': _li.default_pool_id,
                'connection_limit': _li.connection_limit,
                'protocol': _li.protocol,
                'protocol_port': _li.protocol_port,
                'admin_state_up': _li.admin_state_up
            }]
    }
    li_info = copy.deepcopy(info)

    def setUp(self):
        super(TestListener, self).setUp()
        self.li_mock = self.app.client_manager.load_balancer.load_balancers
        self.li_mock.reset_mock()

        self.api_mock = mock.Mock()
        self.api_mock.listener_list.return_value = self.li_info
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock


class TestListenerList(TestListener):

    def setUp(self):
        super(TestListenerList, self).setUp()
        self.cmd = listener.ListListener(self.app, None)

    def test_listener_list_no_options(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        self.api_mock.listener_list.assert_called_with()
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))

    def test_listener_list_with_options(self):
        arglist = ['--name', 'rainbarrel']
        verifylist = [('name', 'rainbarrel')]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)
        self.api_mock.listener_list.assert_called_with(name='rainbarrel')

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))


class TestListenerDelete(TestListener):

    def setUp(self):
        super(TestListenerDelete, self).setUp()
        self.cmd = listener.DeleteListener(self.app, None)

    def test_listener_delete(self):
        arglist = [self._li.id]
        verifylist = [
            ('listener', self._li.id)
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.listener_delete.assert_called_with(
            listener_id=self._li.id)

    def test_listener_delete_failure(self):
        arglist = ['unknown_lb']
        verifylist = [
            ('listener', 'unknown_lb')
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.assertRaises(exceptions.CommandError, self.cmd.take_action,
                          parsed_args)
        self.assertNotCalled(self.api_mock.listener_delete)


class TestListenerCreate(TestListener):

    def setUp(self):
        super(TestListenerCreate, self).setUp()
        self.api_mock = mock.Mock()
        self.api_mock.listener_create.return_value = {
            'listener': self.li_info['listeners'][0]}
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock

        self.cmd = listener.CreateListener(self.app, None)

    @mock.patch('octaviaclient.osc.v2.utils.get_listener_attrs')
    def test_listener_create(self, mock_client):
        mock_client.return_value = self.li_info['listeners'][0]
        arglist = ['mock_lb_id',
                   '--name', self._li.name,
                   '--protocol', 'HTTP',
                   '--protocol-port', '80']
        verifylist = [
            ('loadbalancer', 'mock_lb_id'),
            ('name', self._li.name),
            ('protocol', 'HTTP'),
            ('protocol_port', '80')
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.listener_create.assert_called_with(
            json={'listener': self.li_info['listeners'][0]})


class TestListenerShow(TestListener):

    def setUp(self):
        super(TestListenerShow, self).setUp()
        self.api_mock = mock.Mock()
        self.api_mock.listener_list.return_value = self.li_info
        self.api_mock.listener_show.return_value = {
            'listener': self.li_info['listeners'][0]}
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock

        self.cmd = listener.ShowListener(self.app, None)

    def test_listener_show(self):
        arglist = [self._li.id]
        verifylist = [
            ('listener', self._li.id),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.listener_show.assert_called_with(listener_id=self._li.id)


class TestListenerSet(TestListener):

    def setUp(self):
        super(TestListenerSet, self).setUp()
        self.cmd = listener.SetListener(self.app, None)

    def test_listener_set(self):
        arglist = [self._li.id, '--name', 'new_name']
        verifylist = [
            ('listener', self._li.id),
            ('name', 'new_name')
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.listener_set.assert_called_with(
            self._li.id, json={'listener': {'name': 'new_name'}})
