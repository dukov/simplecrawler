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

import plyvel

from urlparse import urlparse

class DBLevelUP(object):
    def __init__(self, uri):
        db_params = urlparse(uri)
        self.db = plyvel.DB(db_params.path, create_if_missing=True)

    def write(self, data):
        with self.db.write_batch() as wb:
            for item in data:
                wb.put(str(item['tags']['id']), str(item['fields']['views']))

    def getVIDs(self):
        return list(self.db)
