#
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

from octaviaclient.osc.v2 import availabilityzoneprofile
from octaviaclient.osc.v2 import constants
from octaviaclient.tests.unit.osc.v2 import constants as attr_consts
from octaviaclient.tests.unit.osc.v2 import fakes


class TestAvailabilityzoneProfile(fakes.TestOctaviaClient):

    def setUp(self):
        super(TestAvailabilityzoneProfile, self).setUp()

        self._availabilityzoneprofile = fakes.createFakeResource(
            'availability_zone_profile')
        self.availabilityzoneprofile_info = copy.deepcopy(
            attr_consts.AVAILABILITY_ZONE_PROFILE_ATTRS)
        self.columns = copy.deepcopy(constants.AVAILABILITYZONEPROFILE_COLUMNS)

        self.api_mock = mock.Mock()
        mock_list = self.api_mock.availabilityzoneprofile_list
        mock_list.return_value = copy.deepcopy({'availability_zone_profiles': [
            attr_consts.AVAILABILITY_ZONE_PROFILE_ATTRS]})
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock


class TestAvailabilityzoneProfileList(TestAvailabilityzoneProfile):

    def setUp(self):
        super(TestAvailabilityzoneProfileList, self).setUp()
        self.datalist = (tuple(
            attr_consts.AVAILABILITY_ZONE_PROFILE_ATTRS[k]
            for k in self.columns),)
        self.cmd = availabilityzoneprofile.ListAvailabilityzoneProfile(
            self.app, None)

    def test_availabilityzoneprofile_list_no_options(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        self.api_mock.availabilityzoneprofile_list.assert_called_with()
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))

    def test_availabilityzoneprofile_list_with_options(self):
        arglist = ['--name', 'availabilityzoneprofile1']
        verifylist = [('name', 'availabilityzoneprofile1')]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)
        self.api_mock.availabilityzoneprofile_list.assert_called_with(
            name='availabilityzoneprofile1')

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))


class TestAvailabilityzoneProfileDelete(TestAvailabilityzoneProfile):

    def setUp(self):
        super(TestAvailabilityzoneProfileDelete, self).setUp()
        self.cmd = availabilityzoneprofile.DeleteAvailabilityzoneProfile(
            self.app, None)

    def test_availabilityzoneprofile_delete(self):
        arglist = [self._availabilityzoneprofile.id]
        verifylist = [
            ('availabilityzoneprofile', self._availabilityzoneprofile.id)
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.availabilityzoneprofile_delete.assert_called_with(
            availabilityzoneprofile_id=self._availabilityzoneprofile.id)

    def test_availabilityzoneprofile_delete_failure(self):
        arglist = ['unknown_availabilityzoneprofile']
        verifylist = [
            ('availabilityzoneprofile', 'unknown_availabilityzoneprofile')
        ]
        self.api_mock.availabilityzoneprofile_list.return_value = {
            'availability_zone_profiles': []}
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.assertRaises(exceptions.CommandError, self.cmd.take_action,
                          parsed_args)
        self.assertNotCalled(self.api_mock.availabilityzoneprofile_delete)


class TestAvailabilityzoneProfileCreate(TestAvailabilityzoneProfile):

    def setUp(self):
        super(TestAvailabilityzoneProfileCreate, self).setUp()
        self.api_mock.availabilityzoneprofile_create.return_value = {
            'availability_zone_profile': self.availabilityzoneprofile_info}
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock

        self.cmd = availabilityzoneprofile.CreateAvailabilityzoneProfile(
            self.app, None)

    @mock.patch('octaviaclient.osc.v2.utils.get_availabilityzoneprofile_attrs')
    def test_availabilityzoneprofile_create(self, mock_client):
        mock_client.return_value = self.availabilityzoneprofile_info
        arglist = ['--name', self._availabilityzoneprofile.name,
                   '--provider', 'mock_provider',
                   '--availability-zone-data', '{"mock_key": "mock_value"}']
        verifylist = [
            ('provider', 'mock_provider'),
            ('name', self._availabilityzoneprofile.name),
            ('availability_zone_data', '{"mock_key": "mock_value"}')
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.availabilityzoneprofile_create.assert_called_with(
            json={
                'availability_zone_profile': self.availabilityzoneprofile_info
            })


class TestAvailabilityzoneProfileShow(TestAvailabilityzoneProfile):

    def setUp(self):
        super(TestAvailabilityzoneProfileShow, self).setUp()
        mock_show = self.api_mock.availabilityzoneprofile_show
        mock_show.return_value = self.availabilityzoneprofile_info
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock

        self.cmd = availabilityzoneprofile.ShowAvailabilityzoneProfile(
            self.app, None)

    def test_availabilityzoneprofile_show(self):
        arglist = [self._availabilityzoneprofile.id]
        verifylist = [
            ('availabilityzoneprofile', self._availabilityzoneprofile.id),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.availabilityzoneprofile_show.assert_called_with(
            availabilityzoneprofile_id=self._availabilityzoneprofile.id)


class TestAvailabilityzoneProfileSet(TestAvailabilityzoneProfile):

    def setUp(self):
        super(TestAvailabilityzoneProfileSet, self).setUp()
        self.cmd = availabilityzoneprofile.SetAvailabilityzoneProfile(
            self.app, None)

    def test_availabilityzoneprofile_set(self):
        arglist = [self._availabilityzoneprofile.id, '--name', 'new_name']
        verifylist = [
            ('availabilityzoneprofile', self._availabilityzoneprofile.id),
            ('name', 'new_name'),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.availabilityzoneprofile_set.assert_called_with(
            self._availabilityzoneprofile.id, json={
                'availability_zone_profile': {
                    'name': 'new_name'
                }})
