#   Copyright 2019 Red Hat, Inc. All rights reserved.
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
from octaviaclient.osc.v2 import pool as pool
from octaviaclient.tests.unit.osc.v2 import constants as attr_consts
from octaviaclient.tests.unit.osc.v2 import fakes


class TestPool(fakes.TestOctaviaClient):

    def setUp(self):
        super().setUp()

        self._po = fakes.createFakeResource('pool')
        self.pool_info = copy.deepcopy(attr_consts.POOL_ATTRS)
        self.columns = copy.deepcopy(constants.POOL_COLUMNS)

        self.api_mock = mock.Mock()
        self.api_mock.pool_list.return_value = copy.deepcopy(
            {'pools': [attr_consts.POOL_ATTRS]})
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock


class TestPoolList(TestPool):

    def setUp(self):
        super().setUp()
        self.datalist = (tuple(
            attr_consts.POOL_ATTRS[k] for k in self.columns
        ),)
        self.cmd = pool.ListPool(self.app, None)

    def test_pool_list_no_options(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        self.api_mock.pool_list.assert_called_with()
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))

    def test_pool_list_with_tags(self):
        arglist = ['--tags', 'foo,bar']
        verifylist = [('tags', ['foo', 'bar'])]
        expected_attrs = {
            'tags': ['foo', 'bar']
        }

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        self.api_mock.pool_list.assert_called_with(**expected_attrs)
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))

    def test_pool_list_with_any_tags(self):
        arglist = ['--any-tags', 'foo,bar']
        verifylist = [('any_tags', ['foo', 'bar'])]
        expected_attrs = {
            'tags-any': ['foo', 'bar']
        }

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        self.api_mock.pool_list.assert_called_with(**expected_attrs)
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))

    def test_pool_list_with_not_tags(self):
        arglist = ['--not-tags', 'foo,bar']
        verifylist = [('not_tags', ['foo', 'bar'])]
        expected_attrs = {
            'not-tags': ['foo', 'bar']
        }

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        self.api_mock.pool_list.assert_called_with(**expected_attrs)
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))

    def test_pool_list_with_not_any_tags(self):
        arglist = ['--not-any-tags', 'foo,bar']
        verifylist = [('not_any_tags', ['foo', 'bar'])]
        expected_attrs = {
            'not-tags-any': ['foo', 'bar']
        }

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        self.api_mock.pool_list.assert_called_with(**expected_attrs)
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))


