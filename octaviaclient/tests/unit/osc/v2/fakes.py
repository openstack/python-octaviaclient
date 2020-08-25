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
from unittest import mock

from osc_lib.tests import utils

from octaviaclient.tests import fakes
from octaviaclient.tests.unit.osc.v2 import constants


class FakeOctaviaClient(object):
    def __init__(self, **kwargs):
        self.load_balancers = mock.Mock()
        self.load_balancers.resource_class = fakes.FakeResource(None, {})
        self.auth_token = kwargs['token']
        self.management_url = kwargs['endpoint']


class TestOctaviaClient(utils.TestCommand):

    def setUp(self):
        super().setUp()
        self.app.client_manager.load_balancer = FakeOctaviaClient(
            endpoint=fakes.AUTH_URL,
            token=fakes.AUTH_TOKEN,
        )


def createFakeResource(name, attrs=None):
    """Creates a single fake resource object.

    :param name: resource_name
    :param attrs: ``dict`` of customized resource attributes
    :returns: A FakeResource object
    """
    attrs = attrs or {}

    # Set to default
    resource_info = getattr(constants, "{}_attrs".format(name).upper())
    assert resource_info is not None, "{} is not found".format(name)

    resource_info.update(attrs)
    return fakes.FakeResource(
        info=copy.deepcopy(resource_info), loaded=True,
    )
