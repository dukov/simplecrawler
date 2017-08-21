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

import eventlet
import json
import sys

from crawler import base_service

from crawler.driver import yt


class Worker(base_service.BaseService):
    def __init__(self):
        super(Worker, self).__init__(['localhost:4730'])
        self.pool = eventlet.GreenPool()
        self.driver = yt.YouTubeDriver()

    def rpc_processURLs(self, gm_w, job):
        print("Got new job for url %s" % job.data)
        urls = json.loads(job.data)
        report = []
        for res in self.pool.imap(self.driver.getData, urls.items()):
            report.append(res)

        self.reportResult(report)
        return ""

    def reportResult(self, res):
        print(res)
        self.rpc_client.rpc_call('rpc_update_db', json.dumps(res))


def main():
    wrkr = Worker()
    wrkr.run()


if __name__ == "__main__":
    sys.exit(main())