class TestPoolDelete(TestPool):

    def setUp(self):
        super().setUp()
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

    @mock.patch('osc_lib.utils.wait_for_delete')
    def test_pool_delete_wait(self, mock_wait):
        arglist = [self._po.id, '--wait']
        verifylist = [
            ('pool', self._po.id),
            ('wait', True),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.pool_delete.assert_called_with(
            pool_id=self._po.id)
        mock_wait.assert_called_once_with(
            manager=mock.ANY,
            res_id=self._po.id,
            sleep_time=mock.ANY,
            status_field='provisioning_status')

    def test_listener_delete_failure(self):
        arglist = ['unknown_pool']
        verifylist = [
            ('pool', 'unknown_pool')
        ]
        self.api_mock.pool_list.return_value = {'pools': []}
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.assertRaises(exceptions.CommandError, self.cmd.take_action,
                          parsed_args)
        self.assertNotCalled(self.api_mock.pool_delete)


class TestPoolCreate(TestPool):

    def setUp(self):
        super().setUp()
        self.api_mock.pool_create.return_value = {
            'pool': self.pool_info}
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock

        self.cmd = pool.CreatePool(self.app, None)

    @mock.patch('octaviaclient.osc.v2.utils.get_pool_attrs')
    def test_pool_create(self, mock_attrs):
        mock_attrs.return_value = self.pool_info
        arglist = ['--loadbalancer', 'mock_lb_id',
                   '--name', self._po.name,
                   '--protocol', 'HTTP',
                   '--lb-algorithm', 'ROUND_ROBIN',
                   '--enable-tls',
                   '--tls-container-ref', self._po.tls_container_ref,
                   '--ca-tls-container-ref', self._po.ca_tls_container_ref,
                   '--crl-container-ref', self._po.crl_container_ref,
                   '--tls-ciphers', self._po.tls_ciphers,
                   '--tls-version', self._po.tls_versions[0],
                   '--tls-version', self._po.tls_versions[1],
                   '--alpn-protocol', self._po.alpn_protocols[0],
                   '--alpn-protocol', self._po.alpn_protocols[1]]

        verifylist = [
            ('loadbalancer', 'mock_lb_id'),
            ('name', self._po.name),
            ('protocol', 'HTTP'),
            ('lb_algorithm', 'ROUND_ROBIN'),
            ('enable_tls', self._po.tls_enabled),
            ('tls_container_ref', self._po.tls_container_ref),
            ('ca_tls_container_ref', self._po.ca_tls_container_ref),
            ('crl_container_ref', self._po.crl_container_ref),
            ('tls_ciphers', self._po.tls_ciphers),
            ('tls_versions', self._po.tls_versions),
            ('alpn_protocols', self._po.alpn_protocols),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.pool_create.assert_called_with(
            json={'pool': self.pool_info})

    @mock.patch('octaviaclient.osc.v2.utils.get_pool_attrs')
    def test_pool_create_with_tag(self, mock_attrs):
        mock_attrs.return_value = self.pool_info
        arglist = ['--loadbalancer', 'mock_lb_id',
                   '--name', self._po.name,
                   '--protocol', 'HTTP',
                   '--lb-algorithm', 'ROUND_ROBIN',
                   '--tag', 'foo']

        verifylist = [
            ('loadbalancer', 'mock_lb_id'),
            ('name', self._po.name),
            ('protocol', 'HTTP'),
            ('lb_algorithm', 'ROUND_ROBIN'),
            ('tags', ['foo'])
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.pool_create.assert_called_with(
            json={'pool': self.pool_info})

    @mock.patch('osc_lib.utils.wait_for_status')
    @mock.patch('octaviaclient.osc.v2.utils.get_pool_attrs')
    def test_pool_create_wait(self, mock_attrs, mock_wait):
        self.pool_info['loadbalancers'] = [{'id': 'mock_lb_id'}]
        mock_attrs.return_value = self.pool_info
        self.api_mock.pool_show.return_value = self.pool_info
        arglist = ['--loadbalancer', 'mock_lb_id',
                   '--name', self._po.name,
                   '--protocol', 'HTTP',
                   '--lb-algorithm', 'ROUND_ROBIN',
                   '--wait']

        verifylist = [
            ('loadbalancer', 'mock_lb_id'),
            ('name', self._po.name),
            ('protocol', 'HTTP'),
            ('lb_algorithm', 'ROUND_ROBIN'),
            ('wait', True),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.pool_create.assert_called_with(
            json={'pool': self.pool_info})
        mock_wait.assert_called_once_with(
            status_f=mock.ANY,
            res_id='mock_lb_id',
            sleep_time=mock.ANY,
            status_field='provisioning_status')


class TestPoolShow(TestPool):

    def setUp(self):
        super().setUp()
        self.api_mock.pool_show.return_value = self.pool_info
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
        super().setUp()
        self.cmd = pool.SetPool(self.app, None)

    def test_pool_set(self):
        new_tls_id, new_ca_id, new_crl_id = (
            'test-tls-container-id', 'test-ca-tls-container-id',
            'test-crl-container-id')
        arglist = [self._po.id, '--name', 'new_name', '--tls-container-ref',
                   new_tls_id, '--ca-tls-container-ref', new_ca_id,
                   '--crl-container-ref', new_crl_id, '--enable-tls',
                   '--tls-ciphers', self._po.tls_ciphers,
                   '--tls-version', self._po.tls_versions[0],
                   '--tls-version', self._po.tls_versions[1],
                   '--alpn-protocol', self._po.alpn_protocols[0],
                   '--alpn-protocol', self._po.alpn_protocols[1]]
        verifylist = [
            ('pool', self._po.id),
            ('name', 'new_name'),
            ('tls_ciphers', self._po.tls_ciphers),
            ('tls_versions', self._po.tls_versions),
            ('alpn_protocols', self._po.alpn_protocols)
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.pool_set.assert_called_with(
            self._po.id, json={'pool': {'name': 'new_name',
                                        'tls_container_ref': new_tls_id,
                                        'ca_tls_container_ref': new_ca_id,
                                        'crl_container_ref': new_crl_id,
                                        'tls_enabled': True,
                                        'tls_ciphers': self._po.tls_ciphers,
                                        'tls_versions': self._po.tls_versions,
                                        'alpn_protocols':
                                            self._po.alpn_protocols,
                                        }})

    @mock.patch('osc_lib.utils.wait_for_status')
    def test_pool_set_wait(self, mock_wait):
        arglist = [self._po.id, '--name', 'new_name', '--wait']
        verifylist = [
            ('pool', self._po.id),
            ('name', 'new_name'),
            ('wait', True),
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.pool_set.assert_called_with(
            self._po.id, json={'pool': {'name': 'new_name'}})
        mock_wait.assert_called_once_with(
            status_f=mock.ANY,
            res_id=self._po.id,
            sleep_time=mock.ANY,
            status_field='provisioning_status')

    def test_pool_set_tag(self):
        self.api_mock.pool_show.return_value = {
            'tags': ['foo']
        }
        arglist = [self._po.id, '--tag', 'bar']
        verifylist = [
            ('pool', self._po.id),
            ('tags', ['bar']),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)

        self.api_mock.pool_set.assert_called_once()
        kwargs = self.api_mock.pool_set.mock_calls[0][2]
        tags = kwargs['json']['pool']['tags']
        self.assertEqual(2, len(tags))
        self.assertIn('foo', tags)
        self.assertIn('bar', tags)

    def test_pool_set_tag_no_tag(self):
        self.api_mock.pool_show.return_value = {
            'tags': ['foo']
        }
        arglist = [self._po.id, '--tag', 'bar', '--no-tag']
        verifylist = [
            ('pool', self._po.id),
            ('tags', ['bar']),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)

        self.api_mock.pool_set.assert_called_once_with(
            self._po.id,
            json={"pool": {"tags": ["bar"]}})


class TestPoolUnset(TestPool):
    PARAMETERS = ('name', 'description', 'ca_tls_container_ref',
                  'crl_container_ref', 'session_persistence',
                  'tls_container_ref', 'tls_versions', 'tls_ciphers')

    def setUp(self):
        super().setUp()
        self.cmd = pool.UnsetPool(self.app, None)

    def test_pool_unset_name(self):
        self._test_pool_unset_param('name')

    def test_pool_unset_name_wait(self):
        self._test_pool_unset_param_wait('name')

    def test_pool_unset_description(self):
        self._test_pool_unset_param('description')

    def test_pool_unset_ca_tls_container_ref(self):
        self._test_pool_unset_param('ca_tls_container_ref')

    def test_pool_unset_crl_container_ref(self):
        self._test_pool_unset_param('crl_container_ref')

    def test_pool_unset_session_persistence(self):
        self._test_pool_unset_param('session_persistence')

    def test_pool_unset_tls_container_ref(self):
        self._test_pool_unset_param('tls_container_ref')

    def test_pool_unset_tls_versions(self):
        self._test_pool_unset_param('tls_versions')

    def test_pool_unset_tls_ciphers(self):
        self._test_pool_unset_param('tls_ciphers')

    def _test_pool_unset_param(self, param):
        self.api_mock.pool_set.reset_mock()
        arg_param = param.replace('_', '-') if '_' in param else param
        arglist = [self._po.id, '--%s' % arg_param]
        ref_body = {'pool': {param: None}}
        verifylist = [
            ('pool', self._po.id),
        ]
        for ref_param in self.PARAMETERS:
            verifylist.append((ref_param, param == ref_param))
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.pool_set.assert_called_once_with(
            self._po.id, json=ref_body)

    @mock.patch('osc_lib.utils.wait_for_status')
    def _test_pool_unset_param_wait(self, param, mock_wait):
        self.api_mock.pool_set.reset_mock()
        arg_param = param.replace('_', '-') if '_' in param else param
        arglist = [self._po.id, '--%s' % arg_param, '--wait']
        ref_body = {'pool': {param: None}}
        verifylist = [
            ('pool', self._po.id),
            ('wait', True),
        ]
        for ref_param in self.PARAMETERS:
            verifylist.append((ref_param, param == ref_param))
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.pool_set.assert_called_once_with(
            self._po.id, json=ref_body)
        mock_wait.assert_called_once_with(
            status_f=mock.ANY,
            res_id=self._po.id,
            sleep_time=mock.ANY,
            status_field='provisioning_status')

    def test_pool_unset_all(self):
        self.api_mock.pool_set.reset_mock()
        ref_body = {'pool': {x: None for x in self.PARAMETERS}}
        arglist = [self._po.id]
        for ref_param in self.PARAMETERS:
            arg_param = (ref_param.replace('_', '-') if '_' in ref_param else
                         ref_param)
            arglist.append('--%s' % arg_param)
        verifylist = list(zip(self.PARAMETERS, [True] * len(self.PARAMETERS)))
        verifylist = [('pool', self._po.id)] + verifylist
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.pool_set.assert_called_once_with(
            self._po.id, json=ref_body)

    def test_pool_unset_none(self):
        self.api_mock.pool_set.reset_mock()
        arglist = [self._po.id]
        verifylist = list(zip(self.PARAMETERS, [False] * len(self.PARAMETERS)))
        verifylist = [('pool', self._po.id)] + verifylist
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.pool_set.assert_not_called()

    def test_pool_unset_tag(self):
        self.api_mock.pool_set.reset_mock()
        self.api_mock.pool_show.return_value = {
            'tags': ['foo', 'bar']
        }

        arglist = [self._po.id, '--tag', 'foo']
        verifylist = [
            ('pool', self._po.id),
            ('tags', ['foo']),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)

        self.api_mock.pool_set.assert_called_once_with(
            self._po.id,
            json={"pool": {"tags": ["bar"]}})

    def test_pool_unset_all_tag(self):
        self.api_mock.pool_set.reset_mock()
        self.api_mock.pool_show.return_value = {
            'tags': ['foo', 'bar']
        }

        arglist = [self._po.id, '--all-tag']
        verifylist = [
            ('pool', self._po.id),
            ('all_tag', True),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)

        self.api_mock.pool_set.assert_called_once_with(
            self._po.id,
            json={"pool": {"tags": []}})
