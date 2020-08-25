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


class OctaviaClientException(Exception):
    """The base exception class for all exceptions this library raises."""

    def __init__(self, code, message=None, request_id=None):
        self.code = code
        self.message = message or self.__class__.message
        super().__init__(self.message)
        self.request_id = request_id

    def __str__(self):
        return "%s (HTTP %s) (Request-ID: %s)" % (self.message,
                                                  self.code,
                                                  self.request_id)
