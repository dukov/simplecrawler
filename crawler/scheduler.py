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
import time

from crawler import util
from influxdb import InfluxDBClient
from oslo_config import cfg
from urlparse import urlparse

from crawler.config import COMMON_OPTIONS


class Scheduler(object):
    def __init__(self, conf):
        super(Scheduler, self).__init__(conf.gearman)
        self.conf = conf
        db_params = urlparse(self.conf.db_uri)
        self.db = InfluxDBClient(
            db_params.host,
            db_params.port,
            db_params.username,
            db_params.password,
            db_params.path[1:]
        )
        self.db.create_database('crawler')
        self.crawled_vids = {}

    def getCrawledVids(self):
        age = time.time() - self.crawled_vids.get('updated_at', 0)
        if age > 300:
            query = 'select views from views group by id;'
            vid_list = [x[1]['id'] for x in self.db.query(query).keys()]
            self.crawled_vids['data'] = vid_list
            self.crawled_vids['updated_at'] = time.time()
        return self.crawled_vids['data']

    def rpc_schedule(self, gm_w, job):
        task = json.loads(job.data)
        payload = {}
        id_size = task.get('id_size', 11)
        max_vid = task.get('max_vid', 121)
        batch = task.get('batch', 10)

        for int_vid, vid in util.vid_gen(max_vid, id_size):
            if len(payload) < batch and int_vid < max_vid - batch:
                vid_str = ''.join(vid)
                if vid_str in self.getCrawledVids():
                    continue
                url = "https://www.youtube.com/watch?v=%s" % vid_str
                payload[vid_str] = url
            elif payload != {}:
                print("Sending job %s" % payload)
                self.gm_client.submit_job('process', json.dumps(
                    payload), wait_until_complete=False, background=True)
                payload = {}


def main():
    CONF = cfg.CONF
    CONF.register_cli_opts(COMMON_OPTIONS)
    CONF(sys.argv[1:])
    sched = Scheduler(CONF)
    sched.run()


if __name__ == "__main__":
    sys.exit(main())
