# Copyright (c) 2018 China Telecom Corporation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import copy
from unittest import mock

from osc_lib import exceptions

from octaviaclient.osc.v2 import constants
from octaviaclient.osc.v2 import flavor
from octaviaclient.tests.unit.osc.v2 import constants as attr_consts
from octaviaclient.tests.unit.osc.v2 import fakes


class TestFlavor(fakes.TestOctaviaClient):

    def setUp(self):
        super().setUp()

        self._flavor = fakes.createFakeResource('flavor')
        self.flavor_info = copy.deepcopy(attr_consts.FLAVOR_ATTRS)
        self.columns = copy.deepcopy(constants.FLAVOR_COLUMNS)

        self.api_mock = mock.Mock()
        self.api_mock.flavor_list.return_value = copy.deepcopy(
            {'flavors': [attr_consts.FLAVOR_ATTRS]})
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock


class TestFlavorList(TestFlavor):

    def setUp(self):
        super().setUp()
        self.datalist = (tuple(
            attr_consts.FLAVOR_ATTRS[k] for k in self.columns),)
        self.cmd = flavor.ListFlavor(self.app, None)

    def test_flavor_list_no_options(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        self.api_mock.flavor_list.assert_called_with()
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))

    def test_flavor_list_with_options(self):
        arglist = ['--name', 'flavor1']
        verifylist = [('name', 'flavor1')]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)
        self.api_mock.flavor_list.assert_called_with(name='flavor1')

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))


class TestFlavorDelete(TestFlavor):

    def setUp(self):
        super().setUp()
        self.cmd = flavor.DeleteFlavor(self.app, None)

    def test_flavor_delete(self):
        arglist = [self._flavor.id]
        verifylist = [
            ('flavor', self._flavor.id)
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.flavor_delete.assert_called_with(
            flavor_id=self._flavor.id)

    def test_flavor_delete_failure(self):
        arglist = ['unknown_flavor']
        verifylist = [
            ('flavor', 'unknown_flavor')
        ]
        self.api_mock.flavor_list.return_value = {'flavors': []}
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.assertRaises(exceptions.CommandError, self.cmd.take_action,
                          parsed_args)
        self.assertNotCalled(self.api_mock.flavor_delete)


class TestFlavorCreate(TestFlavor):

    def setUp(self):
        super().setUp()
        self.api_mock.flavor_create.return_value = {
            'flavor': self.flavor_info}
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock

        self.cmd = flavor.CreateFlavor(self.app, None)

    @mock.patch('octaviaclient.osc.v2.utils.get_flavor_attrs')
    def test_flavor_create(self, mock_client):
        mock_client.return_value = self.flavor_info
        arglist = ['--name', self._flavor.name,
                   '--flavorprofile', 'mock_fvpf_id',
                   '--description', 'description for flavor']
        verifylist = [
            ('flavorprofile', 'mock_fvpf_id'),
            ('name', self._flavor.name),
            ('description', 'description for flavor')
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.flavor_create.assert_called_with(
            json={'flavor': self.flavor_info})


class TestFlavorShow(TestFlavor):

    def setUp(self):
        super().setUp()
        self.api_mock.flavor_show.return_value = self.flavor_info
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock

        self.cmd = flavor.ShowFlavor(self.app, None)

    def test_flavor_show(self):
        arglist = [self._flavor.id]
        verifylist = [
            ('flavor', self._flavor.id),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.flavor_show.assert_called_with(
            flavor_id=self._flavor.id)


class TestFlavorSet(TestFlavor):

    def setUp(self):
        super().setUp()
        self.cmd = flavor.SetFlavor(self.app, None)

    def test_flavor_set(self):
        arglist = [self._flavor.id, '--name', 'new_name',
                   '--description', 'new_desc']
        verifylist = [
            ('flavor', self._flavor.id),
            ('name', 'new_name'),
            ('description', 'new_desc')
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.flavor_set.assert_called_with(
            self._flavor.id, json={
                'flavor': {
                    'name': 'new_name',
                    'description': 'new_desc'
                }})


class TestFlavorUnset(TestFlavor):
    PARAMETERS = ('description',)

    def setUp(self):
        super().setUp()
        self.cmd = flavor.UnsetFlavor(self.app, None)

    def test_hm_unset_description(self):
        self._test_flavor_unset_param('description')

    def _test_flavor_unset_param(self, param):
        self.api_mock.flavor_set.reset_mock()
        arg_param = param.replace('_', '-') if '_' in param else param
        arglist = [self._flavor.id, '--%s' % arg_param]
        ref_body = {'flavor': {param: None}}
        verifylist = [
            ('flavor', self._flavor.id),
        ]
        for ref_param in self.PARAMETERS:
            verifylist.append((ref_param, param == ref_param))
        print(verifylist)
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.flavor_set.assert_called_once_with(
            self._flavor.id, json=ref_body)

    def test_flavor_unset_all(self):
        self.api_mock.flavor_set.reset_mock()
        ref_body = {'flavor': {x: None for x in self.PARAMETERS}}
        arglist = [self._flavor.id]
        for ref_param in self.PARAMETERS:
            arg_param = (ref_param.replace('_', '-') if '_' in ref_param else
                         ref_param)
            arglist.append('--%s' % arg_param)
        verifylist = list(zip(self.PARAMETERS, [True] * len(self.PARAMETERS)))
        verifylist = [('flavor', self._flavor.id)] + verifylist
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.flavor_set.assert_called_once_with(
            self._flavor.id, json=ref_body)

    def test_flavor_unset_none(self):
        self.api_mock.flavor_set.reset_mock()
        arglist = [self._flavor.id]
        verifylist = list(zip(self.PARAMETERS, [False] * len(self.PARAMETERS)))
        verifylist = [('flavor', self._flavor.id)] + verifylist
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.flavor_set.assert_not_called()
