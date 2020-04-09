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

import osc_lib.tests.utils as osc_test_utils
from oslo_utils import uuidutils

from octaviaclient.osc.v2 import amphora
from octaviaclient.osc.v2 import constants
from octaviaclient.tests.unit.osc.v2 import constants as attr_consts
from octaviaclient.tests.unit.osc.v2 import fakes


class TestAmphora(fakes.TestOctaviaClient):

    def setUp(self):
        super(TestAmphora, self).setUp()

        self._amp = fakes.createFakeResource('amphora')
        self.amp_info = copy.deepcopy(attr_consts.AMPHORA_ATTRS)
        self.columns = copy.deepcopy(constants.AMPHORA_COLUMNS)
        self.columns_long = copy.deepcopy(constants.AMPHORA_COLUMNS_LONG)
        self.rows = copy.deepcopy(constants.AMPHORA_ROWS)

        info_list = {'amphorae': [
            {k: v for k, v in attr_consts.AMPHORA_ATTRS.items() if (
                k in self.columns_long)},
        ]}
        self.api_mock = mock.Mock()
        self.api_mock.amphora_list.return_value = info_list
        self.api_mock.amphora_show.return_value = info_list['amphorae'][0]

        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock


class TestAmphoraList(TestAmphora):

    def setUp(self):
        super(TestAmphoraList, self).setUp()
        self.data_list = (tuple(
            attr_consts.AMPHORA_ATTRS[k] for k in self.columns),)
        self.data_list_long = (tuple(
            attr_consts.AMPHORA_ATTRS[k] for k in self.columns_long),)
        self.cmd = amphora.ListAmphora(self.app, None)

    def test_amphora_list_no_options(self):
        arglist = []
        verify_list = []

        parsed_args = self.check_parser(self.cmd, arglist, verify_list)
        columns, data = self.cmd.take_action(parsed_args)

        self.api_mock.amphora_list.assert_called_with()
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data_list, tuple(data))

    def test_amphora_list_long(self):
        arglist = ['--long']
        verify_list = []

        parsed_args = self.check_parser(self.cmd, arglist, verify_list)
        columns, data = self.cmd.take_action(parsed_args)

        self.api_mock.amphora_list.assert_called_with()
        self.assertEqual(self.columns_long, columns)
        self.assertEqual(self.data_list_long, tuple(data))

    @mock.patch('octaviaclient.osc.v2.utils.get_amphora_attrs')
    def test_amphora_list_with_loadbalancer(self, mock_client):
        mock_client.return_value = {
            'loadbalancer_id': self._amp.loadbalancer_id,
            'compute_id': self._amp.compute_id,
            'role': self._amp.role,
            'status': self._amp.status,
        }
        arglist = [
            '--loadbalancer', self._amp.loadbalancer_id,
            '--compute-id', self._amp.compute_id,
            '--role', 'Master',
            '--status', 'allocAted',
        ]
        verify_list = [
            ('loadbalancer', self._amp.loadbalancer_id),
            ('compute_id', self._amp.compute_id),
            ('role', 'MASTER'),
            ('status', 'ALLOCATED'),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verify_list)
        columns, data = self.cmd.take_action(parsed_args)
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data_list, tuple(data))


class TestAmphoraShow(TestAmphora):

    def setUp(self):
        super(TestAmphoraShow, self).setUp()
        self.cmd = amphora.ShowAmphora(self.app, None)

    def test_amphora_show_no_args(self):
        self.assertRaises(
            osc_test_utils.ParserException,
            self.check_parser, self.cmd, [], [],
        )

    @mock.patch('octaviaclient.osc.v2.utils.get_amphora_attrs')
    def test_amphora_show(self, mock_client):
        mock_client.return_value = {'amphora_id': self._amp.id}
        arglist = [self._amp.id]
        verify_list = [('amphora_id', self._amp.id)]

        parsed_args = self.check_parser(self.cmd, arglist, verify_list)
        rows, data = self.cmd.take_action(parsed_args)
        self.assertEqual(self.rows, rows)
        self.api_mock.amphora_show.assert_called_with(amphora_id=self._amp.id)


