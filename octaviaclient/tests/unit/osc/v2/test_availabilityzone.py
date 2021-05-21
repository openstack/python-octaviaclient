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

from octaviaclient.osc.v2 import availabilityzone
from octaviaclient.osc.v2 import constants
from octaviaclient.tests.unit.osc.v2 import constants as attr_consts
from octaviaclient.tests.unit.osc.v2 import fakes


class TestAvailabilityzone(fakes.TestOctaviaClient):

    def setUp(self):
        super().setUp()

        self._availabilityzone = fakes.createFakeResource('availability_zone')
        self.availabilityzone_info = copy.deepcopy(
            attr_consts.AVAILABILITY_ZONE_ATTRS)
        self.columns = copy.deepcopy(constants.AVAILABILITYZONE_COLUMNS)

        self.api_mock = mock.Mock()
        self.api_mock.availabilityzone_list.return_value = copy.deepcopy(
            {'availability_zones': [attr_consts.AVAILABILITY_ZONE_ATTRS]})
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock


class TestAvailabilityzoneList(TestAvailabilityzone):

    def setUp(self):
        super().setUp()
        self.datalist = (tuple(
            attr_consts.AVAILABILITY_ZONE_ATTRS[k] for k in self.columns),)
        self.cmd = availabilityzone.ListAvailabilityzone(self.app, None)

    def test_availabilityzone_list_no_options(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        self.api_mock.availabilityzone_list.assert_called_with()
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))

    def test_availabilityzone_list_with_options(self):
        arglist = ['--name', 'availabilityzone1']
        verifylist = [('name', 'availabilityzone1')]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)
        self.api_mock.availabilityzone_list.assert_called_with(
            name='availabilityzone1')

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))


class TestAvailabilityzoneDelete(TestAvailabilityzone):

    def setUp(self):
        super().setUp()
        self.cmd = availabilityzone.DeleteAvailabilityzone(self.app, None)

    def test_availabilityzone_delete(self):
        arglist = [self._availabilityzone.name]
        verifylist = [
            ('availabilityzone', self._availabilityzone.name)
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.availabilityzone_delete.assert_called_with(
            availabilityzone_name=self._availabilityzone.name)

    def test_availabilityzone_delete_failure(self):
        arglist = ['unknown_availabilityzone']
        verifylist = [
            ('availabilityzone', 'unknown_availabilityzone')
        ]
        self.api_mock.availabilityzone_list.return_value = {
            'availability_zones': []}
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.assertRaises(exceptions.CommandError, self.cmd.take_action,
                          parsed_args)
        self.assertNotCalled(self.api_mock.availabilityzone_delete)


class TestAvailabilityzoneCreate(TestAvailabilityzone):

    def setUp(self):
        super().setUp()
        self.api_mock.availabilityzone_create.return_value = {
            'availability_zone': self.availabilityzone_info}
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock

        self.cmd = availabilityzone.CreateAvailabilityzone(self.app, None)

    @mock.patch('octaviaclient.osc.v2.utils.get_availabilityzone_attrs')
    def test_availabilityzone_create(self, mock_client):
        mock_client.return_value = self.availabilityzone_info
        arglist = ['--name', self._availabilityzone.name,
                   '--availabilityzoneprofile', 'mock_azpf_id',
                   '--description', 'description for availabilityzone']
        verifylist = [
            ('availabilityzoneprofile', 'mock_azpf_id'),
            ('name', self._availabilityzone.name),
            ('description', 'description for availabilityzone')
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.availabilityzone_create.assert_called_with(
            json={'availability_zone': self.availabilityzone_info})


class TestAvailabilityzoneShow(TestAvailabilityzone):

    def setUp(self):
        super().setUp()
        mock_show = self.api_mock.availabilityzone_show
        mock_show.return_value = self.availabilityzone_info
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock

        self.cmd = availabilityzone.ShowAvailabilityzone(self.app, None)

    def test_availabilityzone_show(self):
        arglist = [self._availabilityzone.name]
        verifylist = [
            ('availabilityzone', self._availabilityzone.name),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.availabilityzone_show.assert_called_with(
            availabilityzone_name=self._availabilityzone.name)


class TestAvailabilityzoneSet(TestAvailabilityzone):

    def setUp(self):
        super().setUp()
        self.cmd = availabilityzone.SetAvailabilityzone(self.app, None)

    def test_availabilityzone_set(self):
        arglist = [self._availabilityzone.name, '--description', 'new_desc']
        verifylist = [
            ('availabilityzone', self._availabilityzone.name),
            ('description', 'new_desc'),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.availabilityzone_set.assert_called_with(
            self._availabilityzone.name, json={
                'availability_zone': {
                    'description': 'new_desc'
                }})


class TestAvailabilityzoneUnset(TestAvailabilityzone):
    PARAMETERS = ('description',)

    def setUp(self):
        super().setUp()
        self.cmd = availabilityzone.UnsetAvailabilityzone(self.app, None)

    def test_hm_unset_description(self):
        self._test_availabilityzone_unset_param('description')

    def _test_availabilityzone_unset_param(self, param):
        self.api_mock.availabilityzone_set.reset_mock()
        arg_param = param.replace('_', '-') if '_' in param else param
        arglist = [self._availabilityzone.name, '--%s' % arg_param]
        ref_body = {'availability_zone': {param: None}}
        verifylist = [
            ('availabilityzone', self._availabilityzone.name),
        ]
        for ref_param in self.PARAMETERS:
            verifylist.append((ref_param, param == ref_param))
        print(verifylist)
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.availabilityzone_set.assert_called_once_with(
            self._availabilityzone.name, json=ref_body)

    def test_availabilityzone_unset_all(self):
        self.api_mock.availabilityzone_set.reset_mock()
        ref_body = {'availability_zone': {x: None for x in self.PARAMETERS}}
        arglist = [self._availabilityzone.name]
        for ref_param in self.PARAMETERS:
            arg_param = (ref_param.replace('_', '-') if '_' in ref_param else
                         ref_param)
            arglist.append('--%s' % arg_param)
        verifylist = list(zip(self.PARAMETERS, [True] * len(self.PARAMETERS)))
        verifylist = [('availabilityzone',
                       self._availabilityzone.name)] + verifylist
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.availabilityzone_set.assert_called_once_with(
            self._availabilityzone.name, json=ref_body)

    def test_availabilityzone_unset_none(self):
        self.api_mock.availabilityzone_set.reset_mock()
        arglist = [self._availabilityzone.name]
        verifylist = list(zip(self.PARAMETERS, [False] * len(self.PARAMETERS)))
        verifylist = [('availabilityzone',
                       self._availabilityzone.name)] + verifylist
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.availabilityzone_set.assert_not_called()
