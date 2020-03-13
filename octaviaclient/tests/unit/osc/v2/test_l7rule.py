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

from octaviaclient.osc.v2 import constants
from octaviaclient.osc.v2 import l7rule
from octaviaclient.tests.unit.osc.v2 import constants as attr_consts
from octaviaclient.tests.unit.osc.v2 import fakes


class TestL7Rule(fakes.TestOctaviaClient):

    def setUp(self):
        super(TestL7Rule, self).setUp()

        self._l7ru = fakes.createFakeResource('l7rule')
        self.l7rule_info = copy.deepcopy(attr_consts.L7RULE_ATTRS)
        self.columns = copy.deepcopy(constants.L7RULE_COLUMNS)
        self._l7po = fakes.createFakeResource('l7policy')

        self.api_mock = mock.Mock()
        self.api_mock.l7rule_list.return_value = copy.deepcopy(
            {'rules': [attr_consts.L7RULE_ATTRS]})
        self.api_mock.l7policy_list.return_value = copy.deepcopy(
            {'l7policies': [attr_consts.L7POLICY_ATTRS]})

        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock


class TestL7RuleList(TestL7Rule):

    def setUp(self):
        super(TestL7RuleList, self).setUp()
        self.datalist = (tuple(
            attr_consts.L7RULE_ATTRS[k] for k in self.columns),)
        self.cmd = l7rule.ListL7Rule(self.app, None)

    @mock.patch('octaviaclient.osc.v2.utils.get_l7rule_attrs')
    def test_l7rule_list_no_options(self, mock_attrs):
        mock_attrs.return_value = {'l7policy_id': self._l7po.id}
        arglist = [self._l7po.id]
        verifylist = [('l7policy', self._l7po.id)]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        self.api_mock.l7rule_list.assert_called_with(l7policy_id=self._l7po.id)
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))


