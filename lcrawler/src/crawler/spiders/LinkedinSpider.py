from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.exceptions import CloseSpider
from scrapy import log
from telnetlib import Telnet
from fake_useragent import UserAgent
from crawler.items import Profile
from crawler import parser
import re, os

class LinkedinSpider(CrawlSpider):
    serverIP = os.environ['OPENSHIFT_PYTHON_IP'] if ('OPENSHIFT_PYTHON_IP' in os.environ) else '127.0.0.1'
    privoxyPort = os.environ['PRIVOXY_PORT'] if ('PRIVOXY_PORT' in os.environ) else '8118'
    torControlPort = os.environ['TOR_CONTROL_PORT'] if ('TOR_CONTROL_PORT' in os.environ) else '9051'
    count = 0
    name = "linkedin"
    ua = UserAgent()
    stripspace = re.compile(r'\s+')
    stripnt = re.compile(r'\\n|\\t')
    #allowed_domains = ["linkedin.com"]
    start_urls = [
        'http://www.linkedin.com/pub/suzan-alaswad-phd/51/804/459?trk=pub-pbmap',
        'http://www.linkedin.com/in/nileshchakraborty',
	    'http://sg.linkedin.com/pub/debarka-sengupta/7/751/360',
    	'http://dk.linkedin.com/in/rhodesnu',
	    'http://www.linkedin.com/in/officialjohnmaxwell',
    ]

    def make_requests_from_url(self, url):
            return Request(url, headers={'User-Agent':self.ua.random, 'Connection':'Keep-Alive'}, meta={'proxy':"http://%s:%s" % (self.serverIP, self.privoxyPort)}, dont_filter=True)

    def parse(self, response):
        if response.status == 999:
            self.changeTorIP()
            self.log("Code 999 received. Changing Tor IP and sleeping 4s.", level=log.WARNING)
            time.sleep(4)
            yield Request(url=response.url, headers={'User-Agent':self.ua.random, 'Connection':'Keep-Alive'}, meta={'proxy':"http://%s:%s" % (self.serverIP, self.privoxyPort)})
        self.count += 1
        if self.count % 500 == 0:
            self.changeTorIP()
        if self.count == 242:
            raise CloseSpider("Finished scraping 200 profiles.")
        sel = Selector(response)
        for i in sel.xpath("//strong/a[contains(@href,'linkedin')]/@href").extract():
            if "http" not in i:
                continue
            #print "FOUND:%s" % i
            yield Request(url=i, headers={'User-Agent':self.ua.random, 'Connection':'Keep-Alive'}, meta={'proxy':"http://%s:%s" % (self.serverIP, self.privoxyPort)})

        # if "in.linkedin" in response.url:
        item = parser.parseProfile(response)
        yield item

    def changeTorIP(self):
        tn = Telnet(self.serverIP, int(self.torControlPort))
        tn.write("AUTHENTICATE\r\n")
        tn.read_until("250 OK", 2)
        tn.write("signal NEWNYM\r\n")
        tn.read_until("250 OK", 2)
        tn.write("QUIT\r\n")
        tn.close()
