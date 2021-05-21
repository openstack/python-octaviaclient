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
from octaviaclient.osc.v2 import flavorprofile
from octaviaclient.tests.unit.osc.v2 import constants as attr_consts
from octaviaclient.tests.unit.osc.v2 import fakes


class TestFlavorProfile(fakes.TestOctaviaClient):

    def setUp(self):
        super().setUp()

        self._flavorprofile = fakes.createFakeResource('flavorprofile')
        self.flavorprofile_info = copy.deepcopy(
            attr_consts.FLAVORPROFILE_ATTRS)
        self.columns = copy.deepcopy(constants.FLAVORPROFILE_COLUMNS)

        self.api_mock = mock.Mock()
        self.api_mock.flavorprofile_list.return_value = copy.deepcopy(
            {'flavorprofiles': [attr_consts.FLAVORPROFILE_ATTRS]})
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock


class TestFlavorProfileList(TestFlavorProfile):

    def setUp(self):
        super().setUp()
        self.datalist = (tuple(
            attr_consts.FLAVORPROFILE_ATTRS[k] for k in self.columns),)
        self.cmd = flavorprofile.ListFlavorProfile(self.app, None)

    def test_flavorprofile_list_no_options(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        self.api_mock.flavorprofile_list.assert_called_with()
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))

    def test_flavorprofile_list_with_options(self):
        arglist = ['--name', 'flavorprofile1']
        verifylist = [('name', 'flavorprofile1')]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)
        self.api_mock.flavorprofile_list.assert_called_with(
            name='flavorprofile1')

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))


class TestFlavorProfileDelete(TestFlavorProfile):

    def setUp(self):
        super().setUp()
        self.cmd = flavorprofile.DeleteFlavorProfile(self.app, None)

    def test_flavorprofile_delete(self):
        arglist = [self._flavorprofile.id]
        verifylist = [
            ('flavorprofile', self._flavorprofile.id)
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.flavorprofile_delete.assert_called_with(
            flavorprofile_id=self._flavorprofile.id)

    def test_flavorprofile_delete_failure(self):
        arglist = ['unknown_flavorprofile']
        verifylist = [
            ('flavorprofile', 'unknown_flavorprofile')
        ]
        self.api_mock.flavorprofile_list.return_value = {
            'flavorprofiles': []}
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.assertRaises(exceptions.CommandError, self.cmd.take_action,
                          parsed_args)
        self.assertNotCalled(self.api_mock.flavorprofile_delete)


class TestFlavorProfileCreate(TestFlavorProfile):

    def setUp(self):
        super().setUp()
        self.api_mock.flavorprofile_create.return_value = {
            'flavorprofile': self.flavorprofile_info}
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock

        self.cmd = flavorprofile.CreateFlavorProfile(self.app, None)

    @mock.patch('octaviaclient.osc.v2.utils.get_flavorprofile_attrs')
    def test_flavorprofile_create(self, mock_client):
        mock_client.return_value = self.flavorprofile_info
        arglist = ['--name', self._flavorprofile.name,
                   '--provider', 'mock_provider',
                   '--flavor-data', '{"mock_key": "mock_value"}']
        verifylist = [
            ('provider', 'mock_provider'),
            ('name', self._flavorprofile.name),
            ('flavor_data', '{"mock_key": "mock_value"}')
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.flavorprofile_create.assert_called_with(
            json={'flavorprofile': self.flavorprofile_info})


class TestFlavorProfileShow(TestFlavorProfile):

    def setUp(self):
        super().setUp()
        self.api_mock.flavorprofile_show.return_value = self.flavorprofile_info
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock

        self.cmd = flavorprofile.ShowFlavorProfile(self.app, None)

    def test_flavorprofile_show(self):
        arglist = [self._flavorprofile.id]
        verifylist = [
            ('flavorprofile', self._flavorprofile.id),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.flavorprofile_show.assert_called_with(
            flavorprofile_id=self._flavorprofile.id)


class TestFlavorProfileSet(TestFlavorProfile):

    def setUp(self):
        super().setUp()
        self.cmd = flavorprofile.SetFlavorProfile(self.app, None)

    def test_flavorprofile_set(self):
        arglist = [self._flavorprofile.id, '--name', 'new_name']
        verifylist = [
            ('flavorprofile', self._flavorprofile.id),
            ('name', 'new_name'),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.flavorprofile_set.assert_called_with(
            self._flavorprofile.id, json={
                'flavorprofile': {
                    'name': 'new_name'
                }})
