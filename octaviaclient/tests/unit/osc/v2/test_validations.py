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

from octaviaclient.osc.v2 import validate


class TestValidations(utils.TestCommand):
    def setUp(self):
        super(TestValidations, self).setUp()

    def test_check_l7policy_attrs(self):
        attrs_dict = {
            "action": "redirect_to_pool".upper(),
            "redirect_pool_id": "id",
            }
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
            "redirect_url": "url",
            }
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
