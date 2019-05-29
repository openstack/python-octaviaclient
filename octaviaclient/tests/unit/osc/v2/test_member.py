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

from octaviaclient.osc.v2 import constants
from octaviaclient.osc.v2 import member
from octaviaclient.tests.unit.osc.v2 import constants as attr_consts
from octaviaclient.tests.unit.osc.v2 import fakes


class TestMember(fakes.TestOctaviaClient):

    def setUp(self):
        super(TestMember, self).setUp()

        self._mem = fakes.createFakeResource('member')
        self.mem_info = copy.deepcopy(attr_consts.MEMBER_ATTRS)
        self.columns = copy.deepcopy(constants.MEMBER_COLUMNS)

        info_list = {'members': [
            {k: v for k, v in attr_consts.MEMBER_ATTRS.items() if (
                k in self.columns)}
        ]}
        self.api_mock = mock.Mock()
        self.api_mock.member_list.return_value = info_list
        pool_dict = copy.deepcopy({'pools': [attr_consts.POOL_ATTRS]})
        pool_dict['pools'][0]['id'] = self._mem.pool_id
        self.api_mock.pool_list.return_value = pool_dict

        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock
        lb_client.neutronclient = mock.MagicMock()


class TestListMember(TestMember):

    def setUp(self):
        super(TestListMember, self).setUp()
        self.datalist = (tuple(
            attr_consts.MEMBER_ATTRS[k] for k in self.columns),)
        self.cmd = member.ListMember(self.app, None)

    def test_member_list_no_options(self):
        arglist = []
        verifylist = []

        self.assertRaises(osc_test_utils.ParserException,
                          self.check_parser, self.cmd, arglist, verifylist)

    @mock.patch('octaviaclient.osc.v2.utils.get_member_attrs')
    def test_member_list(self, mock_attrs):
        mock_attrs.return_value = {'pool_id': 'pool_id',
                                   'project_id': self._mem.project_id}
        arglist = ['pool_id']
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        columns, data = self.cmd.take_action(parsed_args)

        self.api_mock.member_list.assert_called_once_with(pool_id='pool_id')
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))


