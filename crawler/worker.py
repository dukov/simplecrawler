import eventlet
import gearman
import uuid
import json
import logging

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
        print "Got new job for url %s"%job.data
        urls = json.loads(job.data)
        report = []
        for res in self.pool.imap(self.driver.getData, urls.items()):
            report.append(res)

        self.reportResult(report)
        return ""

    def reportResult(self, res):
        print res
        self.db.write_points(res)

    def run(self):
        self.gm_worker.work()
