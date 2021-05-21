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
from octaviaclient.osc.v2 import listener
from octaviaclient.tests.unit.osc.v2 import constants as attr_consts
from octaviaclient.tests.unit.osc.v2 import fakes


class TestListener(fakes.TestOctaviaClient):

    def setUp(self):
        super().setUp()

        self._listener = fakes.createFakeResource('listener')
        self.listener_info = copy.deepcopy(attr_consts.LISTENER_ATTRS)
        self.columns = copy.deepcopy(constants.LISTENER_COLUMNS)

        self.api_mock = mock.Mock()
        self.api_mock.listener_list.return_value = copy.deepcopy(
            {'listeners': [attr_consts.LISTENER_ATTRS]})
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock


class TestListenerList(TestListener):

    def setUp(self):
        super().setUp()
        self.datalist = (tuple(
            attr_consts.LISTENER_ATTRS[k] for k in self.columns),)
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
        super().setUp()
        self.cmd = listener.DeleteListener(self.app, None)

    def test_listener_delete(self):
        arglist = [self._listener.id]
        verifylist = [
            ('listener', self._listener.id)
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.listener_delete.assert_called_with(
            listener_id=self._listener.id)

    @mock.patch('osc_lib.utils.wait_for_delete')
    def test_listener_delete_wait(self, mock_wait):
        arglist = [self._listener.id, '--wait']
        verifylist = [
            ('listener', self._listener.id),
            ('wait', True),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.listener_delete.assert_called_with(
            listener_id=self._listener.id)
        mock_wait.assert_called_once_with(
            manager=mock.ANY,
            res_id=self._listener.id,
            sleep_time=mock.ANY,
            status_field='provisioning_status')

    def test_listener_delete_failure(self):
        arglist = ['unknown_lb']
        verifylist = [
            ('listener', 'unknown_lb')
        ]
        self.api_mock.listener_list.return_value = {'listeners': []}
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.assertRaises(exceptions.CommandError, self.cmd.take_action,
                          parsed_args)
        self.assertNotCalled(self.api_mock.listener_delete)


class TestListenerCreate(TestListener):

    def setUp(self):
        super().setUp()
        self.api_mock.listener_create.return_value = {
            'listener': self.listener_info}
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock

        self.cmd = listener.CreateListener(self.app, None)

    @mock.patch('octaviaclient.osc.v2.utils.get_listener_attrs')
    def test_listener_create(self, mock_client):
        mock_client.return_value = self.listener_info
        arglist = ['mock_lb_id',
                   '--name', self._listener.name,
                   '--protocol', 'HTTP',
                   '--protocol-port', '80']
        verifylist = [
            ('loadbalancer', 'mock_lb_id'),
            ('name', self._listener.name),
            ('protocol', 'HTTP'),
            ('protocol_port', 80)
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.listener_create.assert_called_with(
            json={'listener': self.listener_info})

    @mock.patch('osc_lib.utils.wait_for_status')
    @mock.patch('octaviaclient.osc.v2.utils.get_listener_attrs')
    def test_listener_create_wait(self, mock_client, mock_wait):
        self.listener_info['loadbalancers'] = [{'id': 'mock_lb_id'}]
        mock_client.return_value = self.listener_info
        self.api_mock.listener_show.return_value = self.listener_info
        arglist = ['mock_lb_id',
                   '--name', self._listener.name,
                   '--protocol', 'HTTP',
                   '--protocol-port', '80',
                   '--wait']
        verifylist = [
            ('loadbalancer', 'mock_lb_id'),
            ('name', self._listener.name),
            ('protocol', 'HTTP'),
            ('protocol_port', 80),
            ('wait', True),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.listener_create.assert_called_with(
            json={'listener': self.listener_info})
        mock_wait.assert_called_once_with(
            status_f=mock.ANY,
            res_id=self.listener_info['loadbalancers'][0]['id'],
            sleep_time=mock.ANY,
            status_field='provisioning_status')

    @mock.patch('octaviaclient.osc.v2.utils.get_listener_attrs')
    def test_tls_listener_create(self, mock_client):
        mock_client.return_value = self.listener_info
        arglist = ['mock_lb_id',
                   '--name', self._listener.name,
                   '--protocol', 'TERMINATED_HTTPS'.lower(),
                   '--protocol-port', '443',
                   '--sni-container-refs',
                   self._listener.sni_container_refs[0],
                   self._listener.sni_container_refs[1],
                   '--default-tls-container-ref',
                   self._listener.default_tls_container_ref,
                   '--client-ca-tls-container-ref',
                   self._listener.client_ca_tls_container_ref,
                   '--client-authentication',
                   self._listener.client_authentication,
                   '--client-crl-container-ref',
                   self._listener.client_crl_container_ref,
                   '--tls-ciphers',
                   self._listener.tls_ciphers,
                   '--tls-version',
                   self._listener.tls_versions[0],
                   '--tls-version',
                   self._listener.tls_versions[1],
                   '--alpn-protocol',
                   self._listener.alpn_protocols[0],
                   '--alpn-protocol',
                   self._listener.alpn_protocols[1]]

        verifylist = [
            ('loadbalancer', 'mock_lb_id'),
            ('name', self._listener.name),
            ('protocol', 'TERMINATED_HTTPS'),
            ('protocol_port', 443),
            ('sni_container_refs', self._listener.sni_container_refs),
            ('default_tls_container_ref',
             self._listener.default_tls_container_ref),
            ('client_ca_tls_container_ref',
             self._listener.client_ca_tls_container_ref),
            ('client_authentication', self._listener.client_authentication),
            ('client_crl_container_ref',
             self._listener.client_crl_container_ref),
            ('tls_ciphers',
             self._listener.tls_ciphers),
            ('tls_versions',
             self._listener.tls_versions),
            ('alpn_protocols',
             self._listener.alpn_protocols),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.listener_create.assert_called_with(
            json={'listener': self.listener_info})

    @mock.patch('octaviaclient.osc.v2.utils.get_listener_attrs')
    def test_listener_create_timeouts(self, mock_client):
        mock_client.return_value = self.listener_info
        arglist = ['mock_lb_id',
                   '--name', self._listener.name,
                   '--protocol', 'HTTP',
                   '--protocol-port', '80',
                   '--timeout-client-data', '123',
                   '--timeout-member-connect', '234',
                   '--timeout-member-data', '345',
                   '--timeout-tcp-inspect', '456']
        verifylist = [
            ('loadbalancer', 'mock_lb_id'),
            ('name', self._listener.name),
            ('protocol', 'HTTP'),
            ('protocol_port', 80),
            ('timeout_client_data', 123),
            ('timeout_member_connect', 234),
            ('timeout_member_data', 345),
            ('timeout_tcp_inspect', 456),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.listener_create.assert_called_with(
            json={'listener': self.listener_info})


class TestListenerShow(TestListener):

    def setUp(self):
        super().setUp()
        self.api_mock.listener_show.return_value = self.listener_info
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock

        self.cmd = listener.ShowListener(self.app, None)

    def test_listener_show(self):
        arglist = [self._listener.id]
        verifylist = [
            ('listener', self._listener.id),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.listener_show.assert_called_with(
            listener_id=self._listener.id)


class TestListenerSet(TestListener):

    def setUp(self):
        super().setUp()
        self.cmd = listener.SetListener(self.app, None)

    def test_listener_set(self):
        arglist = [self._listener.id, '--name', 'new_name',
                   '--sni-container-refs',
                   self._listener.sni_container_refs[0],
                   self._listener.sni_container_refs[1],
                   '--default-tls-container-ref',
                   self._listener.default_tls_container_ref,
                   '--client-ca-tls-container-ref',
                   self._listener.client_ca_tls_container_ref,
                   '--client-authentication',
                   self._listener.client_authentication,
                   '--client-crl-container-ref',
                   self._listener.client_crl_container_ref,
                   '--allowed-cidr',
                   self._listener.allowed_cidrs[0],
                   '--allowed-cidr',
                   self._listener.allowed_cidrs[1],
                   '--tls-ciphers',
                   self._listener.tls_ciphers,
                   '--tls-version',
                   self._listener.tls_versions[0],
                   '--tls-version',
                   self._listener.tls_versions[1],
                   '--alpn-protocol',
                   self._listener.alpn_protocols[0],
                   '--alpn-protocol',
                   self._listener.alpn_protocols[1]]
        verifylist = [
            ('listener', self._listener.id),
            ('name', 'new_name'),
            ('sni_container_refs', self._listener.sni_container_refs),
            ('default_tls_container_ref',
                self._listener.default_tls_container_ref),
            ('client_ca_tls_container_ref',
             self._listener.client_ca_tls_container_ref),
            ('client_authentication',
             self._listener.client_authentication),
            ('client_crl_container_ref',
             self._listener.client_crl_container_ref),
            ('allowed_cidrs', self._listener.allowed_cidrs),
            ('tls_ciphers', self._listener.tls_ciphers),
            ('tls_versions', self._listener.tls_versions),
            ('alpn_protocols', self._listener.alpn_protocols)
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.listener_set.assert_called_with(
            self._listener.id, json={
                'listener': {
                    'name': 'new_name',
                    'sni_container_refs': self._listener.sni_container_refs,
                    'default_tls_container_ref':
                        self._listener.default_tls_container_ref,
                    'client_ca_tls_container_ref':
                        self._listener.client_ca_tls_container_ref,
                    'client_authentication':
                        self._listener.client_authentication,
                    'client_crl_container_ref':
                        self._listener.client_crl_container_ref,
                    'allowed_cidrs': self._listener.allowed_cidrs,
                    'tls_ciphers': self._listener.tls_ciphers,
                    'tls_versions': self._listener.tls_versions,
                    'alpn_protocols': self._listener.alpn_protocols,
                }})

    @mock.patch('osc_lib.utils.wait_for_status')
    def test_listener_set_wait(self, mock_wait):
        arglist = [self._listener.id, '--name', 'new_name', '--wait']
        verifylist = [
            ('listener', self._listener.id),
            ('name', 'new_name'),
            ('wait', True),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.listener_set.assert_called_with(
            self._listener.id, json={'listener': {'name': 'new_name'}})
        mock_wait.assert_called_once_with(
            status_f=mock.ANY,
            res_id=self._listener.id,
            sleep_time=mock.ANY,
            status_field='provisioning_status')


class TestListenerStatsShow(TestListener):

    def setUp(self):
        super().setUp()
        listener_stats_info = {'stats': {'bytes_in': '0'}}
        self.api_mock.listener_stats_show.return_value = {
            'stats': listener_stats_info['stats']}
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock
        self.cmd = listener.ShowListenerStats(self.app, None)

    def test_listener_stats_show(self):
        arglist = [self._listener.id]
        verifylist = [
            ('listener', self._listener.id),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.listener_stats_show.assert_called_with(
            listener_id=self._listener.id)


class TestListenerUnset(TestListener):
    PARAMETERS = ('name', 'description', 'connection_limit', 'default_pool_id',
                  'default_tls_container_ref', 'sni_container_refs',
                  'insert_headers', 'timeout_client_data',
                  'timeout_member_connect', 'timeout_member_data',
                  'timeout_tcp_inspect', 'client_ca_tls_container_ref',
                  'client_authentication', 'client_crl_container_ref',
                  'allowed_cidrs', 'tls_versions', 'tls_ciphers')

    def setUp(self):
        super().setUp()
        self.cmd = listener.UnsetListener(self.app, None)

    def test_listener_unset_name(self):
        self._test_listener_unset_param('name')

    def test_listener_unset_name_wait(self):
        self._test_listener_unset_param_wait('name')

    def test_listener_unset_description(self):
        self._test_listener_unset_param('description')

    def test_listener_unset_connection_limit(self):
        self._test_listener_unset_param('connection_limit')

    def test_listener_unset_default_pool(self):
        self._test_listener_unset_param('default_pool')

    def test_listener_unset_default_tls_container_ref(self):
        self._test_listener_unset_param('default_tls_container_ref')

    def test_listener_unset_sni_container_refs(self):
        self._test_listener_unset_param('sni_container_refs')

    def test_listener_unset_insert_headers(self):
        self._test_listener_unset_param('insert_headers')

    def test_listener_unset_timeout_client_data(self):
        self._test_listener_unset_param('timeout_client_data')

    def test_listener_unset_timeout_member_connect(self):
        self._test_listener_unset_param('timeout_member_connect')

    def test_listener_unset_timeout_member_data(self):
        self._test_listener_unset_param('timeout_member_data')

    def test_listener_unset_timeout_tcp_inspect(self):
        self._test_listener_unset_param('timeout_tcp_inspect')

    def test_listener_unset_client_ca_tls_container_ref(self):
        self._test_listener_unset_param('client_ca_tls_container_ref')

    def test_listener_unset_client_authentication(self):
        self._test_listener_unset_param('client_authentication')

    def test_listener_unset_client_crl_container_ref(self):
        self._test_listener_unset_param('client_crl_container_ref')

    def test_listener_unset_allowed_cidrs(self):
        self._test_listener_unset_param('allowed_cidrs')

    def test_listener_unset_tls_versions(self):
        self._test_listener_unset_param('tls_versions')

    def test_listener_unset_tls_ciphers(self):
        self._test_listener_unset_param('tls_ciphers')

    def _test_listener_unset_param(self, param):
        self.api_mock.listener_set.reset_mock()
        arg_param = param.replace('_', '-') if '_' in param else param
        arglist = [self._listener.id, '--%s' % arg_param]
        # Handle the special rename case of default_pool rename
        if param == 'default_pool':
            param = 'default_pool_id'
        ref_body = {'listener': {param: None}}
        verifylist = [
            ('listener', self._listener.id),
        ]
        for ref_param in self.PARAMETERS:
            verifylist.append((ref_param, param == ref_param))
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.listener_set.assert_called_once_with(
            self._listener.id, json=ref_body)

    @mock.patch('osc_lib.utils.wait_for_status')
    def _test_listener_unset_param_wait(self, param, mock_wait):
        self.api_mock.listener_set.reset_mock()
        arg_param = param.replace('_', '-') if '_' in param else param
        arglist = [self._listener.id, '--%s' % arg_param, '--wait']
        # Handle the special rename case of default_pool rename
        if param == 'default_pool':
            param = 'default_pool_id'
        ref_body = {'listener': {param: None}}
        verifylist = [
            ('listener', self._listener.id),
            ('wait', True),
        ]
        for ref_param in self.PARAMETERS:
            verifylist.append((ref_param, param == ref_param))
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.listener_set.assert_called_once_with(
            self._listener.id, json=ref_body)
        mock_wait.assert_called_once_with(
            status_f=mock.ANY,
            res_id=self._listener.id,
            sleep_time=mock.ANY,
            status_field='provisioning_status')

    def test_listener_unset_all(self):
        self.api_mock.listener_set.reset_mock()
        ref_body = {'listener': {x: None for x in self.PARAMETERS}}
        arglist = [self._listener.id]
        for ref_param in self.PARAMETERS:
            # Handle the special rename case of default_pool rename
            if ref_param == 'default_pool_id':
                ref_param = 'default_pool'
            arg_param = (ref_param.replace('_', '-') if '_' in ref_param else
                         ref_param)
            arglist.append('--%s' % arg_param)
        verifylist = list(zip(self.PARAMETERS, [True] * len(self.PARAMETERS)))
        verifylist = [('listener', self._listener.id)] + verifylist
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.listener_set.assert_called_once_with(
            self._listener.id, json=ref_body)

    def test_listener_unset_none(self):
        self.api_mock.listener_set.reset_mock()
        arglist = [self._listener.id]
        verifylist = list(zip(self.PARAMETERS, [False] * len(self.PARAMETERS)))
        verifylist = [('listener', self._listener.id)] + verifylist
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.listener_set.assert_not_called()