class TestCreateMember(TestMember):

    def setUp(self):
        super(TestCreateMember, self).setUp()
        self.cmd = member.CreateMember(self.app, None)
        self.api_mock.member_create.return_value = {
            'member': self.mem_info}

    @mock.patch('octaviaclient.osc.v2.utils.get_member_attrs')
    def test_member_create(self, mock_attrs):
        mock_attrs.return_value = {
            'ip_address': '192.0.2.122',
            'protocol_port': self._mem.protocol_port,
            'weight': self._mem.weight,
            'admin_state_up': True,
            'pool_id': self._mem.pool_id,
            'backup': False}

        arglist = ['pool_id', '--address', '192.0.2.122',
                   '--protocol-port', '80',
                   '--weight', '1', '--enable', '--disable-backup']
        verifylist = [
            ('address', '192.0.2.122'),
            ('protocol_port', 80),
            ('weight', 1)
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.member_create.assert_called_with(
            pool_id=self._mem.pool_id, json={
                'member': {'ip_address': '192.0.2.122',
                           'protocol_port': self._mem.protocol_port,
                           'weight': self._mem.weight,
                           'admin_state_up': True,
                           'backup': False}})


class TestMemberDelete(TestMember):

    def setUp(self):
        super(TestMemberDelete, self).setUp()
        self.cmd = member.DeleteMember(self.app, None)

    @mock.patch('octaviaclient.osc.v2.utils.get_member_attrs')
    def test_member_delete(self, mock_attrs):
        mock_attrs.return_value = {'pool_id': 'test_pool_id',
                                   'member_id': 'test_mem_id'}
        arglist = ['test_pool_id', 'test_mem_id']
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.member_delete.assert_called_with(
            pool_id='test_pool_id', member_id='test_mem_id')


class TestMemberSet(TestMember):

    def setUp(self):
        super(TestMemberSet, self).setUp()
        self.cmd = member.SetMember(self.app, None)

    @mock.patch('octaviaclient.osc.v2.utils.get_member_attrs')
    def test_member_set(self, mock_attrs):
        mock_attrs.return_value = {'pool_id': 'test_pool_id',
                                   'member_id': 'test_mem_id',
                                   'name': 'new_name',
                                   'backup': True}
        arglist = ['test_pool_id', 'test_mem_id', '--name',
                   'new_name', '--enable-backup']
        verifylist = [
            ('pool', 'test_pool_id'),
            ('member', 'test_mem_id'),
            ('name', 'new_name')
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.member_set.assert_called_with(
            pool_id='test_pool_id', member_id='test_mem_id',
            json={'member': {'name': 'new_name',
                             'backup': True}})


class TestMemberShow(TestMember):

    def setUp(self):
        super(TestMemberShow, self).setUp()
        self.api_mock.member_show.return_value = self.mem_info
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock

        self.cmd = member.ShowMember(self.app, None)

    @mock.patch('octaviaclient.osc.v2.utils.get_member_attrs')
    def test_member_show(self, mock_attrs):
        mock_attrs.return_value = {'member_id': self._mem.id,
                                   'pool_id': self._mem.pool_id}
        arglist = [self._mem.pool_id, self._mem.id]
        verifylist = [
            ('pool', self._mem.pool_id),
            ('member', self._mem.id)
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.member_show.assert_called_with(
            member_id=self._mem.id,
            pool_id=self._mem.pool_id
        )


class TestMemberUnset(TestMember):
    PARAMETERS = ('backup', 'monitor_address', 'monitor_port', 'name',
                  'weight')

    def setUp(self):
        super(TestMemberUnset, self).setUp()
        self.cmd = member.UnsetMember(self.app, None)

    def test_member_unset_backup(self):
        self._test_member_unset_param('backup')

    def test_member_unset_monitor_address(self):
        self._test_member_unset_param('monitor_address')

    def test_member_unset_monitor_port(self):
        self._test_member_unset_param('monitor_port')

    def test_member_unset_name(self):
        self._test_member_unset_param('name')

    def test_member_unset_weight(self):
        self._test_member_unset_param('weight')

    def _test_member_unset_param(self, param):
        self.api_mock.member_set.reset_mock()
        arg_param = param.replace('_', '-') if '_' in param else param
        arglist = [self._mem.pool_id, self._mem.id, '--%s' % arg_param]
        ref_body = {'member': {param: None}}
        verifylist = [('member', self._mem.id)]
        for ref_param in self.PARAMETERS:
            verifylist.append((ref_param, param == ref_param))
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.member_set.assert_called_once_with(
            pool_id=self._mem.pool_id, member_id=self._mem.id, json=ref_body)

    def test_member_unset_all(self):
        self.api_mock.pool_set.reset_mock()
        ref_body = {'member': {x: None for x in self.PARAMETERS}}
        arglist = [self._mem.pool_id, self._mem.id]
        for ref_param in self.PARAMETERS:
            arg_param = (ref_param.replace('_', '-') if '_' in ref_param else
                         ref_param)
            arglist.append('--%s' % arg_param)
        verifylist = list(zip(self.PARAMETERS, [True]*len(self.PARAMETERS)))
        verifylist = [('member', self._mem.id)] + verifylist
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.member_set.assert_called_once_with(
            member_id=self._mem.id, pool_id=self._mem.pool_id, json=ref_body)

    def test_member_unset_none(self):
        self.api_mock.pool_set.reset_mock()
        arglist = [self._mem.pool_id, self._mem.id]
        verifylist = list(zip(self.PARAMETERS, [False]*len(self.PARAMETERS)))
        verifylist = [('member', self._mem.id)] + verifylist
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.member_set.assert_not_called()
