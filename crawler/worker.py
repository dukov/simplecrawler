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
import gearman
import json
import logging
import sys
import uuid

from crawler.driver import yt
from influxdb import InfluxDBClient


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Worker(object):
    def __init__(self):
        self.pool = eventlet.GreenPool()
        self.driver = yt.YouTubeDriver()
        self.id = str(uuid.uuid4())
        self.gm_worker = gearman.GearmanWorker(['localhost:4730'])
        self.gm_worker.set_client_id(self.id)
        self.gm_worker.register_task('process', self.processURLs)
        self.db = InfluxDBClient('localhost', 8086, 'root', 'root', 'crawler')
        self.db.create_database('crawler')

    def processURLs(self, gm_w, job):
        print("Got new job for url %s" % job.data)
        urls = json.loads(job.data)
        report = []
        for res in self.pool.imap(self.driver.getData, urls.items()):
            report.append(res)

        self.reportResult(report)
        return ""

    def reportResult(self, res):
        print(res)
        self.db.write_points(res)

    def run(self):
        self.gm_worker.work()


def main():
    wrkr = Worker()
    wrkr.run()

if __name__ == "__main__":
    sys.exit(main())
