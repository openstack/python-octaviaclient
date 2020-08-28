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

from osc_lib import exceptions
from osc_lib.tests import utils

from octaviaclient.osc.v2 import constants
from octaviaclient.osc.v2 import validate


class TestValidations(utils.TestCommand):
    def setUp(self):
        super().setUp()

    def test_check_l7policy_attrs(self):
        attrs_dict = {
            "action": "redirect_to_pool".upper(),
            "redirect_pool_id": "id"}
        try:
            validate.check_l7policy_attrs(attrs_dict)
        except exceptions.CommandError as e:
            self.fail("%s raised unexpectedly" % e)
        attrs_dict.pop("redirect_pool_id")
        self.assertRaises(
            exceptions.CommandError,
            validate.check_l7policy_attrs, attrs_dict)

        attrs_dict = {
            "action": "redirect_to_url".upper(),
            "redirect_url": "url"}
        try:
            validate.check_l7policy_attrs(attrs_dict)
        except exceptions.CommandError as e:
            self.fail("%s raised unexpectedly" % e)
        attrs_dict.pop("redirect_url")
        self.assertRaises(
            exceptions.CommandError,
            validate.check_l7policy_attrs, attrs_dict)

        attrs_dict = {
            "action": "redirect_prefix".upper(),
            "redirect_prefix": "prefix",
        }
        try:
            validate.check_l7policy_attrs(attrs_dict)
        except exceptions.CommandError as e:
            self.fail("%s raised unexpectedly" % e)
        attrs_dict.pop("redirect_prefix")
        self.assertRaises(
            exceptions.CommandError,
            validate.check_l7policy_attrs, attrs_dict)

    def test_check_l7rule_attrs(self):
        for i in ("cookie", "header"):
            attrs_dict = {
                "type": i.upper(),
                "key": "key",
            }
            try:
                validate.check_l7rule_attrs(attrs_dict)
            except exceptions.CommandError as e:
                self.fail("%s raised unexpectedly" % e)
            attrs_dict.pop("key")
            self.assertRaises(
                exceptions.CommandError,
                validate.check_l7rule_attrs, attrs_dict)

    def test_validate_TCP_UDP_SCTP_port_range(self):
        # Positive tests, should not raise
        validate._validate_TCP_UDP_SCTP_port_range(constants.MIN_PORT_NUMBER,
                                                   "fake-parameter")
        validate._validate_TCP_UDP_SCTP_port_range(constants.MAX_PORT_NUMBER,
                                                   "fake-parameter")

        # Negative tests, should raise
        self.assertRaises(exceptions.InvalidValue,
                          validate._validate_TCP_UDP_SCTP_port_range,
                          constants.MIN_PORT_NUMBER - 1, "fake-parameter")
        self.assertRaises(exceptions.InvalidValue,
                          validate._validate_TCP_UDP_SCTP_port_range,
                          constants.MAX_PORT_NUMBER + 1, "fake-parameter")

    def test_check_listener_attrs(self):
        # Positive tests, should not raise
        attrs_dict = {'protocol_port': constants.MIN_PORT_NUMBER}
        validate.check_listener_attrs(attrs_dict)
        attrs_dict = {'protocol_port': constants.MAX_PORT_NUMBER}
        validate.check_listener_attrs(attrs_dict)

        # Negative tests, should raise
        attrs_dict = {'protocol_port': constants.MIN_PORT_NUMBER - 1}
        self.assertRaises(exceptions.InvalidValue,
                          validate.check_listener_attrs, attrs_dict)
        attrs_dict = {'protocol_port': constants.MAX_PORT_NUMBER + 1}
        self.assertRaises(exceptions.InvalidValue,
                          validate.check_listener_attrs, attrs_dict)

    def test_check_member_attrs(self):
        # Positive tests, should not raise
        attrs_dict = {'protocol_port': constants.MIN_PORT_NUMBER,
                      'member_port': constants.MIN_PORT_NUMBER,
                      'weight': constants.MIN_WEIGHT}
        validate.check_member_attrs(attrs_dict)
        attrs_dict = {'protocol_port': constants.MAX_PORT_NUMBER,
                      'member_port': constants.MAX_PORT_NUMBER,
                      'weight': constants.MAX_WEIGHT}
        validate.check_member_attrs(attrs_dict)

        # Negative tests, should raise - protocol-port
        attrs_dict = {'protocol_port': constants.MIN_PORT_NUMBER - 1,
                      'member_port': constants.MIN_PORT_NUMBER,
                      'weight': constants.MIN_WEIGHT}
        self.assertRaises(exceptions.InvalidValue, validate.check_member_attrs,
                          attrs_dict)
        attrs_dict = {'protocol_port': constants.MAX_PORT_NUMBER + 1,
                      'member_port': constants.MIN_PORT_NUMBER,
                      'weight': constants.MIN_WEIGHT}
        self.assertRaises(exceptions.InvalidValue, validate.check_member_attrs,
                          attrs_dict)

        # Negative tests, should raise - member-port
        attrs_dict = {'protocol_port': constants.MIN_PORT_NUMBER,
                      'member_port': constants.MIN_PORT_NUMBER - 1,
                      'weight': constants.MIN_WEIGHT}
        self.assertRaises(exceptions.InvalidValue, validate.check_member_attrs,
                          attrs_dict)
        attrs_dict = {'protocol_port': constants.MIN_PORT_NUMBER,
                      'member_port': constants.MAX_PORT_NUMBER + 1,
                      'weight': constants.MIN_WEIGHT}
        self.assertRaises(exceptions.InvalidValue, validate.check_member_attrs,
                          attrs_dict)

        # Negative tests, should raise - weight
        attrs_dict = {'protocol_port': constants.MIN_PORT_NUMBER,
                      'member_port': constants.MIN_PORT_NUMBER,
                      'weight': constants.MIN_WEIGHT - 1}
        self.assertRaises(exceptions.InvalidValue, validate.check_member_attrs,
                          attrs_dict)
        attrs_dict = {'protocol_port': constants.MIN_PORT_NUMBER,
                      'member_port': constants.MIN_PORT_NUMBER,
                      'weight': constants.MAX_WEIGHT + 1}
        self.assertRaises(exceptions.InvalidValue, validate.check_member_attrs,
                          attrs_dict)
