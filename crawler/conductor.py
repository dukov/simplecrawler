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

import json

from crawler import base_service
from influxdb import InfluxDBClient


class Conductor(base_service.BaseService):
    def __init__(self):
        super(Conductor, self).__init__(['localhost:4730'])
        self.db = InfluxDBClient('localhost', 8086, 'root', 'root', 'crawler')
        self.db.create_database('crawler')

    def rpc_update_db(self, gm_w, job):
        results = json.loads(job.data)
        self.db.write_points(results)
