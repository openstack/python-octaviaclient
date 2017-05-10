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

from octaviaclient.osc.v2 import health_monitor
from octaviaclient.tests.unit.osc.v2 import fakes as hm_fakes

AUTH_TOKEN = "foobar"
AUTH_URL = "http://192.0.2.2"


class TestHealthMonitor(hm_fakes.TestLoadBalancerv2):

    _hm = hm_fakes.FakeHM.create_one_health_monitor()

    columns = ('id', 'name', 'project_id', 'type', 'admin_state_up')

    datalist = (
        (
            _hm.id,
            _hm.name,
            _hm.project_id,
            _hm.type,
            _hm.admin_state_up
        ),
    )

    info = {
        'healthmonitors':
            [{
                "project_id": _hm.project_id,
                "name": _hm.name,
                "admin_state_up": True,
                "pools": _hm.pools,
                "created_at": _hm.created_at,
                "delay": _hm.delay,
                "expected_codes": _hm.expected_codes,
                "max_retries": _hm.max_retries,
                "http_method": _hm.http_method,
                "timeout": _hm.timeout,
                "max_retries_down": _hm.max_retries_down,
                "url_path": _hm.url_path,
                "type": _hm.type,
                "id": _hm.id
            }]
    }
    hm_info = copy.deepcopy(info)

    def setUp(self):
        super(TestHealthMonitor, self).setUp()
        self.li_mock = self.app.client_manager.load_balancer.load_balancers
        self.li_mock.reset_mock()

        self.api_mock = mock.Mock()
        self.api_mock.health_monitor_list.return_value = self.hm_info
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock


class TestHealthMonitorList(TestHealthMonitor):

    def setUp(self):
        super(TestHealthMonitorList, self).setUp()
        self.cmd = health_monitor.ListHealthMonitor(self.app, None)

    def test_health_monitor_list_no_options(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        self.api_mock.health_monitor_list.assert_called_with()
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))


class TestHealthMonitorDelete(TestHealthMonitor):

    def setUp(self):
        super(TestHealthMonitorDelete, self).setUp()
        self.cmd = health_monitor.DeleteHealthMonitor(self.app, None)

    def test_health_monitor_delete(self):
        arglist = [self._hm.id]
        verifylist = [
            ('health_monitor', self._hm.id)
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.health_monitor_delete.assert_called_with(
            health_monitor_id=self._hm.id)

    def test_health_monitor_delete_failure(self):
        arglist = ['unknown_hm']
        verifylist = [
            ('health_monitor', 'unknown_hm')
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.assertRaises(exceptions.CommandError, self.cmd.take_action,
                          parsed_args)
        self.assertNotCalled(self.api_mock.health_monitor_delete)


class TestHealthMonitorCreate(TestHealthMonitor):

    def setUp(self):
        super(TestHealthMonitorCreate, self).setUp()
        self.api_mock = mock.Mock()
        self.api_mock.health_monitor_create.return_value = {
            'healthmonitor': self.hm_info['healthmonitors'][0]}
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock

        self.cmd = health_monitor.CreateHealthMonitor(self.app, None)

    @mock.patch('octaviaclient.osc.v2.utils.get_health_monitor_attrs')
    def test_health_monitor_create(self, mock_client):
        mock_client.return_value = self.hm_info['healthmonitors'][0]
        arglist = ['mock_pool_id',
                   '--name', self._hm.name,
                   '--delay', str(self._hm.delay),
                   '--timeout', str(self._hm.timeout),
                   '--max-retries', str(self._hm.max_retries),
                   '--type', self._hm.type]
        verifylist = [
            ('pool', 'mock_pool_id'),
            ('name', self._hm.name),
            ('delay', str(self._hm.delay)),
            ('timeout', str(self._hm.timeout)),
            ('max_retries', self._hm.max_retries),
            ('type', self._hm.type)
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.health_monitor_create.assert_called_with(
            json={'healthmonitor': self.hm_info['healthmonitors'][0]})


class TestHealthMonitorShow(TestHealthMonitor):

    def setUp(self):
        super(TestHealthMonitorShow, self).setUp()
        self.api_mock = mock.Mock()
        self.api_mock.health_monitor_list.return_value = self.hm_info
        self.api_mock.health_monitor_show.return_value = {
            'healthmonitor': self.hm_info['healthmonitors'][0]}
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock

        self.cmd = health_monitor.ShowHealthMonitor(self.app, None)

    def test_health_monitor_show(self):
        arglist = [self._hm.id]
        verifylist = [
            ('health_monitor', self._hm.id),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.health_monitor_show.assert_called_with(
            health_monitor_id=self._hm.id)


class TestHealthMonitorSet(TestHealthMonitor):

    def setUp(self):
        super(TestHealthMonitorSet, self).setUp()
        self.cmd = health_monitor.SetHealthMonitor(self.app, None)

    def test_health_monitor_set(self):
        arglist = [self._hm.id, '--name', 'new_name']
        verifylist = [
            ('health_monitor', self._hm.id),
            ('name', 'new_name')
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.health_monitor_set.assert_called_with(
            self._hm.id, json={'healthmonitor': {'name': 'new_name'}})
