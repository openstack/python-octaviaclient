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
import mock

from osc_lib import exceptions

from octaviaclient.osc.v2 import constants
from octaviaclient.osc.v2 import l7policy
from octaviaclient.tests.unit.osc.v2 import constants as attr_consts
from octaviaclient.tests.unit.osc.v2 import fakes


class TestL7Policy(fakes.TestOctaviaClient):

    def setUp(self):
        super(TestL7Policy, self).setUp()

        self._l7po = fakes.createFakeResource('l7policy')
        self.l7po_info = copy.deepcopy(attr_consts.L7POLICY_ATTRS)
        self.columns = copy.deepcopy(constants.L7POLICY_COLUMNS)

        self.api_mock = mock.Mock()
        self.api_mock.l7policy_list.return_value = copy.deepcopy(
            {'l7policies': [attr_consts.L7POLICY_ATTRS]})

        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock


class TestL7PolicyList(TestL7Policy):

    def setUp(self):
        super(TestL7PolicyList, self).setUp()
        self.datalist = (tuple(
            attr_consts.L7POLICY_ATTRS[k] for k in self.columns),)
        self.cmd = l7policy.ListL7Policy(self.app, None)

    def test_l7policy_list_no_options(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        self.api_mock.l7policy_list.assert_called_with()
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))


class TestL7PolicyDelete(TestL7Policy):

    def setUp(self):
        super(TestL7PolicyDelete, self).setUp()
        self.cmd = l7policy.DeleteL7Policy(self.app, None)

    def test_l7policy_delete(self):
        arglist = [self._l7po.id]
        verifylist = [
            ('l7policy', self._l7po.id)
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.l7policy_delete.assert_called_with(
            l7policy_id=self._l7po.id)

    def test_l7policy_delete_failure(self):
        arglist = ['unknown_policy']
        verifylist = [
            ('l7policy', 'unknown_policy')
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.assertRaises(exceptions.CommandError, self.cmd.take_action,
                          parsed_args)
        self.assertNotCalled(self.api_mock.l7policy_delete)


class TestL7PolicyCreate(TestL7Policy):

    def setUp(self):
        super(TestL7PolicyCreate, self).setUp()
        self.api_mock.l7policy_create.return_value = {
            'l7policy': self.l7po_info}
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock

        self.cmd = l7policy.CreateL7Policy(self.app, None)

    @mock.patch('octaviaclient.osc.v2.utils.get_l7policy_attrs')
    def test_l7policy_create(self, mock_attrs):
        mock_attrs.return_value = {
            'listener_id': self._l7po.listener_id,
            'name': self._l7po.name,
            'action': 'REDIRECT_TO_POOL',
            'redirect_pool_id': self._l7po.redirect_pool_id
        }
        arglist = ['mock_li_id',
                   '--name', self._l7po.name,
                   '--action', 'REDIRECT_TO_POOL'.lower(),
                   '--redirect-pool', self._l7po.redirect_pool_id]

        verifylist = [
            ('listener', 'mock_li_id'),
            ('name', self._l7po.name),
            ('action', 'REDIRECT_TO_POOL'),
            ('redirect_pool', self._l7po.redirect_pool_id)
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.l7policy_create.assert_called_with(
            json={'l7policy': {
                'listener_id': self._l7po.listener_id,
                'name': self._l7po.name,
                'action': 'REDIRECT_TO_POOL',
                'redirect_pool_id': self._l7po.redirect_pool_id
            }})


class TestL7PolicyShow(TestL7Policy):

    def setUp(self):
        super(TestL7PolicyShow, self).setUp()
        self.api_mock.l7policy_list.return_value = [{'id': self._l7po.id}]
        self.api_mock.l7policy_show.return_value = self.l7po_info
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock

        self.cmd = l7policy.ShowL7Policy(self.app, None)

    @mock.patch('octaviaclient.osc.v2.utils.get_l7policy_attrs')
    def test_l7policy_show(self, mock_attrs):
        mock_attrs.return_value = {'l7policy_id': self._l7po.id}
        arglist = [self._l7po.id]
        verifylist = [
            ('l7policy', self._l7po.id),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.l7policy_show.assert_called_with(
            l7policy_id=self._l7po.id)


class TestL7PolicySet(TestL7Policy):

    def setUp(self):
        super(TestL7PolicySet, self).setUp()
        self.cmd = l7policy.SetL7Policy(self.app, None)

    def test_l7policy_set(self):
        arglist = [self._l7po.id, '--name', 'new_name']
        verifylist = [
            ('l7policy', self._l7po.id),
            ('name', 'new_name')
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.l7policy_set.assert_called_with(
            self._l7po.id, json={'l7policy': {'name': 'new_name'}})


class TestL7PolicyUnset(TestL7Policy):
    PARAMETERS = ('name', 'description', 'redirect_http_code')

    def setUp(self):
        super(TestL7PolicyUnset, self).setUp()
        self.cmd = l7policy.UnsetL7Policy(self.app, None)

    def test_l7policy_unset_description(self):
        self._test_l7policy_unset_param('description')

    def test_l7policy_unset_name(self):
        self._test_l7policy_unset_param('name')

    def test_l7policy_unset_redirect_http_code(self):
        self._test_l7policy_unset_param('redirect_http_code')

    def _test_l7policy_unset_param(self, param):
        self.api_mock.l7policy_set.reset_mock()
        arg_param = param.replace('_', '-') if '_' in param else param
        arglist = [self._l7po.id, '--%s' % arg_param]
        ref_body = {'l7policy': {param: None}}
        verifylist = [
            ('l7policy', self._l7po.id),
        ]
        for ref_param in self.PARAMETERS:
            verifylist.append((ref_param, param == ref_param))
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.l7policy_set.assert_called_once_with(
            self._l7po.id, json=ref_body)

    def test_l7policy_unset_all(self):
        self.api_mock.l7policy_set.reset_mock()
        ref_body = {'l7policy': {x: None for x in self.PARAMETERS}}
        arglist = [self._l7po.id]
        for ref_param in self.PARAMETERS:
            arg_param = (ref_param.replace('_', '-') if '_' in ref_param else
                         ref_param)
            arglist.append('--%s' % arg_param)
        verifylist = list(zip(self.PARAMETERS, [True]*len(self.PARAMETERS)))
        verifylist = [('l7policy', self._l7po.id)] + verifylist
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.l7policy_set.assert_called_once_with(
            self._l7po.id, json=ref_body)

    def test_l7policy_unset_none(self):
        self.api_mock.l7policy_set.reset_mock()
        arglist = [self._l7po.id]
        verifylist = list(zip(self.PARAMETERS, [False]*len(self.PARAMETERS)))
        verifylist = [('l7policy', self._l7po.id)] + verifylist
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.l7policy_set.assert_not_called()
