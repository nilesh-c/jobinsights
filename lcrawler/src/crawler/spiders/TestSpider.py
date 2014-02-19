from telnetlib import Telnet
from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
import os, time

class TestSpider(CrawlSpider):
    serverIP = os.environ['OPENSHIFT_PYTHON_IP'] if ('OPENSHIFT_PYTHON_IP' in os.environ) else '127.0.0.1'
    torProxyPort = os.environ['TOR_PROXY_PORT'] if ('TOR_PROXY_PORT' in os.environ) else '9050'
    torControlPort = os.environ['TOR_CONTROL_PORT'] if ('TOR_CONTROL_PORT' in os.environ) else '9051'
    proxyPort = None
    count = 0
    name = "test"
    domain_name = "wtfismyip.com"
    # The following url is subject to change, you can get the last updated one from here :
    # http://www.whatismyip.com/faq/automation.asp
    start_urls = ["http://wtfismyip.com/text"]

    def make_requests_from_url(self, url):
        if self.proxyPort == None:
            self.proxyPort = self.getProxyPort()
        return Request(url, headers={'Connection':'Keep-Alive'}, meta={'proxy':"http://%s:%s" % (self.serverIP, self.proxyPort.next())}, dont_filter=True)
 
    def parse(self, response):
        self.count += 1
        print response.body
        time.sleep(2)
        yield Request(self.start_urls[0], headers={'Connection':'Keep-Alive'}, dont_filter=True, meta={'proxy':"http://%s:%s" % (self.serverIP, self.proxyPort.next())})

    def getProxyPort(self):
        i = int(self.torProxyPort)
        while True:
            yield i
            #i = (i + 1) if i < (int(self.torProxyPort) + 5) else int(self.torProxyPort)