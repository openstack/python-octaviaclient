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

"""Load Balancer action implementation"""


from cliff import lister
from osc_lib import utils


class ListLoadBalancer(lister.Lister):
    """List load balancers"""

    def parsed_args(self, prog_name):
        parser = super(ListLoadBalancer, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        columns = (
            'ID',
            'Name',
            'Project ID',
            'VIP Address',
            'Provisioning Status',)

        data = self.app.client_manager.load_balancer.load_balancer_list()
        return (columns,
                (utils.get_dict_properties(
                    s, columns,
                    formatters={},
                ) for s in data))
