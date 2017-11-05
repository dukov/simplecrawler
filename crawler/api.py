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

import web
from web.httpserver import WSGIServer

import sys
import time
import gearman
import json

from crawler import base_service
from crawler import util

from oslo_config import cfg

from crawler.config import COMMON_OPTIONS

from gearman.errors import ExceededConnectionAttempts

urls = (
        '/', 'Urls',
        '/status', 'Status',
        '/agents', 'AgentCollection',
        '/jobs', 'JobCollection',
)

class Urls:
    def GET(self):
        return json.dumps(urls)

class Status:

    def GET(self):
        gm_admin_client = gearman.GearmanAdminClient(CONF.gearman)
        return json.dumps(gm_admin_client.get_status())

class AgentCollection:

    def GET(self):
        gm_admin_client = gearman.GearmanAdminClient(CONF.gearman)
        return json.dumps(gm_admin_client.get_workers())


class JobCollection:

    def send_range(self, start, stop, batch=10):
        data={
            'vid1': util.int2vid(start),
            'vid2': util.int2vid(stop),
            'batch': batch,
        }
        print "Sending data %s" % data
        gm_client = gearman.GearmanClient(CONF.gearman)
        return gm_client.submit_job('rpc_schedule', json.dumps(data),
                wait_until_complete=False, background=True, max_retries=10)

    def POST(self):
        #data = json.loads(web.data())
        #task_num = data.get('workers', 1)
        #vid1 = util.vid2int(data.get('vid1','aaaaaaaaaaa'))
        #vid2 = util.vid2int(data.get('vid2','aaaaaaaaaba'))
        #print vid1, vid2
        #start_vid = min(vid1, vid2)
        #stop_vid = max(vid1,vid2)
        #rng = 1000000
        #res = [] 
        #res.append(
        #    self.send_range(stop_vid - stop_vid % rng + start_vid % rng, stop_vid)
        #)
        #while start_vid <= stop_vid:
        #    try:
        #        res.append(self.send_range(start_vid, start_vid + rng - 1))
        #        start_vid += rng
        #    except ExceededConnectionAttempts:
        #        print "Exceeded connection attempts. Sleeping"
        #        start_vid += rng
        #        time.sleep(0.5)
        #
        #return res

        data = web.data()
        print "Sending data %s" % data
        gm_client = gearman.GearmanClient(CONF.gearman)
        return gm_client.submit_job('rpc_schedule', data,
                wait_until_complete=False, background=True, max_retries=10)

def main():
    CONF.register_cli_opts(COMMON_OPTIONS)
    CONF(sys.argv[2:])
    app.run()


CONF = cfg.CONF
app = web.application(urls, globals(), autoreload=False)
if __name__ == '__main__':
    main()
