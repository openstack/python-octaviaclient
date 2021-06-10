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
import itertools
from unittest import mock

import munch
from osc_lib import exceptions
from oslo_utils import uuidutils

from octaviaclient.osc.v2 import constants
from octaviaclient.osc.v2 import load_balancer
from octaviaclient.tests.unit.osc.v2 import constants as attr_consts
from octaviaclient.tests.unit.osc.v2 import fakes


class TestLoadBalancer(fakes.TestOctaviaClient):

    def setUp(self):
        super().setUp()

        self._lb = fakes.createFakeResource('loadbalancer')
        self.lb_info = copy.deepcopy(attr_consts.LOADBALANCER_ATTRS)
        self.columns = copy.deepcopy(constants.LOAD_BALANCER_COLUMNS)

        self.api_mock = mock.Mock()
        self.api_mock.load_balancer_list.return_value = copy.deepcopy(
            {'loadbalancers': [attr_consts.LOADBALANCER_ATTRS]})

        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock
        lb_client.neutronclient = mock.MagicMock()


class TestLoadBalancerList(TestLoadBalancer):

    def setUp(self):
        super().setUp()
        self.datalist = (tuple(
            attr_consts.LOADBALANCER_ATTRS[k] for k in self.columns),)
        self.cmd = load_balancer.ListLoadBalancer(self.app, None)

    def test_load_balancer_list_no_options(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)
        self.api_mock.load_balancer_list.assert_called_with()

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))

    def test_load_balancer_list_with_name(self):
        arglist = ['--name', 'rainbarrel']
        verifylist = [('name', 'rainbarrel')]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)
        self.api_mock.load_balancer_list.assert_called_with(name='rainbarrel')

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))

    @mock.patch('octaviaclient.osc.v2.utils.get_loadbalancer_attrs')
    def test_load_balancer_list_with_network(self, mock_client):
        mock_client.return_value = {
            'vip_network_id': self._lb.vip_network_id,
        }
        arglist = [
            '--vip-network-id', self._lb.vip_network_id,
        ]
        verify_list = [
            ('vip_network_id', self._lb.vip_network_id),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verify_list)
        columns, data = self.cmd.take_action(parsed_args)
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))

    @mock.patch('octaviaclient.osc.v2.utils.get_loadbalancer_attrs')
    def test_load_balancer_list_with_subnet(self, mock_client):
        mock_client.return_value = {
            'vip_subnet_id': self._lb.vip_subnet_id,
        }
        arglist = [
            '--vip-subnet-id', self._lb.vip_subnet_id,
        ]
        verify_list = [
            ('vip_subnet_id', self._lb.vip_subnet_id),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verify_list)
        columns, data = self.cmd.take_action(parsed_args)
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))

    @mock.patch('octaviaclient.osc.v2.utils.get_loadbalancer_attrs')
    def test_load_balancer_list_with_qos_policy(self, mock_client):
        mock_client.return_value = {
            'vip_qos_policy_id': self._lb.vip_qos_policy_id,
        }
        arglist = [
            '--vip-qos-policy-id', self._lb.vip_qos_policy_id,
        ]
        verify_list = [
            ('vip_qos_policy_id', self._lb.vip_qos_policy_id),

        ]

        parsed_args = self.check_parser(self.cmd, arglist, verify_list)
        columns, data = self.cmd.take_action(parsed_args)
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))

    @mock.patch('octaviaclient.osc.v2.utils.get_loadbalancer_attrs')
    def test_load_balancer_list_with_provisioning_status(self, mock_client):
        mock_client.return_value = {
            'provisioning_status': self._lb.provisioning_status,
        }
        arglist = [
            '--provisioning-status', 'active',
        ]
        verify_list = [
            ('provisioning_status', 'ACTIVE'),

        ]

        parsed_args = self.check_parser(self.cmd, arglist, verify_list)
        columns, data = self.cmd.take_action(parsed_args)
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))

    @mock.patch('octaviaclient.osc.v2.utils.get_loadbalancer_attrs')
    def test_load_balancer_list_with_operating_status(self, mock_client):
        mock_client.return_value = {
            'operating_status': self._lb.operating_status,
        }
        arglist = [
            '--operating-status', 'ONLiNE',
        ]
        verify_list = [
            ('operating_status', 'ONLINE'),

        ]

        parsed_args = self.check_parser(self.cmd, arglist, verify_list)
        columns, data = self.cmd.take_action(parsed_args)
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))

    @mock.patch('octaviaclient.osc.v2.utils.get_loadbalancer_attrs')
    def test_load_balancer_list_with_provider(self, mock_client):
        mock_client.return_value = {
            'provider': self._lb.provider,
        }
        arglist = [
            '--provider', 'octavia',
        ]
        verify_list = [
            ('provider', 'octavia'),

        ]

        parsed_args = self.check_parser(self.cmd, arglist, verify_list)
        columns, data = self.cmd.take_action(parsed_args)
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))

    @mock.patch('octaviaclient.osc.v2.utils.get_loadbalancer_attrs')
    def test_load_balancer_list_with_flavor(self, mock_client):
        mock_client.return_value = {
            'flavor_id': self._lb.flavor_id,
        }
        arglist = [
            '--flavor', self._lb.flavor_id,
        ]
        verify_list = [
            ('flavor', self._lb.flavor_id),

        ]

        parsed_args = self.check_parser(self.cmd, arglist, verify_list)
        columns, data = self.cmd.take_action(parsed_args)
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))

    @mock.patch('octaviaclient.osc.v2.utils.get_loadbalancer_attrs')
    def test_load_balancer_list_with_tags(self, mock_client):
        mock_client.return_value = {
            'tags': self._lb.tags,
        }
        arglist = [
            '--tags', ",".join(self._lb.tags),
        ]
        verify_list = [
            ('tags', self._lb.tags),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verify_list)
        columns, data = self.cmd.take_action(parsed_args)
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))

    @mock.patch('octaviaclient.osc.v2.utils.get_loadbalancer_attrs')
    def test_load_balancer_list_with_any_tags(self, mock_client):
        mock_client.return_value = {
            'tags': self._lb.tags,
        }
        arglist = [
            '--any-tags', ",".join(self._lb.tags),
        ]
        verify_list = [
            ('any_tags', self._lb.tags),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verify_list)
        columns, data = self.cmd.take_action(parsed_args)
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))

    @mock.patch('octaviaclient.osc.v2.utils.get_loadbalancer_attrs')
    def test_load_balancer_list_with_not_tags(self, mock_client):
        mock_client.return_value = {
            'tags': self._lb.tags[0],
        }
        arglist = [
            '--any-tags', ",".join(self._lb.tags),
        ]
        verify_list = [
            ('any_tags', self._lb.tags),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verify_list)
        columns, data = self.cmd.take_action(parsed_args)
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))

    @mock.patch('octaviaclient.osc.v2.utils.get_loadbalancer_attrs')
    def test_load_balancer_list_with_not_any_tags(self, mock_client):
        mock_client.return_value = {
            'tags': self._lb.tags[0],
        }
        arglist = [
            '--not-any-tags', ",".join(self._lb.tags),
        ]
        verify_list = [
            ('not_any_tags', self._lb.tags),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verify_list)
        columns, data = self.cmd.take_action(parsed_args)
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))