class TestAmphoraConfigure(TestAmphora):
    def setUp(self):
        super(TestAmphoraConfigure, self).setUp()
        self.cmd = amphora.ConfigureAmphora(self.app, None)

    def test_amphora_configure(self):
        arglist = [self._amp.id]
        verify_list = [('amphora_id', self._amp.id)]

        parsed_args = self.check_parser(self.cmd, arglist, verify_list)
        self.cmd.take_action(parsed_args)
        self.api_mock.amphora_configure.assert_called_with(
            amphora_id=self._amp.id)

    @mock.patch('osc_lib.utils.wait_for_status')
    def test_amphora_configure_linked_wait(self, mock_wait):
        arglist = [self._amp.id, '--wait']
        verify_list = [('amphora_id', self._amp.id)]

        parsed_args = self.check_parser(self.cmd, arglist, verify_list)
        self.cmd.take_action(parsed_args)
        self.api_mock.amphora_configure.assert_called_with(
            amphora_id=self._amp.id)
        mock_wait.assert_called_once_with(
            status_f=mock.ANY,
            res_id=self._amp.loadbalancer_id,
            sleep_time=mock.ANY,
            status_field='provisioning_status')

    @mock.patch('osc_lib.utils.wait_for_status')
    def test_amphora_configure_unlinked_wait(self, mock_wait):
        self.api_mock.amphora_show.return_value.pop('loadbalancer_id')
        arglist = [self._amp.id, '--wait']
        verify_list = [('amphora_id', self._amp.id)]

        parsed_args = self.check_parser(self.cmd, arglist, verify_list)
        self.cmd.take_action(parsed_args)
        self.api_mock.amphora_configure.assert_called_with(
            amphora_id=self._amp.id)
        # TODO(rm_work): No wait expected if the amp isn't linked to an LB?
        mock_wait.assert_not_called()


class TestAmphoraFailover(TestAmphora):
    def setUp(self):
        super(TestAmphoraFailover, self).setUp()
        self.cmd = amphora.FailoverAmphora(self.app, None)

    def test_amphora_failover(self):
        arglist = [self._amp.id]
        verify_list = [('amphora_id', self._amp.id)]

        parsed_args = self.check_parser(self.cmd, arglist, verify_list)
        self.cmd.take_action(parsed_args)
        self.api_mock.amphora_failover.assert_called_with(
            amphora_id=self._amp.id)

    @mock.patch('osc_lib.utils.wait_for_status')
    @mock.patch('osc_lib.utils.wait_for_delete')
    def test_amphora_failover_linked_wait(self, mock_wait_delete,
                                          mock_wait_active):
        arglist = [self._amp.id, '--wait']
        verify_list = [
            ('amphora_id', self._amp.id),
            ('wait', True),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verify_list)
        self.cmd.take_action(parsed_args)
        self.api_mock.amphora_failover.assert_called_with(
            amphora_id=self._amp.id)
        mock_wait_active.assert_called_once_with(
            status_f=mock.ANY,
            res_id=self._amp.loadbalancer_id,
            sleep_time=mock.ANY,
            status_field='provisioning_status')
        mock_wait_delete.assert_not_called()

    @mock.patch('osc_lib.utils.wait_for_status')
    @mock.patch('osc_lib.utils.wait_for_delete')
    def test_amphora_failover_unlinked_wait(self, mock_wait_delete,
                                            mock_wait_active):
        self.api_mock.amphora_show.return_value.pop('loadbalancer_id')
        arglist = [self._amp.id, '--wait']
        verify_list = [
            ('amphora_id', self._amp.id),
            ('wait', True),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verify_list)
        self.cmd.take_action(parsed_args)
        self.api_mock.amphora_failover.assert_called_with(
            amphora_id=self._amp.id)
        mock_wait_active.assert_not_called()
        mock_wait_delete.assert_called_once_with(
            manager=mock.ANY,
            res_id=self._amp.id,
            sleep_time=mock.ANY,
            status_field='provisioning_status')


class TestAmphoraStatsShow(TestAmphora):

    def setUp(self):
        super(TestAmphoraStatsShow, self).setUp()
        # map fake listener_id to fake bytes_in counter
        self.stats = {
            uuidutils.generate_uuid(): 12,
            uuidutils.generate_uuid(): 34,
        }
        amphora_stats_info = [
            {'listener_id': k, 'bytes_in': self.stats[k]}
            for k in self.stats]

        self.api_mock.amphora_stats_show.return_value = {
            'amphora_stats': amphora_stats_info}
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock
        self.cmd = amphora.ShowAmphoraStats(self.app, None)

    def test_amphora_stats_show(self):
        arglist = [self._amp.id]
        verifylist = [
            ('amphora_id', self._amp.id),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)
        self.api_mock.amphora_stats_show.assert_called_with(
            amphora_id=self._amp.id)

        column_idx = columns.index('bytes_in')
        total_bytes_in = sum(self.stats.values())
        self.assertEqual(data[column_idx], total_bytes_in)

    @mock.patch('octaviaclient.osc.v2.utils.get_listener_attrs')
    def test_amphora_stats_show_with_listener_id(self,
                                                 mock_get_listener_attrs):
        listener_id = list(self.stats)[0]
        arglist = ['--listener', listener_id, self._amp.id]
        verifylist = [
            ('amphora_id', self._amp.id),
        ]
        mock_get_listener_attrs.return_value = {
            'listener_id': listener_id
        }

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)
        self.api_mock.amphora_stats_show.assert_called_with(
            amphora_id=self._amp.id)

        column_idx = columns.index('bytes_in')
        bytes_in = self.stats[listener_id]
        self.assertEqual(data[column_idx], bytes_in)
