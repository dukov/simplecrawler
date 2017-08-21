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

import gearman


class RPCGearman(object):
    def __init__(self, srvrs, client_id):
        self.id = client_id
        self.hosts = srvrs
        self.reciever = gearman.GearmanWorker(self.hosts)
        self.reciever.set_client_id(self.id)
        self.sender = gearman.GearmanClient(self.hosts)

    def register_task(self, task_name, func):
        self.reciever.register_task(task_name, func)

    def rpc_call(self, method, data, **kwargs):
        self.sender.submit_job(method, data, **kwargs)

    def run(self):
        self.reciever.work()
