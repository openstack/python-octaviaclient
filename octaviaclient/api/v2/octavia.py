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

"""Octavia API Library"""
import functools

from osc_lib.api import api
from osc_lib import exceptions as osc_exc

from octaviaclient.api import constants as const


def correct_return_codes(func):
    _status_dict = {400: 'Bad Request', 401: 'Unauthorized',
                    403: 'Forbidden', 404: 'Not found',
                    409: 'Conflict', 413: 'Over Limit',
                    501: 'Not Implemented'}

    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
        except Exception as e:
            if hasattr(e, 'response'):
                code = e.response.status_code
                message = e.response.json().get(
                    'faultstring',
                    _status_dict.get(e.response.status_code, 'Unknown Error'))
                request_id = e.request_id
            elif (isinstance(e, osc_exc.ClientException)
                    and e.code != e.http_status):
                # cover https://review.opendev.org/675328 case
                code = e.http_status
                message = e.code
                request_id = "n/a"
            else:
                raise

            raise OctaviaClientException(
                code=code,
                message=message,
                request_id=request_id)
        return response
    return wrapper


class OctaviaAPI(api.BaseAPI):
    """Octavia API"""

    _endpoint_suffix = '/v2.0'

    def __init__(self, endpoint=None, **kwargs):
        super(OctaviaAPI, self).__init__(endpoint=endpoint, **kwargs)
        self.endpoint = self.endpoint.rstrip('/')
        self._build_url()

        # Make sure we are always requesting JSON responses
        JSON_HEADER = {'Accept': 'application/json'}
        self._create = functools.partial(self.create, headers=JSON_HEADER)
        self._delete = functools.partial(self.delete, headers=JSON_HEADER)
        self._find = functools.partial(self.find, headers=JSON_HEADER)
        self._list = functools.partial(self.list, headers=JSON_HEADER)

    def _build_url(self):
        if not self.endpoint.endswith(self._endpoint_suffix):
            self.endpoint += self._endpoint_suffix

    def load_balancer_list(self, **params):
        """List all load balancers

        :param params:
            Parameters to filter on
        :return:
            List of load balancers
        """
        url = const.BASE_LOADBALANCER_URL
        response = self._list(url, **params)

        return response

    @correct_return_codes
    def load_balancer_show(self, lb_id):
        """Show a load balancer

        :param string lb_id:
            ID of the load balancer to show
        :return:
            A dict of the specified load balancer's settings
        """
        response = self._find(path=const.BASE_LOADBALANCER_URL, value=lb_id)

        return response

    @correct_return_codes
    def load_balancer_create(self, **params):
        """Create a load balancer

        :param params:
            Paramaters to create the load balancer with (expects json=)
        :return:
            A dict of the created load balancer's settings
        """
        url = const.BASE_LOADBALANCER_URL
        response = self._create(url, **params)

        return response

    @correct_return_codes
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
        response = self._delete(url, params=params)

        return response

    @correct_return_codes
    def load_balancer_set(self, lb_id, **params):
        """Update a load balancer's settings

        :param string lb_id:
            The ID of the load balancer to update
        :param params:
            A dict of arguments to update a loadbalancer
        :return:
            Response Code from API
        """
        url = const.BASE_SINGLE_LB_URL.format(uuid=lb_id)
        response = self._create(url, method='PUT', **params)

        return response

    def load_balancer_stats_show(self, lb_id, **kwargs):
        """Shows the current statistics for a load balancer.

        :param string lb_id:
            ID of the load balancer
        :return:
            A dict of the specified load balancer's statistics
        """
        url = const.BASE_LB_STATS_URL.format(uuid=lb_id)
        response = self._list(url, **kwargs)

        return response

    def load_balancer_status_show(self, lb_id, **kwargs):
        """Display load balancer status tree in json format.

        :param string lb_id:
            ID of the load balancer
        :return:
            A dict of the specified load balancer's status
        """
        url = const.BASE_LOADBALANCER_STATUS_URL.format(uuid=lb_id)
        response = self._list(url, **kwargs)

        return response

    @correct_return_codes
    def load_balancer_failover(self, lb_id):
        """Trigger load balancer failover

        :param string lb_id:
            ID of the load balancer to failover
        :return:
            Response Code from the API
        """
        url = const.BASE_LOADBALANCER_FAILOVER_URL.format(uuid=lb_id)
        response = self._create(url, method='PUT')

        return response

    def listener_list(self, **kwargs):
        """List all listeners

        :param kwargs:
            Parameters to filter on
        :return:
            List of listeners
        """
        url = const.BASE_LISTENER_URL
        response = self._list(url, **kwargs)

        return response

    @correct_return_codes
    def listener_show(self, listener_id):
        """Show a listener

        :param string listener_id:
            ID of the listener to show
        :return:
            A dict of the specified listener's settings
        """
        response = self._find(path=const.BASE_LISTENER_URL, value=listener_id)

        return response

    @correct_return_codes
    def listener_create(self, **kwargs):
        """Create a listener

        :param kwargs:
            Parameters to create a listener with (expects json=)
        :return:
            A dict of the created listener's settings
        """
        url = const.BASE_LISTENER_URL
        response = self._create(url, **kwargs)

        return response

    @correct_return_codes
    def listener_delete(self, listener_id):
        """Delete a listener

        :param stirng listener_id:
            ID of of listener to delete
        :return:
            Response Code from the API
        """
        url = const.BASE_SINGLE_LISTENER_URL.format(uuid=listener_id)
        response = self._delete(url)

        return response

    @correct_return_codes
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
        response = self._create(url, method='PUT', **kwargs)

        return response

    def listener_stats_show(self, listener_id, **kwargs):
        """Shows the current statistics for a listener

        :param string listener_id:
            ID of the listener
        :return:
            A dict of the specified listener's statistics
        """
        url = const.BASE_LISTENER_STATS_URL.format(uuid=listener_id)
        response = self._list(url, **kwargs)

        return response

    def pool_list(self, **kwargs):
        """List all pools

        :param kwargs:
            Parameters to filter on
        :return:
            List of pools
        """
        url = const.BASE_POOL_URL
        response = self._list(url, **kwargs)

        return response

    @correct_return_codes
    def pool_create(self, **kwargs):
        """Create a pool

        :param kwargs:
            Parameters to create a pool with (expects json=)
        :return:
            A dict of the created pool's settings
        """
        url = const.BASE_POOL_URL
        response = self._create(url, **kwargs)

        return response

    @correct_return_codes
    def pool_delete(self, pool_id):
        """Delete a pool

        :param string pool_id:
            ID of of pool to delete
        :return:
            Response Code from the API
        """
        url = const.BASE_SINGLE_POOL_URL.format(pool_id=pool_id)
        response = self._delete(url)

        return response

    @correct_return_codes
    def pool_show(self, pool_id):
        """Show a pool's settings

        :param string pool_id:
            ID of the pool to show
        :return:
            Dict of the specified pool's settings
        """
        response = self._find(path=const.BASE_POOL_URL, value=pool_id)

        return response

    @correct_return_codes
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
        response = self._create(url, method='PUT', **kwargs)

        return response

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
        response = self._list(url, **kwargs)

        return response

    @correct_return_codes
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
        response = self._find(path=url, value=member_id)

        return response

    @correct_return_codes
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
        response = self._create(url, **kwargs)

        return response

    @correct_return_codes
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
        response = self._delete(url)

        return response

    @correct_return_codes
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
        response = self._create(url, method='PUT', **kwargs)

        return response

    def l7policy_list(self, **kwargs):
        """List all l7policies

        :param kwargs:
            Parameters to filter on
        :return:
            List of l7policies
        """
        url = const.BASE_L7POLICY_URL
        response = self._list(url, **kwargs)

        return response

    @correct_return_codes
    def l7policy_create(self, **kwargs):
        """Create a l7policy

        :param kwargs:
            Parameters to create a l7policy with (expects json=)
        :return:
            A dict of the created l7policy's settings
        """
        url = const.BASE_L7POLICY_URL
        response = self._create(url, **kwargs)

        return response

    @correct_return_codes
    def l7policy_delete(self, l7policy_id):
        """Delete a l7policy

        :param string l7policy_id:
            ID of of l7policy to delete
        :return:
            Response Code from the API
        """
        url = const.BASE_SINGLE_L7POLICY_URL.format(policy_uuid=l7policy_id)
        response = self._delete(url)

        return response

    @correct_return_codes
    def l7policy_show(self, l7policy_id):
        """Show a l7policy's settings

        :param string l7policy_id:
            ID of the l7policy to show
        :return:
            Dict of the specified l7policy's settings
        """
        response = self._find(path=const.BASE_L7POLICY_URL, value=l7policy_id)

        return response

    @correct_return_codes
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
        response = self._create(url, method='PUT', **kwargs)

        return response

    def l7rule_list(self, l7policy_id, **kwargs):
        """List all l7rules for a l7policy

        :param kwargs:
            Parameters to filter on
        :return:
            List of l7rules
        """
        url = const.BASE_L7RULE_URL.format(policy_uuid=l7policy_id)
        response = self._list(url, **kwargs)

        return response

    @correct_return_codes
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
        response = self._create(url, **kwargs)

        return response

    @correct_return_codes
    def l7rule_delete(self, l7rule_id, l7policy_id):
        """Delete a l7rule

        :param string l7rule_id:
            ID of of l7rule to delete
        :param string l7policy_id:
            ID of the l7policy for this l7rule
        :return:
            Response Code from the API
        """
        url = const.BASE_SINGLE_L7RULE_URL.format(rule_uuid=l7rule_id,
                                                  policy_uuid=l7policy_id)
        response = self._delete(url)

        return response

    @correct_return_codes
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
        response = self._find(path=url, value=l7rule_id)

        return response

    @correct_return_codes
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
        response = self._create(url, method='PUT', **kwargs)

        return response

    def health_monitor_list(self, **kwargs):
        """List all health monitors

        :param kwargs:
            Parameters to filter on
        :return:
            A dict containing a list of health monitors
        """
        url = const.BASE_HEALTH_MONITOR_URL
        response = self._list(url, **kwargs)

        return response

    @correct_return_codes
    def health_monitor_create(self, **kwargs):
        """Create a health monitor

        :param kwargs:
            Parameters to create a health monitor with (expects json=)
        :return:
            A dict of the created health monitor's settings
        """
        url = const.BASE_HEALTH_MONITOR_URL
        response = self._create(url, **kwargs)

        return response

    @correct_return_codes
    def health_monitor_delete(self, health_monitor_id):
        """Delete a health_monitor

        :param string health_monitor_id:
            ID of of health monitor to delete
        :return:
            Response Code from the API
        """
        url = const.BASE_SINGLE_HEALTH_MONITOR_URL.format(
            uuid=health_monitor_id)
        response = self._delete(url)

        return response

    @correct_return_codes
    def health_monitor_show(self, health_monitor_id):
        """Show a health monitor's settings

        :param string health_monitor_id:
            ID of the health monitor to show
        :return:
            Dict of the specified health monitor's settings
        """
        url = const.BASE_HEALTH_MONITOR_URL
        response = self._find(path=url, value=health_monitor_id)

        return response

    @correct_return_codes
    def health_monitor_set(self, health_monitor_id, **kwargs):
        """Update a health monitor's settings

        :param health_monitor_id:
            ID of the health monitor to update
        :param kwargs:
            A dict of arguments to update a health monitor
        :return:
            Response Code from the API
        """
        url = const.BASE_SINGLE_HEALTH_MONITOR_URL.format(
            uuid=health_monitor_id)
        response = self._create(url, method='PUT', **kwargs)

        return response

    def quota_list(self, **params):
        """List all quotas

        :param params:
            Parameters to filter on (not implemented)
        :return:
            A ``dict`` representing a list of quotas for the project
        """
        url = const.BASE_QUOTA_URL
        response = self._list(url, **params)

        return response

    @correct_return_codes
    def quota_show(self, project_id):
        """Show a quota

        :param string project_id:
            ID of the project to show
        :return:
            A ``dict`` representing the quota for the project
        """
        response = self._find(path=const.BASE_QUOTA_URL, value=project_id)

        return response

    @correct_return_codes
    def quota_reset(self, project_id):
        """Reset a quota

        :param string project_id:
            The ID of the project to reset quotas
        :return:
            ``None``
        """
        url = const.BASE_SINGLE_QUOTA_URL.format(uuid=project_id)
        response = self._delete(url)

        return response

    @correct_return_codes
    def quota_set(self, project_id, **params):
        """Update a quota's settings

        :param string project_id:
            The ID of the project to update
        :param params:
            A ``dict`` of arguments to update project quota
        :return:
            A ``dict`` representing the updated quota
        """
        url = const.BASE_SINGLE_QUOTA_URL.format(uuid=project_id)
        response = self._create(url, method='PUT', **params)

        return response

    def quota_defaults_show(self):
        """Show quota defaults

        :return:
            A ``dict`` representing a list of quota defaults
        """
        url = const.BASE_QUOTA_DEFAULT_URL
        response = self._list(url)

        return response

    @correct_return_codes
    def amphora_show(self, amphora_id):
        """Show an amphora

        :param string amphora_id:
            ID of the amphora to show
        :return:
            A ``dict`` of the specified amphora's attributes
        """
        url = const.BASE_AMPHORA_URL
        response = self._find(path=url, value=amphora_id)

        return response

    def amphora_list(self, **kwargs):
        """List all amphorae

        :param kwargs:
            Parameters to filter on
        :return:
            A ``dict`` containing a list of amphorae
        """
        url = const.BASE_AMPHORA_URL
        response = self._list(path=url, **kwargs)

        return response

    @correct_return_codes
    def amphora_configure(self, amphora_id):
        """Update the amphora agent configuration

        :param string amphora_id:
            ID of the amphora to configure
        :return:
            Response Code from the API
        """
        url = const.BASE_AMPHORA_CONFIGURE_URL.format(uuid=amphora_id)
        response = self._create(url, method='PUT')

        return response

    @correct_return_codes
    def amphora_failover(self, amphora_id):
        """Force failover an amphorae

        :param string amphora_id:
            ID of the amphora to failover
        :return:
            Response Code from the API
        """
        url = const.BASE_AMPHORA_FAILOVER_URL.format(uuid=amphora_id)
        response = self._create(url, method='PUT')

        return response

    def provider_list(self):
        """List all providers

        :return:
            A ``dict`` containing a list of provider
        """
        url = const.BASE_PROVIDER_URL
        response = self._list(path=url)

        return response

    def provider_capability_list(self, provider):
        """Show the flavor capability of the specified provider.

        :param string provider:
            The name of the provider to show
        :return:
            A ``dict`` containing the capabilicy of provider
        """
        url = const.BASE_PROVIDER_FLAVOR_CAPABILITY_URL.format(
            provider=provider)
        response = self._list(url)

        return response

    def flavor_list(self, **kwargs):
        """List all flavors

        :param kwargs:
            Parameters to filter on
        :return:
            A ``dict`` containing a list of flavor
        """
        url = const.BASE_FLAVOR_URL
        response = self._list(path=url, **kwargs)

        return response

    @correct_return_codes
    def flavor_delete(self, flavor_id):
        """Delete a flavor

        :param string flavor_id:
            ID of the flavor to delete
        :return:
            Response Code from the API
        """
        url = const.BASE_SINGLE_FLAVOR_URL.format(uuid=flavor_id)
        response = self._delete(url)

        return response

    @correct_return_codes
    def flavor_create(self, **kwargs):
        """Create a flavor

        :param kwargs:
            Parameters to create a flavor with (expects json=)
        :return:
            A dict of the created flavor's settings
        """
        url = const.BASE_FLAVOR_URL
        response = self._create(url, **kwargs)

        return response

    @correct_return_codes
    def flavor_set(self, flavor_id, **kwargs):
        """Update a flavor's settings

        :param string flavor_id:
            ID of the flavor to update
        :param kwargs:
            A dict of arguments to update a flavor
        :return:
            Response Code from the API
        """
        url = const.BASE_SINGLE_FLAVOR_URL.format(uuid=flavor_id)
        response = self._create(url, method='PUT', **kwargs)

        return response

    @correct_return_codes
    def flavor_show(self, flavor_id):
        """Show a flavor

        :param string flavor_id:
            ID of the flavor to show
        :return:
            A dict of the specified flavor's settings
        """
        response = self._find(path=const.BASE_FLAVOR_URL, value=flavor_id)

        return response

    @correct_return_codes
    def flavorprofile_create(self, **kwargs):
        """Create a flavor profile

        :param kwargs:
            Parameters to create a flavor profile with (expects json=)
        :return:
            A dict of the created flavor profile's settings
        """
        url = const.BASE_FLAVORPROFILE_URL
        response = self._create(url, **kwargs)

        return response

    def flavorprofile_list(self, **kwargs):
        """List all flavor profiles

        :param kwargs:
            Parameters to filter on
        :return:
            List of flavor profile
        """
        url = const.BASE_FLAVORPROFILE_URL
        response = self._list(url, **kwargs)

        return response

    def flavorprofile_show(self, flavorprofile_id):
        """Show a flavor profile

        :param string flavorprofile_id:
            ID of the flavor profile to show
        :return:
            A dict of the specified flavor profile's settings
        """
        response = self._find(path=const.BASE_FLAVORPROFILE_URL,
                              value=flavorprofile_id)

        return response

    @correct_return_codes
    def flavorprofile_set(self, flavorprofile_id, **kwargs):
        """Update a flavor profile's settings

        :param string flavorprofile_id:
            ID of the flavor profile to update
        :kwargs:
            A dict of arguments to update the flavor profile
        :return:
            Response Code from the API
        """
        url = const.BASE_SINGLE_FLAVORPROFILE_URL.format(uuid=flavorprofile_id)
        response = self._create(url, method='PUT', **kwargs)

        return response

    @correct_return_codes
    def flavorprofile_delete(self, flavorprofile_id):
        """Delete a flavor profile

        :param string flavorprofile_id:
            ID of the flavor profile to delete
        :return:
            Response Code from the API
        """
        url = const.BASE_SINGLE_FLAVORPROFILE_URL.format(uuid=flavorprofile_id)
        response = self._delete(url)

        return response


class OctaviaClientException(Exception):
    """The base exception class for all exceptions this library raises."""

    def __init__(self, code, message=None, request_id=None):
        self.code = code
        self.message = message or self.__class__.message
        self.request_id = request_id

    def __str__(self):
        return "%s (HTTP %s) (Request-ID: %s)" % (self.message,
                                                  self.code,
                                                  self.request_id)
