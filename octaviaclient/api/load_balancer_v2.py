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
            Response Code from the API
        """
        url = const.BASE_SINGLE_LISTENER_URL.format(uuid=listener_id)
        response = self.create(url, method='PUT', **kwargs)

        return response

    def pool_list(self, **kwargs):
        """List all pools

        :param kwargs:
            Parameters to filter on (not implemented)
        :return:
            List of pools
        """
        url = const.BASE_POOL_URL
        pool_list = self.list(url, **kwargs)

        return pool_list

    def pool_create(self, **kwargs):
        """Create a pool

        :param kwargs:
            Parameters to create a listener with (expects json=)
        :return:
            A dict of the created pool's settings
        """
        url = const.BASE_POOL_URL
        pool = self.create(url, **kwargs)

        return pool

    def pool_delete(self, pool_id):
        """Delete a pool

        :param string pool_id:
            ID of of pool to delete
        :return:
            Response Code from the API
        """
        url = const.BASE_SINGLE_POOL_URL.format(pool_id=pool_id)
        deleted_pool = self.delete(url)

        return deleted_pool

    def pool_show(self, pool_id):
        """Show a pool's settings

        :param string pool_id:
            ID of the pool to show
        :return:
            Dict of the specified pool's settings
        """
        pool = self.find(path=const.BASE_POOL_URL, value=pool_id)

        return pool

    def pool_set(self, pool_id, **kwargs):
        """Update a pool's settings

        :param pool_id:
            ID of the pool to update
        :param kwargs:
            A dict of arguments to update a pool
        :return:
            Response Code from the API
        """
        url = const.BASE_SINGLE_POOL_URL.format(pool_id=pool_id)
        pool = self.create(url, method='PUT', **kwargs)

        return pool

    def member_list(self, pool_id, **kwargs):
        """Lists the member from a given pool id

        :param pool_id:
            ID of the pool
        :param kwargs:
            A dict of filter arguments
        :return:
            Response list members
        """
        url = const.BASE_MEMBER_URL.format(pool_id=pool_id)
        members_list = self.list(url, **kwargs)

        return members_list

    def member_show(self, pool_id, member_id):
        """Showing a member details of a pool

        :param pool_id:
            ID of pool the member is added
        :param member_id:
            ID of the member
        :param kwargs:
            A dict of arguments
        :return:
            Response of member
        """
        url = const.BASE_MEMBER_URL.format(pool_id=pool_id)
        member = self.find(path=url, value=member_id)

        return member

    def member_create(self, pool_id, **kwargs):
        """Creating a member for the given pool id

        :param pool_id:
            ID of pool to which member is added
        :param kwargs:
            A Dict of arguments
        :return:
            A member details on successful creation
        """
        url = const.BASE_MEMBER_URL.format(pool_id=pool_id)
        member = self.create(url, **kwargs)

        return member

    def member_delete(self, pool_id, member_id):
        """Removing a member from a pool and mark that member as deleted

        :param pool_id:
            ID of the pool
        :param member_id:
            ID of the member to be deleted
        :return:
            Response code from the API
        """
        url = const.BASE_SINGLE_MEMBER_URL.format(pool_id=pool_id,
                                                  member_id=member_id)
        response = self.delete(url)

        return response

    def member_set(self, pool_id, member_id, **kwargs):
        """Updating a member settings

        :param pool_id:
            ID of the pool
        :param member_id:
            ID of the member to be updated
        :param kwargs:
            A dict of the values of member to be updated
        :return:
            Response code from the API
        """
        url = const.BASE_SINGLE_MEMBER_URL.format(pool_id=pool_id,
                                                  member_id=member_id)

        response = self.create(url, method='PUT', **kwargs)

        return response

    def l7policy_list(self, **kwargs):
        """List all l7policies

        :param kwargs:
            Parameters to filter on (not implemented)
        :return:
            List of l7policies
        """
        url = const.BASE_L7POLICY_URL
        policy_list = self.list(url, **kwargs)

        return policy_list

    def l7policy_create(self, **kwargs):
        """Create a l7policy

        :param kwargs:
            Parameters to create a l7policy with (expects json=)
        :return:
            A dict of the created l7policy's settings
        """
        url = const.BASE_L7POLICY_URL
        policy = self.create(url, **kwargs)

        return policy

    def l7policy_delete(self, l7policy_id):
        """Delete a l7policy

        :param string l7policy_id:
            ID of of l7policy to delete
        :return:
            Response Code from the API
        """
        url = const.BASE_SINGLE_L7POLICY_URL.format(policy_uuid=l7policy_id)
        response = self.delete(url)

        return response

    def l7policy_show(self, l7policy_id):
        """Show a l7policy's settings

        :param string l7policy_id:
            ID of the l7policy to show
        :return:
            Dict of the specified l7policy's settings
        """
        l7policy = self.find(path=const.BASE_L7POLICY_URL, value=l7policy_id)

        return l7policy

    def l7policy_set(self, l7policy_id, **kwargs):
        """Update a l7policy's settings

        :param l7policy_id:
            ID of the l7policy to update
        :param kwargs:
            A dict of arguments to update a l7policy
        :return:
            Response Code from the API
        """
        url = const.BASE_SINGLE_L7POLICY_URL.format(policy_uuid=l7policy_id)

        response = self.create(url, method='PUT', **kwargs)

        return response

    def l7rule_list(self, l7policy_id, **kwargs):
        """List all l7rules for a l7policy

        :param kwargs:
            Parameters to filter on (not implemented)
        :return:
            List of l7policies
        """
        url = const.BASE_L7RULE_URL.format(policy_uuid=l7policy_id)
        rule_list = self.list(url, **kwargs)

        return rule_list

    def l7rule_create(self, l7policy_id, **kwargs):
        """Create a l7rule

        :param string l7policy_id:
            The l7policy to create the l7rule for
        :param kwargs:
            Parameters to create a l7rule with (expects json=)
        :return:
            A dict of the created l7rule's settings
        """
        url = const.BASE_L7RULE_URL.format(policy_uuid=l7policy_id)
        rule = self.create(url, **kwargs)

        return rule

    def l7rule_delete(self, l7rule_id, l7policy_id):
        """Delete a l7rule

        :param string l7rule_id:
            ID of of listener to delete
        :param string l7policy_id:
            ID of the l7policy for this l7rule
        :return:
            Response Code from the API
        """
        url = const.BASE_SINGLE_L7RULE_URL.format(rule_uuid=l7rule_id,
                                                  policy_uuid=l7policy_id)
        response = self.delete(url)

        return response

    def l7rule_show(self, l7rule_id, l7policy_id):
        """Show a l7rule's settings

        :param string l7rule_id:
            ID of the l7rule to show
        :param string l7policy_id:
            ID of the l7policy for this l7rule
        :return:
            Dict of the specified l7rule's settings
        """
        url = const.BASE_L7RULE_URL.format(policy_uuid=l7policy_id)

        rule = self.find(path=url, value=l7rule_id)

        return rule

    def l7rule_set(self, l7rule_id, l7policy_id, **kwargs):
        """Update a l7rule's settings

        :param l7rule_id:
            ID of the l7rule to update
        :param string l7policy_id:
            ID of the l7policy for this l7rule
        :param kwargs:
            A dict of arguments to update a l7rule
        :return:
            Response Code from the API
        """
        url = const.BASE_SINGLE_L7RULE_URL.format(rule_uuid=l7rule_id,
                                                  policy_uuid=l7policy_id)
        response = self.create(url, method='PUT', **kwargs)

        return response

    def health_monitor_list(self, **kwargs):
        """List all health monitors

        :param kwargs:
            Parameters to filter on (not implemented)
        :return:
            A dict containing a list of health monitors
        """
        url = const.BASE_HEALTH_MONITOR_URL
        policy_list = self.list(url, **kwargs)

        return policy_list

    def health_monitor_create(self, **kwargs):
        """Create a health monitor

        :param kwargs:
            Parameters to create a health monitor with (expects json=)
        :return:
            A dict of the created health monitor's settings
        """
        url = const.BASE_HEALTH_MONITOR_URL
        health_monitor = self.create(url, **kwargs)

        return health_monitor

    def health_monitor_delete(self, health_monitor_id):
        """Delete a health_monitor

        :param string health_monitor_id:
            ID of of health monitor to delete
        :return:
            Response Code from the API
        """
        url = const.BASE_SINGLE_HEALTH_MONITOR_URL.format(
            uuid=health_monitor_id)
        response = self.delete(url)

        return response

    def health_monitor_show(self, health_monitor_id):
        """Show a health monitor's settings

        :param string health_monitor_id:
            ID of the health monitor to show
        :return:
            Dict of the specified health monitor's settings
        """
        url = const.BASE_HEALTH_MONITOR_URL
        health_monitor = self.find(path=url, value=health_monitor_id)

        return health_monitor

    def health_monitor_set(self, health_monitor_id, **kwargs):
        """Update a health monitor's settings

        :param health_monitor_id:
            ID of the health monitor to update
        :param kwargs:
            A dict of arguments to update a l7policy
        :return:
            Response Code from the API
        """
        url = const.BASE_SINGLE_HEALTH_MONITOR_URL.format(
            uuid=health_monitor_id)

        response = self.create(url, method='PUT', **kwargs)

        return response
