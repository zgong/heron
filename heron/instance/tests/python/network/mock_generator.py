# Copyright 2016 Twitter. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
'''mock_generator for instance/network'''
# pylint : disable=missing-docstring

from heron.common.src.python.basics import EventLooper
from heron.common.src.python.network import SocketOptions
from heron.common.src.python.utils.misc import HeronCommunicator
from heron.instance.src.python.network import SingleThreadStmgrClient, MetricsManagerClient
import heron.common.src.python.constants as constants
import heron.common.tests.python.mock_protobuf as mock_protobuf

class MockSTStmgrClient(SingleThreadStmgrClient):
  HOST = '127.0.0.1'
  PORT = 9000

  def __init__(self):
    socket_options = SocketOptions(32768, 16, 32768, 16, 1024000, 1024000)
    sys_config = {constants.INSTANCE_RECONNECT_STREAMMGR_INTERVAL_SEC: 10}
    SingleThreadStmgrClient.__init__(self, EventLooper(), None, self.HOST, self.PORT,
                                     "topology_name", "topology_id",
                                     mock_protobuf.get_mock_instance(), {},
                                     None, socket_options, sys_config)

    self.register_msg_called = False
    self.handle_register_response_called = False

  def _register_msg_to_handle(self):
    self.register_msg_called = True

  # pylint: disable=unused-argument
  def _handle_register_response(self, response):
    self.handle_register_response_called = True

class MockMetricsManagerClient(MetricsManagerClient):
  HOST = '127.0.0.1'
  PORT = 9000
  def __init__(self):
    socket_options = SocketOptions(32768, 16, 32768, 16, 1024000, 1024000)
    sys_config = {constants.INSTANCE_RECONNECT_METRICSMGR_INTERVAL_SEC: 10}
    MetricsManagerClient.__init__(self, EventLooper(), self.HOST, self.PORT,
                                  mock_protobuf.get_mock_instance(), HeronCommunicator(), {},
                                  socket_options, sys_config)
    self.register_req_called = False

  def _send_register_req(self):
    self.register_req_called = True
