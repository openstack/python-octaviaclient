#   Copyright 2019 Red Hat, Inc. All rights reserved.
#
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
from unittest import mock

from osc_lib import exceptions

from octaviaclient.osc.v2 import constants
from octaviaclient.osc.v2 import health_monitor
from octaviaclient.tests.unit.osc.v2 import constants as attr_consts
from octaviaclient.tests.unit.osc.v2 import fakes


class TestHealthMonitor(fakes.TestOctaviaClient):

    def setUp(self):
        super().setUp()

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
        super().setUp()
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
        super().setUp()
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

    @mock.patch('osc_lib.utils.wait_for_delete')
    def test_health_monitor_delete_wait(self, mock_wait):
        arglist = [self._hm.id, '--wait']
        verifylist = [
            ('health_monitor', self._hm.id),
            ('wait', True),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.health_monitor_delete.assert_called_with(
            health_monitor_id=self._hm.id)
        mock_wait.assert_called_once_with(
            manager=mock.ANY,
            res_id=self._hm.id,
            sleep_time=mock.ANY,
            status_field='provisioning_status')

    def test_health_monitor_delete_failure(self):
        arglist = ['unknown_hm']
        verifylist = [
            ('health_monitor', 'unknown_hm')
        ]
        self.api_mock.health_monitor_list.return_value = {
            'healthmonitors': []}
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.assertRaises(exceptions.CommandError, self.cmd.take_action,
                          parsed_args)
        self.assertNotCalled(self.api_mock.health_monitor_delete)


class TestHealthMonitorCreate(TestHealthMonitor):

    def setUp(self):
        super().setUp()
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

    @mock.patch('osc_lib.utils.wait_for_status')
    @mock.patch('octaviaclient.osc.v2.utils.get_health_monitor_attrs')
    def test_health_monitor_create_wait(self, mock_client, mock_wait):
        self.hm_info['pools'] = [{'id': 'mock_pool_id'}]
        mock_client.return_value = self.hm_info
        self.api_mock.pool_show.return_value = {
            'loadbalancers': [{'id': 'mock_lb_id'}]}
        self.api_mock.health_monitor_show.return_value = self.hm_info
        arglist = ['mock_pool_id',
                   '--name', self._hm.name,
                   '--delay', str(self._hm.delay),
                   '--timeout', str(self._hm.timeout),
                   '--max-retries', str(self._hm.max_retries),
                   '--type', self._hm.type.lower(),
                   '--http-method', self._hm.http_method.lower(),
                   '--http-version', str(self._hm.http_version),
                   '--domain-name', self._hm.domain_name,
                   '--wait']
        verifylist = [
            ('pool', 'mock_pool_id'),
            ('name', self._hm.name),
            ('delay', str(self._hm.delay)),
            ('timeout', str(self._hm.timeout)),
            ('max_retries', self._hm.max_retries),
            ('type', self._hm.type),
            ('http_method', self._hm.http_method),
            ('http_version', self._hm.http_version),
            ('domain_name', self._hm.domain_name),
            ('wait', True),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.health_monitor_create.assert_called_with(
            json={'healthmonitor': self.hm_info})
        mock_wait.assert_called_once_with(
            status_f=mock.ANY,
            res_id='mock_lb_id',
            sleep_time=mock.ANY,
            status_field='provisioning_status')


class TestHealthMonitorShow(TestHealthMonitor):

    def setUp(self):
        super().setUp()
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
        super().setUp()
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

    @mock.patch('osc_lib.utils.wait_for_status')
    def test_health_monitor_set_wait(self, mock_wait):
        arglist = [self._hm.id, '--name', 'new_name', '--wait']
        verifylist = [
            ('health_monitor', self._hm.id),
            ('name', 'new_name'),
            ('wait', True),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.health_monitor_set.assert_called_with(
            self._hm.id, json={'healthmonitor': {'name': 'new_name'}})
        mock_wait.assert_called_once_with(
            status_f=mock.ANY,
            res_id=self._hm.id,
            sleep_time=mock.ANY,
            status_field='provisioning_status')


class TestHealthMonitorUnset(TestHealthMonitor):
    PARAMETERS = ('name', 'domain_name', 'expected_codes', 'http_method',
                  'http_version', 'max_retries_down', 'url_path')

    def setUp(self):
        super().setUp()
        self.cmd = health_monitor.UnsetHealthMonitor(self.app, None)

    def test_hm_unset_domain_name(self):
        self._test_hm_unset_param('domain_name')

    def test_hm_unset_expected_codes(self):
        self._test_hm_unset_param('expected_codes')

    def test_hm_unset_http_method(self):
        self._test_hm_unset_param('http_method')

    def test_hm_unset_http_version(self):
        self._test_hm_unset_param('http_version')

    def test_hm_unset_max_retries_down(self):
        self._test_hm_unset_param('max_retries_down')

    def test_hm_unset_name(self):
        self._test_hm_unset_param('name')

    def test_hm_unset_name_wait(self):
        self._test_hm_unset_param_wait('name')

    def test_hm_unset_url_path(self):
        self._test_hm_unset_param('url_path')

    def _test_hm_unset_param(self, param):
        self.api_mock.health_monitor_set.reset_mock()
        arg_param = param.replace('_', '-') if '_' in param else param
        arglist = [self._hm.id, '--%s' % arg_param]
        ref_body = {'healthmonitor': {param: None}}
        verifylist = [
            ('health_monitor', self._hm.id),
        ]
        for ref_param in self.PARAMETERS:
            verifylist.append((ref_param, param == ref_param))
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.health_monitor_set.assert_called_once_with(
            self._hm.id, json=ref_body)

    @mock.patch('osc_lib.utils.wait_for_status')
    def _test_hm_unset_param_wait(self, param, mock_wait):
        self.api_mock.health_monitor_set.reset_mock()
        arg_param = param.replace('_', '-') if '_' in param else param
        arglist = [self._hm.id, '--%s' % arg_param, '--wait']
        ref_body = {'healthmonitor': {param: None}}
        verifylist = [
            ('health_monitor', self._hm.id),
            ('wait', True),
        ]
        for ref_param in self.PARAMETERS:
            verifylist.append((ref_param, param == ref_param))
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.health_monitor_set.assert_called_once_with(
            self._hm.id, json=ref_body)
        mock_wait.assert_called_once_with(
            status_f=mock.ANY,
            res_id=self._hm.id,
            sleep_time=mock.ANY,
            status_field='provisioning_status')

    def test_hm_unset_all(self):
        self.api_mock.health_monitor_set.reset_mock()
        ref_body = {'healthmonitor': {x: None for x in self.PARAMETERS}}
        arglist = [self._hm.id]
        for ref_param in self.PARAMETERS:
            arg_param = (ref_param.replace('_', '-') if '_' in ref_param else
                         ref_param)
            arglist.append('--%s' % arg_param)
        verifylist = list(zip(self.PARAMETERS, [True] * len(self.PARAMETERS)))
        verifylist = [('health_monitor', self._hm.id)] + verifylist
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.health_monitor_set.assert_called_once_with(
            self._hm.id, json=ref_body)

    def test_hm_unset_none(self):
        self.api_mock.health_monitor_set.reset_mock()
        arglist = [self._hm.id]
        verifylist = list(zip(self.PARAMETERS, [False] * len(self.PARAMETERS)))
        verifylist = [('health_monitor', self._hm.id)] + verifylist
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.health_monitor_set.assert_not_called()