class TestL7RuleDelete(TestL7Rule):

    def setUp(self):
        super(TestL7RuleDelete, self).setUp()
        self.cmd = l7rule.DeleteL7Rule(self.app, None)

    @mock.patch('octaviaclient.osc.v2.utils.get_l7rule_attrs')
    def test_l7rule_delete(self, mock_attrs):
        mock_attrs.return_value = {
            'l7policy_id': self._l7po.id,
            'l7rule_id': self._l7ru.id,
        }
        arglist = [self._l7po.id, self._l7ru.id]
        verifylist = [
            ('l7policy', self._l7po.id),
            ('l7rule', self._l7ru.id)
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.l7rule_delete.assert_called_with(
            l7rule_id=self._l7ru.id,
            l7policy_id=self._l7po.id
        )

    @mock.patch('functools.partial')
    @mock.patch('osc_lib.utils.wait_for_delete')
    @mock.patch('octaviaclient.osc.v2.utils.get_l7rule_attrs')
    def test_l7rule_delete_wait(self, mock_attrs, mock_wait, mock_partial):
        mock_attrs.return_value = {
            'l7policy_id': self._l7po.id,
            'l7rule_id': self._l7ru.id,
        }
        arglist = [self._l7po.id, self._l7ru.id, '--wait']
        verifylist = [
            ('l7policy', self._l7po.id),
            ('l7rule', self._l7ru.id),
            ('wait', True),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.l7rule_delete.assert_called_with(
            l7rule_id=self._l7ru.id,
            l7policy_id=self._l7po.id
        )
        mock_partial.assert_called_once_with(
            self.api_mock.l7rule_show, self._l7po.id
        )
        mock_wait.assert_called_once_with(
            manager=mock.ANY,
            res_id=self._l7ru.id,
            sleep_time=mock.ANY,
            status_field='provisioning_status')


class TestL7RuleCreate(TestL7Rule):

    def setUp(self):
        super(TestL7RuleCreate, self).setUp()
        self.api_mock.l7rule_create.return_value = {
            'rule': self.l7rule_info}
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock

        self.cmd = l7rule.CreateL7Rule(self.app, None)

    @mock.patch('octaviaclient.osc.v2.utils.get_l7rule_attrs')
    def test_l7rule_create(self, mock_attrs):
        mock_attrs.return_value = {
            'l7policy_id': self._l7po.id,
            'compare-type': 'ENDS_WITH',
            'value': '.example.com',
            'type': 'HOST_NAME'
        }
        arglist = [self._l7po.id,
                   '--compare-type', 'ENDS_WITH',
                   '--value', '.example.com',
                   '--type', 'HOST_NAME'.lower()]

        verifylist = [
            ('l7policy', self._l7po.id),
            ('compare_type', 'ENDS_WITH'),
            ('value', '.example.com'),
            ('type', 'HOST_NAME')
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.l7rule_create.assert_called_with(
            l7policy_id=self._l7po.id,
            json={'rule': {
                'compare-type': 'ENDS_WITH',
                'value': '.example.com',
                'type': 'HOST_NAME'}
            })

    @mock.patch('osc_lib.utils.wait_for_status')
    @mock.patch('octaviaclient.osc.v2.utils.get_l7rule_attrs')
    def test_l7rule_create_wait(self, mock_attrs, mock_wait):
        mock_attrs.return_value = {
            'l7policy_id': self._l7po.id,
            'compare-type': 'ENDS_WITH',
            'value': '.example.com',
            'type': 'HOST_NAME'
        }
        self.api_mock.l7policy_show.return_value = {
            'listener_id': 'mock_listener_id'}
        self.api_mock.listener_show.return_value = {
            'loadbalancers': [{'id': 'mock_lb_id'}]}
        self.api_mock.l7rule_show.return_value = self.l7rule_info
        arglist = [self._l7po.id,
                   '--compare-type', 'ENDS_WITH',
                   '--value', '.example.com',
                   '--type', 'HOST_NAME'.lower(),
                   '--wait']

        verifylist = [
            ('l7policy', self._l7po.id),
            ('compare_type', 'ENDS_WITH'),
            ('value', '.example.com'),
            ('type', 'HOST_NAME'),
            ('wait', True),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.l7rule_create.assert_called_with(
            l7policy_id=self._l7po.id,
            json={'rule': {
                'compare-type': 'ENDS_WITH',
                'value': '.example.com',
                'type': 'HOST_NAME'}
            })
        mock_wait.assert_called_once_with(
            status_f=mock.ANY,
            res_id='mock_lb_id',
            sleep_time=mock.ANY,
            status_field='provisioning_status')


class TestL7RuleShow(TestL7Rule):

    def setUp(self):
        super(TestL7RuleShow, self).setUp()
        self.api_mock.l7rule_show.return_value = self.l7rule_info
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock

        self.cmd = l7rule.ShowL7Rule(self.app, None)

    def test_l7rule_show(self):
        arglist = [self._l7po.id, self._l7ru.id]
        verifylist = [
            ('l7policy', self._l7po.id),
            ('l7rule', self._l7ru.id)
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.l7rule_show.assert_called_with(
            l7rule_id=self._l7ru.id,
            l7policy_id=self._l7po.id
        )


class TestL7RuleSet(TestL7Rule):

    def setUp(self):
        super(TestL7RuleSet, self).setUp()
        self.cmd = l7rule.SetL7Rule(self.app, None)

    @mock.patch('octaviaclient.osc.v2.utils.get_l7rule_attrs')
    def test_l7rule_set(self, mock_attrs):
        mock_attrs.return_value = {
            'admin_state_up': False,
            'l7policy_id': self._l7po.id,
            'l7rule_id': self._l7ru.id
        }
        arglist = [
            self._l7po.id,
            self._l7ru.id,
            '--disable'
        ]
        verifylist = [
            ('l7policy', self._l7po.id),
            ('l7rule', self._l7ru.id),
            ('disable', True)
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.l7rule_set.assert_called_with(
            l7rule_id=self._l7ru.id,
            l7policy_id=self._l7po.id,
            json={'rule': {'admin_state_up': False}})

    @mock.patch('functools.partial')
    @mock.patch('osc_lib.utils.wait_for_status')
    @mock.patch('octaviaclient.osc.v2.utils.get_l7rule_attrs')
    def test_l7rule_set_wait(self, mock_attrs, mock_wait, mock_partial):
        mock_attrs.return_value = {
            'admin_state_up': False,
            'l7policy_id': self._l7po.id,
            'l7rule_id': self._l7ru.id
        }
        arglist = [
            self._l7po.id,
            self._l7ru.id,
            '--disable',
            '--wait',
        ]
        verifylist = [
            ('l7policy', self._l7po.id),
            ('l7rule', self._l7ru.id),
            ('disable', True),
            ('wait', True),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.l7rule_set.assert_called_with(
            l7rule_id=self._l7ru.id,
            l7policy_id=self._l7po.id,
            json={'rule': {'admin_state_up': False}})
        mock_partial.assert_called_once_with(
            self.api_mock.l7rule_show, self._l7po.id
        )
        mock_wait.assert_called_once_with(
            status_f=mock.ANY,
            res_id=self._l7ru.id,
            sleep_time=mock.ANY,
            status_field='provisioning_status')


class TestL7RuleUnset(TestL7Rule):
    PARAMETERS = ('invert', 'key')

    def setUp(self):
        super(TestL7RuleUnset, self).setUp()
        self.cmd = l7rule.UnsetL7Rule(self.app, None)

    def test_l7rule_unset_invert(self):
        self._test_l7rule_unset_param('invert')

    def test_l7rule_unset_invert_wait(self):
        self._test_l7rule_unset_param_wait('invert')

    def test_l7rule_unset_key(self):
        self._test_l7rule_unset_param('key')

    def _test_l7rule_unset_param(self, param):
        self.api_mock.l7rule_set.reset_mock()
        arg_param = param.replace('_', '-') if '_' in param else param
        arglist = [self._l7po.id, self._l7ru.id, '--%s' % arg_param]
        ref_body = {'rule': {param: None}}
        verifylist = [
            ('l7rule_id', self._l7ru.id),
        ]
        for ref_param in self.PARAMETERS:
            verifylist.append((ref_param, param == ref_param))
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.l7rule_set.assert_called_once_with(
            l7policy_id=self._l7po.id, l7rule_id=self._l7ru.id, json=ref_body)

    @mock.patch('functools.partial')
    @mock.patch('osc_lib.utils.wait_for_status')
    def _test_l7rule_unset_param_wait(self, param, mock_wait, mock_partial):
        self.api_mock.l7rule_set.reset_mock()
        arg_param = param.replace('_', '-') if '_' in param else param
        arglist = [self._l7po.id, self._l7ru.id, '--%s' % arg_param, '--wait']
        ref_body = {'rule': {param: None}}
        verifylist = [
            ('l7policy', self._l7po.id),
            ('l7rule_id', self._l7ru.id),
            ('wait', True),
        ]
        for ref_param in self.PARAMETERS:
            verifylist.append((ref_param, param == ref_param))
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.l7rule_set.assert_called_once_with(
            l7policy_id=self._l7po.id, l7rule_id=self._l7ru.id, json=ref_body)
        mock_partial.assert_called_once_with(
            self.api_mock.l7rule_show, self._l7po.id
        )
        mock_wait.assert_called_once_with(
            status_f=mock.ANY,
            res_id=self._l7ru.id,
            sleep_time=mock.ANY,
            status_field='provisioning_status')

    def test_l7rule_unset_all(self):
        self.api_mock.l7rule_set.reset_mock()
        ref_body = {'rule': {x: None for x in self.PARAMETERS}}
        arglist = [self._l7po.id, self._l7ru.id]
        for ref_param in self.PARAMETERS:
            arg_param = (ref_param.replace('_', '-') if '_' in ref_param else
                         ref_param)
            arglist.append('--%s' % arg_param)
        verifylist = list(zip(self.PARAMETERS, [True] * len(self.PARAMETERS)))
        verifylist = [('l7rule_id', self._l7ru.id)] + verifylist
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.l7rule_set.assert_called_once_with(
            l7policy_id=self._l7po.id, l7rule_id=self._l7ru.id, json=ref_body)

    def test_l7rule_unset_none(self):
        self.api_mock.l7rule_set.reset_mock()
        arglist = [self._l7po.id, self._l7ru.id]
        verifylist = list(zip(self.PARAMETERS, [False] * len(self.PARAMETERS)))
        verifylist = [('l7rule_id', self._l7ru.id)] + verifylist
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.l7rule_set.assert_not_called()