class TestLoadBalancerDelete(TestLoadBalancer):

    def setUp(self):
        super().setUp()
        self.cmd = load_balancer.DeleteLoadBalancer(self.app, None)

    def test_load_balancer_delete(self):
        arglist = [self._lb.id]
        verifylist = [
            ('loadbalancer', self._lb.id)
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.load_balancer_delete.assert_called_with(
            lb_id=self._lb.id)

    @mock.patch('osc_lib.utils.wait_for_delete')
    def test_load_balancer_delete_wait(self, mock_wait):
        arglist = [self._lb.id, '--wait']
        verifylist = [
            ('loadbalancer', self._lb.id),
            ('wait', True),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.load_balancer_delete.assert_called_with(
            lb_id=self._lb.id)
        mock_wait.assert_called_once_with(
            manager=mock.ANY,
            res_id=self.lb_info['id'],
            sleep_time=mock.ANY,
            status_field='provisioning_status')

    def test_load_balancer_delete_failure(self):
        arglist = ['unknown_lb']
        verifylist = [
            ('loadbalancer', 'unknown_lb')
        ]
        self.api_mock.load_balancer_list.return_value = {
            'loadbalancers': []}
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.assertRaises(exceptions.CommandError, self.cmd.take_action,
                          parsed_args)
        self.assertNotCalled(self.api_mock.load_balancer_delete)


class TestLoadBalancerCreate(TestLoadBalancer):

    def setUp(self):
        super().setUp()

        self.api_mock.load_balancer_create.return_value = {
            'loadbalancer': self.lb_info
        }
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock

        self.cmd = load_balancer.CreateLoadBalancer(self.app, None)

    @mock.patch('octaviaclient.osc.v2.utils.get_loadbalancer_attrs')
    def test_load_balancer_create(self, mock_client):
        mock_client.return_value = self.lb_info
        arglist = ['--name', self._lb.name,
                   '--vip-network-id', self._lb.vip_network_id,
                   '--project', self._lb.project_id,
                   '--flavor', self._lb.flavor_id]
        verifylist = [
            ('name', self._lb.name),
            ('vip_network_id', self._lb.vip_network_id),
            ('project', self._lb.project_id),
            ('flavor', self._lb.flavor_id),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.load_balancer_create.assert_called_with(
            json={'loadbalancer': self.lb_info})

    @mock.patch('osc_lib.utils.wait_for_status')
    @mock.patch('octaviaclient.osc.v2.utils.get_loadbalancer_attrs')
    def test_load_balancer_create_wait(self, mock_client, mock_wait):
        mock_client.return_value = self.lb_info
        self.api_mock.load_balancer_show.return_value = self.lb_info
        arglist = ['--name', self._lb.name,
                   '--vip-network-id', self._lb.vip_network_id,
                   '--project', self._lb.project_id,
                   '--flavor', self._lb.flavor_id,
                   '--wait']
        verifylist = [
            ('name', self._lb.name),
            ('vip_network_id', self._lb.vip_network_id),
            ('project', self._lb.project_id),
            ('flavor', self._lb.flavor_id),
            ('wait', True),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.load_balancer_create.assert_called_with(
            json={'loadbalancer': self.lb_info})
        mock_wait.assert_called_once_with(
            status_f=mock.ANY,
            res_id=self.lb_info['id'],
            sleep_time=mock.ANY,
            status_field='provisioning_status')

    @mock.patch('octaviaclient.osc.v2.utils.get_loadbalancer_attrs')
    def test_load_balancer_create_with_qos_policy(self, mock_client):
        qos_policy_id = 'qos_id'
        lb_info = copy.deepcopy(self.lb_info)
        lb_info.update({'vip_qos_policy_id': qos_policy_id})
        mock_client.return_value = lb_info

        arglist = [
            '--name', self._lb.name,
            '--vip-network-id', self._lb.vip_network_id,
            '--project', self._lb.project_id,
            '--vip-qos-policy-id', qos_policy_id,
        ]
        verifylist = [
            ('name', self._lb.name),
            ('vip_network_id', self._lb.vip_network_id),
            ('project', self._lb.project_id),
            ('vip_qos_policy_id', qos_policy_id),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.load_balancer_create.assert_called_with(
            json={'loadbalancer': lb_info})

    @mock.patch('octaviaclient.osc.v2.utils.get_loadbalancer_attrs')
    def test_load_balancer_create_with_provider(self, mock_client):
        provider = 'foobar'
        lb_info = copy.deepcopy(self.lb_info)
        lb_info.update({'provider': provider})
        mock_client.return_value = lb_info

        arglist = [
            '--name', self._lb.name,
            '--vip-network-id', self._lb.vip_network_id,
            '--project', self._lb.project_id,
            '--provider', provider,
        ]
        verifylist = [
            ('name', self._lb.name),
            ('vip_network_id', self._lb.vip_network_id),
            ('project', self._lb.project_id),
            ('provider', provider),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.load_balancer_create.assert_called_with(
            json={'loadbalancer': lb_info})

    @mock.patch('octaviaclient.osc.v2.utils.get_loadbalancer_attrs')
    def test_load_balancer_create_with_tags(self, mock_client):
        lb_info = copy.deepcopy(self.lb_info)
        lb_info.update({'tags': self._lb.tags})
        mock_client.return_value = lb_info

        arglist = [
            '--name', self._lb.name,
            '--vip-network-id', self._lb.vip_network_id,
            '--project', self._lb.project_id,
            '--tag', self._lb.tags[0],
            '--tag', self._lb.tags[1],
        ]
        verifylist = [
            ('name', self._lb.name),
            ('vip_network_id', self._lb.vip_network_id),
            ('project', self._lb.project_id),
            ('tags', self._lb.tags),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.load_balancer_create.assert_called_with(
            json={'loadbalancer': lb_info})

    @mock.patch('octaviaclient.osc.v2.utils.get_loadbalancer_attrs')
    def test_load_balancer_create_missing_args(self, mock_client):
        attrs_list = self.lb_info

        # init missing keys
        args = ("vip_subnet_id", "vip_network_id", "vip_port_id")
        for a in args:
            # init missing keys
            attrs_list[a] = ''
        # verify all valid combinations of args
        for n in range(len(args) + 1):
            for comb in itertools.combinations(args, n):
                # subtract comb's keys from attrs_list
                filtered_attrs = {k: v for k, v in attrs_list.items() if (
                    k not in comb)}
                # Add the 'wait' attribute, which isn't part of an LB directly
                filtered_attrs['wait'] = False
                mock_client.return_value = filtered_attrs
                if not any(k in filtered_attrs for k in args) or all(
                    k in filtered_attrs for k in ("vip_network_id",
                                                  "vip_port_id")
                ):
                    self.assertRaises(
                        exceptions.CommandError,
                        self.cmd.take_action,
                        filtered_attrs)
                else:
                    try:
                        self.cmd.take_action(munch.Munch(filtered_attrs))
                    except exceptions.CommandError as e:
                        self.fail("%s raised unexpectedly" % e)


class TestLoadBalancerShow(TestLoadBalancer):

    def setUp(self):
        super().setUp()
        self.api_mock.load_balancer_show.return_value = {
            'loadbalancer': self.lb_info}
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock

        self.cmd = load_balancer.ShowLoadBalancer(self.app, None)

    def test_load_balancer_show(self):
        arglist = [self._lb.id]
        verifylist = [
            ('loadbalancer', self._lb.id),
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.load_balancer_show.assert_called_with(lb_id=self._lb.id)


class TestLoadBalancerSet(TestLoadBalancer):

    def setUp(self):
        super().setUp()
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock
        self.cmd = load_balancer.SetLoadBalancer(self.app, None)

    @mock.patch('octaviaclient.osc.v2.utils.get_loadbalancer_attrs')
    def test_load_balancer_set(self, mock_attrs):
        qos_policy_id = uuidutils.generate_uuid()
        mock_attrs.return_value = {
            'loadbalancer_id': self._lb.id,
            'name': 'new_name',
            'vip_qos_policy_id': qos_policy_id,
        }
        arglist = [self._lb.id, '--name', 'new_name',
                   '--vip-qos-policy-id', qos_policy_id]
        verifylist = [
            ('loadbalancer', self._lb.id),
            ('name', 'new_name'),
            ('vip_qos_policy_id', qos_policy_id),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.load_balancer_set.assert_called_with(
            self._lb.id, json={
                'loadbalancer': {
                    'name': 'new_name',
                    'vip_qos_policy_id': qos_policy_id,
                }
            })

    @mock.patch('osc_lib.utils.wait_for_status')
    @mock.patch('octaviaclient.osc.v2.utils.get_loadbalancer_attrs')
    def test_load_balancer_set_wait(self, mock_attrs, mock_wait):
        qos_policy_id = uuidutils.generate_uuid()
        mock_attrs.return_value = {
            'loadbalancer_id': self._lb.id,
            'name': 'new_name',
            'vip_qos_policy_id': qos_policy_id,
        }
        arglist = [self._lb.id, '--name', 'new_name',
                   '--vip-qos-policy-id', qos_policy_id, '--wait']
        verifylist = [
            ('loadbalancer', self._lb.id),
            ('name', 'new_name'),
            ('vip_qos_policy_id', qos_policy_id),
            ('wait', True),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.load_balancer_set.assert_called_with(
            self._lb.id, json={
                'loadbalancer': {
                    'name': 'new_name',
                    'vip_qos_policy_id': qos_policy_id,
                }
            })
        mock_wait.assert_called_once_with(
            status_f=mock.ANY,
            res_id=self.lb_info['id'],
            sleep_time=mock.ANY,
            status_field='provisioning_status')

    @mock.patch('octaviaclient.osc.v2.utils.get_loadbalancer_attrs')
    def test_load_balancer_set_tag(self, mock_attrs):
        self.api_mock.load_balancer_show.return_value = {
            'tags': ['foo']
        }

        mock_attrs.return_value = {
            'loadbalancer_id': self._lb.id,
            'tags': ['bar']
        }
        arglist = [self._lb.id, '--tag', 'bar']
        verifylist = [
            ('loadbalancer', self._lb.id),
            ('tags', ['bar'])
        ]

        try:
            parsed_args = self.check_parser(self.cmd, arglist, verifylist)
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.fail("%s raised unexpectedly" % e)

        self.api_mock.load_balancer_set.assert_called_once()
        kwargs = self.api_mock.load_balancer_set.mock_calls[0][2]
        tags = kwargs['json']['loadbalancer']['tags']
        self.assertEqual(2, len(tags))
        self.assertIn('foo', tags)
        self.assertIn('bar', tags)

    @mock.patch('octaviaclient.osc.v2.utils.get_loadbalancer_attrs')
    def test_load_balancer_set_tag_no_tag(self, mock_attrs):
        self.api_mock.load_balancer_show.return_value = {
            'tags': ['foo']
        }

        mock_attrs.return_value = {
            'loadbalancer_id': self._lb.id,
            'tags': ['bar']
        }
        arglist = [self._lb.id, '--tag', 'bar', '--no-tag']
        verifylist = [
            ('loadbalancer', self._lb.id),
            ('tags', ['bar'])
        ]

        try:
            parsed_args = self.check_parser(self.cmd, arglist, verifylist)
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.fail("%s raised unexpectedly" % e)

        self.api_mock.load_balancer_set.assert_called_once_with(
            self._lb.id,
            json={'loadbalancer': {'tags': ['bar']}})

    @mock.patch('octaviaclient.osc.v2.utils.get_loadbalancer_attrs')
    def test_load_balancer_remove_qos_policy(self, mock_attrs):
        mock_attrs.return_value = {
            'loadbalancer_id': self._lb.id,
            'vip_qos_policy_id': None,
        }
        arglist = [self._lb.id, '--vip-qos-policy-id', 'None']
        verifylist = [
            ('loadbalancer', self._lb.id),
            ('vip_qos_policy_id', 'None'),
        ]

        try:
            parsed_args = self.check_parser(self.cmd, arglist, verifylist)
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.fail("%s raised unexpectedly" % e)


class TestLoadBalancerStats(TestLoadBalancer):

    def setUp(self):
        super().setUp()
        lb_stats_info = {'stats': {'bytes_in': '0'}}
        self.api_mock.load_balancer_stats_show.return_value = {
            'stats': lb_stats_info['stats']}
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock
        self.cmd = load_balancer.ShowLoadBalancerStats(self.app, None)

    def test_load_balancer_stats_show(self):
        arglist = [self._lb.id]
        verifylist = [
            ('loadbalancer', self._lb.id),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.load_balancer_stats_show.assert_called_with(
            lb_id=self._lb.id)


class TestLoadBalancerStatus(TestLoadBalancer):
    def setUp(self):
        super().setUp()
        expected_res = {'statuses': {'operating_status': 'ONLINE',
                                     'provisioning_status': 'ACTIVE'}}
        self.api_mock.load_balancer_status_show.return_value = {
            'statuses': expected_res['statuses']
        }
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock
        self.cmd = load_balancer.ShowLoadBalancerStatus(self.app, None)

    def test_load_balancer_status_show(self):
        # lbaas-loadbalancer-status test_id.
        arglist = [self._lb.id]
        verifylist = [
            ('loadbalancer', self._lb.id),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.load_balancer_status_show.assert_called_with(
            lb_id=self._lb.id)


class TestLoadBalancerFailover(TestLoadBalancer):

    def setUp(self):
        super().setUp()
        self.cmd = load_balancer.FailoverLoadBalancer(self.app, None)

    def test_load_balancer_failover(self):
        arglist = [self._lb.id]
        verifylist = [
            ('loadbalancer', self._lb.id)
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.load_balancer_failover.assert_called_with(
            lb_id=self._lb.id)

    @mock.patch('osc_lib.utils.wait_for_status')
    def test_load_balancer_failover_wait(self, mock_wait):
        arglist = [self._lb.id, '--wait']
        verifylist = [
            ('loadbalancer', self._lb.id),
            ('wait', True),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.load_balancer_failover.assert_called_with(
            lb_id=self._lb.id)
        mock_wait.assert_called_once_with(
            status_f=mock.ANY,
            res_id=self._lb.id,
            sleep_time=mock.ANY,
            status_field='provisioning_status')


class TestLoadBalancerUnset(TestLoadBalancer):
    PARAMETERS = ('name', 'description', 'vip_qos_policy_id')

    def setUp(self):
        super().setUp()
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock
        self.cmd = load_balancer.UnsetLoadBalancer(self.app, None)

    def test_load_balancer_unset_name(self):
        self._test_load_balancer_unset_param('name')

    def test_load_balancer_unset_name_wait(self):
        self._test_load_balancer_unset_param_wait('name')

    def test_load_balancer_unset_description(self):
        self._test_load_balancer_unset_param('description')

    def test_load_balancer_unset_qos(self):
        self._test_load_balancer_unset_param('vip_qos_policy_id')

    def _test_load_balancer_unset_param(self, param):
        self.api_mock.load_balancer_set.reset_mock()
        ref_body = {'loadbalancer': {param: None}}
        arg_param = param.replace('_', '-') if '_' in param else param
        arglist = [self._lb.id, '--%s' % arg_param]
        verifylist = [
            ('loadbalancer', self._lb.id),
        ]
        for ref_param in self.PARAMETERS:
            verifylist.append((ref_param, param == ref_param))
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.load_balancer_set.assert_called_once_with(
            self._lb.id, json=ref_body)

    @mock.patch('osc_lib.utils.wait_for_status')
    def _test_load_balancer_unset_param_wait(self, param, mock_wait):
        self.api_mock.load_balancer_set.reset_mock()
        ref_body = {'loadbalancer': {param: None}}
        arg_param = param.replace('_', '-') if '_' in param else param
        arglist = [self._lb.id, '--%s' % arg_param, '--wait']
        verifylist = [
            ('loadbalancer', self._lb.id),
            ('wait', True),
        ]
        for ref_param in self.PARAMETERS:
            verifylist.append((ref_param, param == ref_param))
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.load_balancer_set.assert_called_once_with(
            self._lb.id, json=ref_body)
        mock_wait.assert_called_once_with(
            status_f=mock.ANY,
            res_id=self.lb_info['id'],
            sleep_time=mock.ANY,
            status_field='provisioning_status')

    def test_load_balancer_unset_all(self):
        self.api_mock.load_balancer_set.reset_mock()
        ref_body = {'loadbalancer': {x: None for x in self.PARAMETERS}}
        arglist = [self._lb.id]
        for ref_param in self.PARAMETERS:
            arg_param = (ref_param.replace('_', '-') if '_' in ref_param else
                         ref_param)
            arglist.append('--%s' % arg_param)
        verifylist = list(zip(self.PARAMETERS, [True] * len(self.PARAMETERS)))
        verifylist = [('loadbalancer', self._lb.id)] + verifylist
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.load_balancer_set.assert_called_once_with(
            self._lb.id, json=ref_body)

    def test_load_balancer_unset_none(self):
        self.api_mock.load_balancer_set.reset_mock()
        arglist = [self._lb.id]
        verifylist = list(zip(self.PARAMETERS, [False] * len(self.PARAMETERS)))
        verifylist = [('loadbalancer', self._lb.id)] + verifylist
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.load_balancer_set.assert_not_called()

    def test_load_balancer_unset_tag(self):
        self.api_mock.load_balancer_show.return_value = {
            'tags': ['foo', 'bar']
        }

        arglist = [self._lb.id, '--tag', 'foo']
        verifylist = [
            ('loadbalancer', self._lb.id),
            ('tags', ['foo'])
        ]

        try:
            parsed_args = self.check_parser(self.cmd, arglist, verifylist)
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.fail("%s raised unexpectedly" % e)

        self.api_mock.load_balancer_set.assert_called_once_with(
            self._lb.id,
            json={'loadbalancer': {'tags': ['bar']}})

    def test_load_balancer_unset_all_tag(self):
        self.api_mock.load_balancer_show.return_value = {
            'tags': ['foo', 'bar']
        }

        arglist = [self._lb.id, '--all-tag']
        verifylist = [
            ('loadbalancer', self._lb.id),
            ('all_tag', True)
        ]

        try:
            parsed_args = self.check_parser(self.cmd, arglist, verifylist)
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.fail("%s raised unexpectedly" % e)

        self.api_mock.load_balancer_set.assert_called_once_with(
            self._lb.id,
            json={'loadbalancer': {'tags': []}})
