from eventlet.green import urllib2

class BaseDriver(object):

    def getData(self, tgt):
        vid, url = tgt
        data = urllib2.urlopen(url, timeout=1).readlines()
        return self.parseData(data, vid, url)

    def parseData(self):
        raise NotImplementedError
