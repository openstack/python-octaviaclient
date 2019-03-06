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

from octaviaclient.osc.v2 import constants
from octaviaclient.osc.v2 import health_monitor
from octaviaclient.tests.unit.osc.v2 import constants as attr_consts
from octaviaclient.tests.unit.osc.v2 import fakes


class TestHealthMonitor(fakes.TestOctaviaClient):

    def setUp(self):
        super(TestHealthMonitor, self).setUp()

        self._hm = fakes.createFakeResource('hm')
        self.hm_info = copy.deepcopy(attr_consts.HM_ATTRS)
        self.columns = copy.deepcopy(constants.MONITOR_COLUMNS)

        info_list = {'healthmonitors': [
            {k: v for k, v in attr_consts.HM_ATTRS.items() if (
                k in self.columns)},
        ]}
        self.api_mock = mock.Mock()
        self.api_mock.health_monitor_list.return_value = info_list
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock


class TestHealthMonitorList(TestHealthMonitor):

    def setUp(self):
        super(TestHealthMonitorList, self).setUp()
        self.datalist = (tuple(attr_consts.HM_ATTRS[k] for k in self.columns),)
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
            'healthmonitor': self.hm_info}
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock

        self.cmd = health_monitor.CreateHealthMonitor(self.app, None)

    @mock.patch('octaviaclient.osc.v2.utils.get_health_monitor_attrs')
    def test_health_monitor_create(self, mock_client):
        mock_client.return_value = self.hm_info
        arglist = ['mock_pool_id',
                   '--name', self._hm.name,
                   '--delay', str(self._hm.delay),
                   '--timeout', str(self._hm.timeout),
                   '--max-retries', str(self._hm.max_retries),
                   '--type', self._hm.type.lower(),
                   '--http-method', self._hm.http_method.lower(),
                   '--http-version', str(self._hm.http_version),
                   '--domain-name', self._hm.domain_name]
        verifylist = [
            ('pool', 'mock_pool_id'),
            ('name', self._hm.name),
            ('delay', str(self._hm.delay)),
            ('timeout', str(self._hm.timeout)),
            ('max_retries', self._hm.max_retries),
            ('type', self._hm.type),
            ('http_method', self._hm.http_method),
            ('http_version', self._hm.http_version),
            ('domain_name', self._hm.domain_name)
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.health_monitor_create.assert_called_with(
            json={'healthmonitor': self.hm_info})


class TestHealthMonitorShow(TestHealthMonitor):

    def setUp(self):
        super(TestHealthMonitorShow, self).setUp()
        self.api_mock.health_monitor_show.return_value = {
            'healthmonitor': self.hm_info,
        }
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
        arglist = [self._hm.id, '--name', 'new_name',
                   '--http-version', str(self._hm.http_version),
                   '--domain-name', self._hm.domain_name]
        verifylist = [
            ('health_monitor', self._hm.id),
            ('name', 'new_name'),
            ('http_version', self._hm.http_version),
            ('domain_name', self._hm.domain_name)
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.health_monitor_set.assert_called_with(
            self._hm.id, json={'healthmonitor': {
                'name': 'new_name', 'http_version': self._hm.http_version,
                'domain_name': self._hm.domain_name}})
