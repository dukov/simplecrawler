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

from crawler.driver.base import BaseDriver


class YouTubeDriver(BaseDriver):
    def parseData(self, data, vid, url):
        res = {}
        res['measurement'] = 'views'
        res['tags'] = {
            'id': vid,
            'url': url,
            'found': False
        }
        res['fields'] = {'views': 0}
        for line in data:
            if "nteractionCount" in line:
                for word in line.strip().replace('>', '').split():
                    param = word.split('=')
                    if param[0] == 'content':
                        res['fields']['views'] = int(param[1].replace('"', ''))
                        res['tags']['found'] = True
                        return res
        return res
