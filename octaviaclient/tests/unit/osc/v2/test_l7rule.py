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

from octaviaclient.osc.v2 import l7rule
from octaviaclient.tests.unit.osc.v2 import fakes as ru_fakes

AUTH_TOKEN = "foobar"
AUTH_URL = "http://192.0.2.2"


class TestL7Policy(ru_fakes.TestLoadBalancerv2):

    _l7ru = ru_fakes.FakeL7Rule.create_one_l7rule()
    _l7po = ru_fakes.FakeL7Policy.create_one_l7policy()

    columns = (
        'id',
        'project_id',
        'provisioning_status',
        'compare_type',
        'type',
        'key',
        'value',
        'invert',
        'admin_state_up')

    datalist = (
        (
            _l7ru.id,
            _l7ru.project_id,
            _l7ru.provisioning_status,
            _l7ru.compare_type,
            _l7ru.type,
            _l7ru.key,
            _l7ru.value,
            _l7ru.invert,
            _l7ru.admin_state_up
        ),
    )

    info = {'rules': [{
        "provisioning_status": _l7ru.provisioning_status,
        "compare_type": _l7ru.compare_type,
        "type": _l7ru.type,
        "key": _l7ru.key,
        "project_id": _l7ru.project_id,
        "id": _l7ru.id,
        "value": _l7ru.value,
        'l7rule_id': _l7ru.id,
        'l7policy_id': _l7po.id,
        'admin_state_up': _l7ru.admin_state_up,
        'invert': _l7ru.invert
    }]}
    po_info = {'l7policies': [{
        "listener_id": _l7po.listener_id,
        "description": _l7po.description,
        "admin_state_up": _l7po.admin_state_up,
        "rules": _l7po.rules,
        "provisioning_status": _l7po.provisioning_status,
        "redirect_pool_id": _l7po.redirect_pool_id,
        "action": _l7po.action,
        "position": _l7po.position,
        "project_id": _l7po.project_id,
        "id": _l7po.id,
        "name": _l7po.name
    }]}
    l7po_info = copy.deepcopy(po_info)
    l7ru_info = copy.deepcopy(info)

    def setUp(self):
        super(TestL7Policy, self).setUp()
        self.l7ru_mock = self.app.client_manager.load_balancer.load_balancers
        self.l7ru_mock.reset_mock()

        self.api_mock = mock.Mock()
        self.api_mock.l7rule_list.return_value = self.l7ru_info
        self.api_mock.l7pool_list.return_value = self.l7po_info
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock


class TestL7RuleList(TestL7Policy):

    def setUp(self):
        super(TestL7RuleList, self).setUp()
        self.cmd = l7rule.ListL7Rule(self.app, None)

    @mock.patch('octaviaclient.osc.v2.utils.get_l7rule_attrs')
    def test_l7rule_list_no_options(self, mock_attrs):
        mock_attrs.return_value = self.l7ru_info['rules'][0]
        arglist = [self._l7po.id]
        verifylist = [('l7policy', self._l7po.id)]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        self.api_mock.l7rule_list.assert_called_with(l7policy_id=self._l7po.id)
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))


class TestL7RuleDelete(TestL7Policy):

    def setUp(self):
        super(TestL7RuleDelete, self).setUp()
        self.cmd = l7rule.DeleteL7Rule(self.app, None)

    @mock.patch('octaviaclient.osc.v2.utils.get_l7rule_attrs')
    def test_l7rule_delete(self, mock_attrs):
        mock_attrs.return_value = self.l7ru_info['rules'][0]
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


class TestL7RuleCreate(TestL7Policy):

    def setUp(self):
        super(TestL7RuleCreate, self).setUp()
        self.api_mock = mock.Mock()
        self.api_mock.l7rule_create.return_value = {
            'rule': self.l7ru_info}
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
                   '--type', 'HOST_NAME']

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


class TestL7RuleShow(TestL7Policy):

    def setUp(self):
        super(TestL7RuleShow, self).setUp()
        self.api_mock = mock.Mock()
        self.api_mock.l7policy_list.return_value = self.l7po_info
        self.api_mock.l7rule_list.return_value = self.l7ru_info
        self.api_mock.l7rule_show.return_value = {
            'rule': self.l7ru_info['rules'][0]}
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


class TestL7RuleSet(TestL7Policy):

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
