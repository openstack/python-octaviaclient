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

BASE_MONITOR_URL = '/healthmonitors'
BASE_SINGLE_MONITOR_URL = '/healthmonitors/{uuid}'
