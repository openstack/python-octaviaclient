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

"""Load Balancer v2 API Library"""

from osc_lib.api import api

from octaviaclient.api import constants as const


class APIv2(api.BaseAPI):
    """Load Balancer v2 API"""

    _endpoint_suffix = '/v2.0/lbaas'

    def __init__(self, endpoint=None, **kwargs):
        super(APIv2, self).__init__(endpoint=endpoint, **kwargs)
        self.endpoint = self.endpoint.rstrip('/')
        self._build_url()

    def _build_url(self):
        if not self.endpoint.endswith(self._endpoint_suffix):
            self.endpoint = self.endpoint + self._endpoint_suffix

    def load_balancer_list(self, **params):
        """List all load balancers

        :param params:
            Parameters to filter on (not implemented)
        :return:
            List of load balancers
        """
        url = const.BASE_LOADBALANCER_URL
        load_balancer_list = self.list(url, **params)

        return load_balancer_list

    def load_balancer_show(self, lb_id):
        """Show a load balancer

        :param string lb_id:
            ID of the load balancer to show
        :return:
            A dict of the specified load balancer's settings
        """
        load_balancer = self.find(path=const.BASE_LOADBALANCER_URL,
                                  value=lb_id)

        return load_balancer

    def load_balancer_create(self, **params):
        """Create a load balancer

        :param params:
            Paramaters to create the load balancer with (expects json=)
        :return:
            A dict of the created load balancer's settings
        """
        url = const.BASE_LOADBALANCER_URL
        load_balancer = self.create(url, **params)

        return load_balancer

    def load_balancer_delete(self, lb_id, **params):
        """Delete a load balancer

        :param string lb_id:
            The ID of the load balancer to delete
        :param params:
            A dict of url parameters
        :return:
            Response Code from the API
        """
        url = const.BASE_SINGLE_LB_URL.format(uuid=lb_id)
        response = self.delete(url, params=params)

        return response

    def load_balancer_set(self, lb_id, **params):
        """Update a load balancer's settings

        :param string lb_id:
            The ID of the load baalancer to update
        :param params:
            A dict of arguments to update a loadbalancer
        :return:
            Response Code from API
        """
        url = const.BASE_SINGLE_LB_URL.format(uuid=lb_id)
        response = self.create(url, method='PUT', **params)

        return response

    def listener_list(self, **kwargs):
        """List all listeners

        :param kwargs:
            Parameters to filter on (not implemented)
        :return:
            List of listeners
        """
        url = const.BASE_LISTENER_URL
        listener_list = self.list(url, **kwargs)

        return listener_list

    def listener_show(self, listener_id):
        """Show a listener

        :param string listener_id:
        :return:
            A dict of the specified listener's settings
        """
        listener = self.find(path=const.BASE_LISTENER_URL, value=listener_id)

        return listener

    def listener_create(self, **kwargs):
        """Create a listener

        :param kwargs:
            Parameters to create a listener with (expects json=)
        :return:
            A dict of the created listener's settings
        """
        url = const.BASE_LISTENER_URL
        listener = self.create(url, **kwargs)

        return listener

    def listener_delete(self, listener_id):
        """Delete a listener

        :param stirng listener_id:
            ID of of listener to delete
        :return:
            Response Code from the API
        """
        url = const.BASE_SINGLE_LISTENER_URL.format(uuid=listener_id)
        response = self.delete(url)

        return response

    def listener_set(self, listener_id, **kwargs):
        """Update a listener's settings

        :param string listener_id:
            ID of the listener to update
        :param kwargs:
            A dict of arguments to update a listener
        :return:
            A dict of the updated listener's settings
        """
        url = const.BASE_SINGLE_LISTENER_URL.format(uuid=listener_id)
        response = self.create(url, method='PUT', **kwargs)

        return response
