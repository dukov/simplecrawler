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
import sys

from crawler import base_service
from oslo_config import cfg

from crawler.config import COMMON_OPTIONS
from crawler.db import collection


class Conductor(base_service.BaseService):
    def __init__(self, conf):
        super(Conductor, self).__init__(conf.gearman)
        self.dbc = collection.DBCollection(conf.db_uris)
        self.conf = conf

    def rpc_update_db(self, gm_w, job):
        print "Got data"
        results = json.loads(job.data)
        self.dbc.write_data(results)
        return ""

    def rpc_get_crawled(self, gm_w, job):
        vids = self.dbc.getCrawledVids()
        return json.dumps(vids)


def main():
    CONF = cfg.CONF
    CONF.register_cli_opts(COMMON_OPTIONS)
    CONF(sys.argv[1:])
    cond = Conductor(CONF)
    cond.run()


if __name__ == "__main__":
    sys.exit(main())
