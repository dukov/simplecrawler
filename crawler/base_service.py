# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import uuid

from crawler.driver import rpc_gearman
from crawler.logger import logger


class BaseService(object):
    def __init__(self, gearman_hosts):
        class_name = self.__class__.__name__
        self.id = "{0}_{1}".format(class_name, str(uuid.uuid4()))
        self.rpc_client = rpc_gearman.RPCGearman(gearman_hosts, self.id)
        for method in dir(self):
            if method.startswith('rpc_'):
                func = getattr(self, method)
                self.rpc_client.register_task(method, func)

    def run(self):
        logger.info("Starting Service")
        self.rpc_client.run()
