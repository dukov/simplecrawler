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

from crawler.const import DB_DRIVER_MAP
from oslo_utils.importutils import import_class
from urlparse import urlparse


class DBCollection(object):
    def __init__(self, uris):
        self.dbs = []
        for uri in uris:
             drv_str = DB_DRIVER_MAP[urlparse(uri).scheme]
             db = import_class(drv_str)
             self.dbs.append(db(uri))

    def getCrawledVids(self):
        res = {}
        for db in self.dbs:
            res.update(db.getVIDs())
        return res

    def write_data(self, data):
        for db in self.dbs:
            db.write(data)
