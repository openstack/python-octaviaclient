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

BASE_LOADBALANCER_URL = '/loadbalancers'
BASE_SINGLE_LB_URL = BASE_LOADBALANCER_URL + '/{uuid}'

BASE_LISTENER_URL = '/listeners'
BASE_SINGLE_LISTENER_URL = BASE_LISTENER_URL + '/{uuid}'

BASE_POOL_URL = '/pools'
BASE_SINGLE_POOL_URL = BASE_POOL_URL + '/{pool_id}'

BASE_MEMBER_URL = BASE_SINGLE_POOL_URL + '/members'
BASE_SINGLE_MEMBER_URL = BASE_MEMBER_URL + '/{member_id}'

BASE_HEALTH_MONITOR_URL = '/healthmonitors'
BASE_SINGLE_HEALTH_MONITOR_URL = BASE_HEALTH_MONITOR_URL + '/{uuid}'

BASE_L7POLICY_URL = '/l7policies'
BASE_SINGLE_L7POLICY_URL = BASE_L7POLICY_URL + '/{policy_uuid}'
BASE_L7RULE_URL = BASE_SINGLE_L7POLICY_URL + '/rules'
BASE_SINGLE_L7RULE_URL = BASE_SINGLE_L7POLICY_URL + '/rules/{rule_uuid}'
