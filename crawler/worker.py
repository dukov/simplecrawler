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
from oslo_config import cfg

from crawler.config import COMMON_OPTIONS
from crawler.driver import yt
from crawler.logger import logger


class Worker(base_service.BaseService):
    def __init__(self, conf):
        logger.debug("Initialising worker")
        super(Worker, self).__init__(conf.gearman)
        self.conf = conf
        self.pool = eventlet.GreenPool()
        self.driver = yt.YouTubeDriver()

    def rpc_processURLs(self, gm_w, job):
        logger.info("Got new job for url %s" % job.data)
        urls = json.loads(job.data)
        report = []
        for res in self.pool.imap(self.driver.getData, urls.items()):
            report.append(res)

        self.reportResult(report)
        return ""

    def reportResult(self, res):
        logger.debug("Reporting result %s" % res)
        self.rpc_client.rpc_call('rpc_update_db', json.dumps(res))


def main():
    CONF = cfg.CONF
    CONF.register_cli_opts(COMMON_OPTIONS)
    CONF(sys.argv[1:])
    wrkr = Worker(CONF)
    wrkr.run()


if __name__ == "__main__":
    sys.exit(main())
