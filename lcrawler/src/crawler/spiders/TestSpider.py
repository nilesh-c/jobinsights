from telnetlib import Telnet
from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
import os, time

class TestSpider(CrawlSpider):
    serverIP = os.environ['OPENSHIFT_PYTHON_IP'] if ('OPENSHIFT_PYTHON_IP' in os.environ) else '127.0.0.1'
    privoxyPort = os.environ['PRIVOXY_PORT'] if ('PRIVOXY_PORT' in os.environ) else '8118'
    torControlPort = os.environ['TOR_CONTROL_PORT'] if ('TOR_CONTROL_PORT' in os.environ) else '9051'
    count = 0
    name = "test"
    domain_name = "wtfismyip.com"
    # The following url is subject to change, you can get the last updated one from here :
    # http://www.whatismyip.com/faq/automation.asp
    start_urls = ["http://wtfismyip.com/text"]

    def make_requests_from_url(self, url):
        return Request(url, headers={'Connection':'Keep-Alive'}, meta={'proxy':"http://%s:%s" % (self.serverIP, self.privoxyPort)}, dont_filter=True)
 
    def parse(self, response):
        self.count += 1
        if self.count % 10 == 0:
            tn = Telnet(self.serverIP, int(self.torControlPort))
            tn.write("AUTHENTICATE\r\n")
            tn.read_until("250 OK", 2)
            tn.write("signal NEWNYM\r\n")
            tn.read_until("250 OK", 2)
            tn.write("QUIT\r\n")
            tn.close()
        print response.body
        yield Request(self.start_urls[0], headers={'Connection':'Keep-Alive'}, dont_filter=True, meta={'proxy':"http://%s:%s" % (self.serverIP, self.privoxyPort)})
