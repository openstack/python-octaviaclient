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

from octaviaclient.osc.v2 import member
from octaviaclient.tests.unit.osc.v2 import fakes as mem_fakes
from osc_lib.tests.utils import ParserException


class TestMember(mem_fakes.TestLoadBalancerv2):

    mem = mem_fakes.FakeMember.create_member()

    columns = (
        'id',
        'name',
        'project_id',
        'provisioning_status',
        'address',
        'protocol_port',
        'operating_status',
        'weight'
    )

    datalist = (
        (
            mem.id,
            mem.name,
            mem.project_id,
            mem.provisioning_status,
            mem.address,
            mem.protocol_port,
            mem.operating_status,
            mem.weight
        ),
    )

    info = {'members': [{
        'id': mem.id,
        'name': mem.name,
        'project_id': mem.project_id,
        'provisioning_status': mem.provisioning_status,
        'address': mem.address,
        'protocol_port': mem.protocol_port,
        'operating_status': mem.operating_status,
        'weight': mem.weight,
        'pool_id': mem.pool_id}]
    }

    mem_info = copy.deepcopy(info)

    def setUp(self):
        super(TestMember, self).setUp()
        self.mem_mock = self.app.client_manager.load_balancer.load_balancers
        self.mem_mock.reset_mock()

        self.api_mock = mock.Mock()
        self.api_mock.member_list.return_value = self.mem_info
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock
        lb_client.neutronclient = mock.MagicMock()


class TestListMember(TestMember):

    def setUp(self):
        super(TestListMember, self).setUp()
        self.cmd = member.ListMember(self.app, None)

    def test_member_list_no_options(self):
        arglist = []
        verifylist = []

        self.assertRaises(ParserException,
                          self.check_parser, self.cmd, arglist, verifylist)

    @mock.patch('octaviaclient.osc.v2.utils.get_member_attrs')
    def test_member_list(self, mock_attrs):
        mock_attrs.return_value = {'pool_id': 'pool_id',
                                   'project_id': self.mem.project_id}
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
            'protocol_port': self.mem.protocol_port,
            'weight': self.mem.weight,
            'admin_state_up': True,
            'pool_id': self.mem.pool_id}

        arglist = ['pool_id', '--address', '192.0.2.122',
                   '--protocol-port', '80',
                   '--weight', '1', '--enable']
        verifylist = [
            ('address', '192.0.2.122'),
            ('protocol_port', 80),
            ('weight', 1)
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.member_create.assert_called_with(
            pool_id=self.mem.pool_id, json={
                'member': {'ip_address': '192.0.2.122',
                           'protocol_port': self.mem.protocol_port,
                           'weight': self.mem.weight,
                           'admin_state_up': True}})


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
                                   'name': 'new_name'}
        arglist = ['test_pool_id', 'test_mem_id', '--name',
                   'new_name']
        verifylist = [
            ('pool', 'test_pool_id'),
            ('member', 'test_mem_id'),
            ('name', 'new_name')
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.member_set.assert_called_with(
            pool_id='test_pool_id', member_id='test_mem_id',
            json={'member': {'name': 'new_name'}})


class TestMemberShow(TestMember):

    def setUp(self):
        super(TestMemberShow, self).setUp()
        self.api_mock = mock.Mock()
        self.api_mock.member_list.return_value = self.mem_info
        self.api_mock.member_show.return_value = {
            'member': self.mem_info['members'][0]}
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock

        self.cmd = member.ShowMember(self.app, None)

    @mock.patch('octaviaclient.osc.v2.utils.get_member_attrs')
    def test_member_show(self, mock_attrs):
        mock_attrs.return_value = {'member_id': self.mem.id,
                                   'pool_id': self.mem.pool_id}
        arglist = [self.mem.pool_id, self.mem.id]
        verifylist = [
            ('pool', self.mem.pool_id),
            ('member', self.mem.id)
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.member_show.assert_called_with(
            member_id=self.mem.id,
            pool_id=self.mem.pool_id
        )
