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

from octaviaclient.osc.v2 import constants
from octaviaclient.osc.v2 import provider
from octaviaclient.tests.unit.osc.v2 import constants as attr_consts
from octaviaclient.tests.unit.osc.v2 import fakes


class TestProvider(fakes.TestOctaviaClient):

    def setUp(self):
        super().setUp()

        self.columns = copy.deepcopy(constants.PROVIDER_COLUMNS)

        self.api_mock = mock.Mock()
        self.api_mock.provider_list.return_value = copy.deepcopy(
            {'providers': [attr_consts.PROVIDER_ATTRS]})
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock


class TestProviderList(TestProvider):

    def setUp(self):
        super().setUp()
        self.datalist = (tuple(
            attr_consts.PROVIDER_ATTRS[k] for k in self.columns),)
        self.cmd = provider.ListProvider(self.app, None)

    def test_provider_list(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        self.api_mock.provider_list.assert_called_with()
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))


class TestProviderCapability(fakes.TestOctaviaClient):

    def setUp(self):
        super().setUp()

        self.api_mock = mock.Mock()
        self.api_mock.provider_flavor_capability_list.return_value = (
            copy.deepcopy(
                {'flavor_capabilities': [attr_consts.CAPABILITY_ATTRS]}))
        (self.api_mock.provider_availability_zone_capability_list.
         return_value) = (
            copy.deepcopy(
                {'availability_zone_capabilities': [
                    attr_consts.CAPABILITY_ATTRS]}))
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock


class TestProviderCapabilityShow(TestProviderCapability):

    def setUp(self):
        super().setUp()
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock

        self.cmd = provider.ListProviderCapability(self.app, None)

    def test_provider_capability_list_flavor(self):
        arglist = ['--flavor', 'provider1']
        verifylist = [
            ('provider', 'provider1'),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        result = self.cmd.take_action(parsed_args)
        capabilities = list(result[1])
        self.api_mock.provider_flavor_capability_list.assert_called_with(
            provider='provider1')
        (self.api_mock.provider_availability_zone_capability_list.
            assert_not_called())
        self.assertIn(
            tuple(['flavor'] + list(attr_consts.CAPABILITY_ATTRS.values())),
            capabilities)

    def test_provider_capability_list_availability_zone(self):
        arglist = ['--availability-zone', 'provider1']
        verifylist = [
            ('provider', 'provider1'),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        result = self.cmd.take_action(parsed_args)
        capabilities = list(result[1])
        self.api_mock.provider_flavor_capability_list.assert_not_called()
        (self.api_mock.provider_availability_zone_capability_list.
            assert_called_with(provider='provider1'))
        self.assertIn(
            tuple(
                ['availability_zone'] +
                list(attr_consts.CAPABILITY_ATTRS.values())),
            capabilities)

    def test_provider_capability_list_all(self):
        arglist = ['provider1']
        verifylist = [
            ('provider', 'provider1'),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        result = self.cmd.take_action(parsed_args)
        capabilities = list(result[1])
        self.api_mock.provider_flavor_capability_list.assert_called_with(
            provider='provider1')
        (self.api_mock.provider_availability_zone_capability_list.
            assert_called_with(provider='provider1'))
        self.assertIn(
            tuple(['flavor'] + list(attr_consts.CAPABILITY_ATTRS.values())),
            capabilities)
        self.assertIn(
            tuple(
                ['availability_zone'] +
                list(attr_consts.CAPABILITY_ATTRS.values())),
            capabilities)
