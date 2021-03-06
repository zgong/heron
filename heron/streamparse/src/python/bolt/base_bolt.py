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
'''base_bolt.py'''

from heron.common.src.python.utils.tuple import TupleHelper

from ..component import HeronComponentSpec, BaseComponent
from ..stream import Stream

class BaseBolt(BaseComponent):
  """BaseBolt class

  This is the base for pyheron bolt, which wraps the implementation of publicly available methods.
  This includes:
    - <classmethod> spec()
    - emit()
    - <staticmethod> is_tick()
    - ack()
    - fail()

  They are compatible with StreamParse API.
  """
  # pylint: disable=no-member
  @classmethod
  def spec(cls, name=None, inputs=None, par=1, config=None):
    """Register this bolt to the topology and create ``HeronComponentSpec``

    The usage of this method is compatible with StreamParse API, although it does not create
    ``ShellBoltSpec`` but instead directly registers to a ``Topology`` class.

    This method does not take a ``outputs`` argument because ``outputs`` should be
    an attribute of your ``Spout`` subclass. Also, some ways of declaring inputs is not supported
    in this implementation; please read the documentation below.

    :type name: str
    :param name: Name of this bolt.
    :param inputs: Streams that feed into this Bolt.

                   Two forms of this are acceptable:

                   1. A `dict` mapping from ``HeronComponentSpec`` to ``Grouping``.
                      In this case, default stream is used.
                   2. A `dict` mapping from ``GlobalStreamId`` to ``Grouping``.
                      This ``GlobalStreamId`` object itself is different from StreamParse, because
                      Heron does not use thrift, although its constructor method is compatible.
                   3. A `list` of ``HeronComponentSpec``. In this case, default stream with
                      SHUFFLE grouping is used.
                   4. A `list` of ``GlobalStreamId``. In this case, SHUFFLE grouping is used.
    :type par: int
    :param par: Parallelism hint for this spout.
    :type config: dict
    :param config: Component-specific config settings.
    """
    python_class_path = "%s.%s" % (cls.__module__, cls.__name__)

    if hasattr(cls, 'outputs'):
      _outputs = cls.outputs
    else:
      _outputs = None

    return HeronComponentSpec(name, python_class_path, is_spout=False, par=par,
                              inputs=inputs, outputs=_outputs, config=config)

  def emit(self, tup, stream=Stream.DEFAULT_STREAM_ID,
           anchors=None, direct_task=None, need_task_ids=False):
    """Emits a new tuple from this Bolt

    It is compatible with StreamParse API.

    :type tup: list or tuple
    :param tup: the new output Tuple to send from this bolt,
                should only contain only serializable data.
    :type stream: str
    :param stream: the ID of the stream to emit this Tuple to.
                   Leave empty to emit to the default stream.
    :type anchors: list
    :param anchors: a list of HeronTuples to which the emitted Tuples should be anchored.
    :type direct_task: int
    :param direct_task: the task to send the Tuple to if performing a direct emit.
    :type need_task_ids: bool
    :param need_task_ids: indicate whether or not you would like the task IDs the Tuple was emitted.
    """
    self.delegate.emit(tup, stream, anchors, direct_task, need_task_ids)

  @staticmethod
  def is_tick(tup):
    """Returns whether or not the given HeronTuple is a tick Tuple

    It is compatible with StreamParse API.
    """
    return tup.stream == TupleHelper.TICK_TUPLE_ID

  def ack(self, tup):
    """Indicate that processing of a Tuple has succeeded

    It is compatible with StreamParse API.
    """
    self.delegate.ack(tup)

  def fail(self, tup):
    """Indicate that processing of a Tuple has failed

    It is compatible with StreamParse API.
    """
    self.delegate.fail(tup)
