import gearman
import json
import time

from crawler import util
from influxdb import InfluxDBClient

class Scheduler(object):
    def __init__(self):
        self.gm_client = gearman.GearmanClient(['localhost:4730'])
        self.db = InfluxDBClient('localhost', 8086, 'root', 'root', 'crawler')
        self.db.create_database('crawler')
        self.crawled_vids = {}

    def getCrawledVids(self):

        age = time.time() - self.crawled_vids.get('updated_at', 0)
        if age > 300:
            query = 'select views from views group by id;'
            vid_list = [x[1]['id'] for x in self.db.query(query).keys()]
            self.crawled_vids['data'] = vid_list
            self.crawled_vids['updated_at'] = time.time()
        return self.crawled_vids['data']

    def checkInDb(self, vid):
        pass

    def _generateVID(self):
        payload = {}
        id_size = 11
        max_vid = 121
        batch = 10

        for int_vid, vid in util.vid_gen(max_vid, id_size):
            if len(payload) < batch and int_vid < max_vid - batch:
                vid_str = ''.join(vid)
                if vid_str in self.getCrawledVids():
                    continue
                url = "https://www.youtube.com/watch?v=%s" % vid_str
                payload[vid_str] = url
            elif payload != {}:
                print "Sending job %s"%payload
                req = self.gm_client.submit_job('process', json.dumps(payload),
                    wait_until_complete=False, background=True)
                payload = {}
