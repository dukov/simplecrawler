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
import sys

from crawler import base_service
from crawler import util
from oslo_config import cfg

from crawler.config import COMMON_OPTIONS
from crawler.db import collection


class Scheduler(base_service.BaseService):
    def __init__(self, conf):
        super(Scheduler, self).__init__(conf.gearman)
        self.dbc = collection.DBCollection(conf.db_uris)
        self.conf = conf

    def rpc_schedule(self, gm_w, job):
        print "Got rquest %s" % job.data
        task = json.loads(job.data)
        payload = {}
        vid1 = util.vid2int(task.get('vid1', '7-Sl8uXOb5k'))
        vid2 = util.vid2int(task.get('vid2', '7-Sl8uXOb5t'))
        start_vid = min(vid1, vid2)
        stop_vid = max(vid1,vid2)
        batch = task.get('batch', 10)

        for int_vid in util.vid_gen(start_vid, stop_vid):
            vid_str = util.int2vid(int_vid)
            if len(payload) < batch and int_vid < stop_vid + 1 - batch or payload == {}:
                if vid_str in self.dbc.getCrawledVids():
                    continue
                url = "https://www.youtube.com/watch?v=%s" % vid_str
                payload[vid_str] = url
            elif payload != {}:
                print("Sending job %s" % payload)
                self.rpc_client.rpc_call('rpc_processURLs', json.dumps(
                    payload), wait_until_complete=False, background=True)
                payload = {}
        return ""


def main():
    CONF = cfg.CONF
    CONF.register_cli_opts(COMMON_OPTIONS)
    CONF(sys.argv[1:])
    sched = Scheduler(CONF)
    sched.run()


if __name__ == "__main__":
    sys.exit(main())
