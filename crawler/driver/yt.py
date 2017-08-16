import time

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
                for word in line.strip().replace('>','').split():
                    param = word.split('=')
                    if param[0] == 'content':
                        res['fields']['views'] = int(param[1].replace('"',''))
                        res['tags']['found'] = True
                        return res
        return res
