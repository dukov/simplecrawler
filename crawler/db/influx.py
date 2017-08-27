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

from influxdb import InfluxDBClient
from urlparse import urlparse


class DBInflux(object):
    def __init__(self, uri):
        import pdb;pdb.set_trace()
        db_params = urlparse(uri)
        self.db = InfluxDBClient(
            db_params.hostname,
            db_params.port,
            db_params.username,
            db_params.password,
            db_params.path[1:]
        )
        self.db.create_database('crawler')
        self.crawled_vids = {}

    def getVIDs(self):
        age = time.time() - self.crawled_vids.get('updated_at', 0)
        if age > 300:
            query = 'select views from views group by id;'
            vid_list = [x[1]['id'] for x in self.db.query(query).keys()]
            self.crawled_vids['data'] = vid_list
            self.crawled_vids['updated_at'] = time.time()
        return self.crawled_vids['data']

    def write(self, data):
        self.db.write_points(data)

