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

import osc_lib.tests.utils as osc_test_utils

from octaviaclient.osc.v2 import amphora
from octaviaclient.osc.v2 import constants
from octaviaclient.tests.unit.osc.v2 import fakes


class TestAmphora(fakes.TestOctaviaClient):

    _amp = fakes.createFakeResource('amphora')

    columns = constants.AMPHORA_COLUMNS
    rows = constants.AMPHORA_ROWS

    data_show = (
        (
            _amp.id,
            _amp.loadbalancer_id,
            _amp.compute_id,
            _amp.lb_network_ip,
            _amp.vrrp_ip,
            _amp.ha_ip,
            _amp.vrrp_port_id,
            _amp.ha_port_id,
            _amp.cert_expiration,
            _amp.cert_busy,
            _amp.role,
            _amp.status,
            _amp.vrrp_interface,
            _amp.vrrp_id,
            _amp.vrrp_priority,
            _amp.cached_zone,
        ),
    )

    info_show = {
        'id': _amp.id,
        'loadbalancer_id': _amp.loadbalancer_id,
        'compute_id': _amp.compute_id,
        'lb_network_ip': _amp.lb_network_ip,
        'vrrp_ip': _amp.vrrp_ip,
        'ha_ip': _amp.ha_ip,
        'vrrp_port_id': _amp.vrrp_port_id,
        'ha_port_id': _amp.ha_port_id,
        'cert_expiration': _amp.cert_expiration,
        'cert_busy': _amp.cert_busy,
        'role': _amp.role,
        'status': _amp.status,
        'vrrp_interface': _amp.vrrp_interface,
        'vrrp_id': _amp.vrrp_id,
        'vrrp_priority': _amp.vrrp_priority,
        'cached_zone': _amp.cached_zone,
    }

    data_list = (
        (
            _amp.id,
            _amp.loadbalancer_id,
            _amp.status,
            _amp.role,
            _amp.lb_network_ip,
            _amp.ha_ip,
        ),
    )

    info_list = {
        'amphorae':
            [{
                'id': _amp.id,
                'loadbalancer_id': _amp.loadbalancer_id,
                'status': _amp.status,
                'role': _amp.role,
                'lb_network_ip': _amp.lb_network_ip,
                'ha_ip': _amp.ha_ip,
            }],
    }
    amp_info = copy.deepcopy(info_list)

    def setUp(self):
        super(TestAmphora, self).setUp()

        self.api_mock = mock.Mock()
        self.api_mock.amphora_list.return_value = self.amp_info
        self.api_mock.amphora_show.return_value = {
            "amphora": self.amp_info['amphorae'][0],
        }
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock


class TestAmphoraList(TestAmphora):

    def setUp(self):
        super(TestAmphoraList, self).setUp()
        self.cmd = amphora.ListAmphora(self.app, None)

    def test_amphora_list_no_options(self):
        arglist = []
        verify_list = []

        parsed_args = self.check_parser(self.cmd, arglist, verify_list)
        columns, data = self.cmd.take_action(parsed_args)

        self.api_mock.amphora_list.assert_called_with()
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data_list, tuple(data))

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
