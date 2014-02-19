from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.exceptions import CloseSpider
from scrapy import log
from pyquery import PyQuery as pq
from crawler.items import Profile
from crawler import parser
from fake_useragent import UserAgent
from telnetlib import Telnet
import re, os, time

class LinkedinSpider(CrawlSpider):
    handle_httpstatus_list = [999]
    serverIP = os.environ['OPENSHIFT_PYTHON_IP'] if ('OPENSHIFT_PYTHON_IP' in os.environ) else '127.0.0.1'
    torProxyPort = os.environ['TOR_PROXY_PORT'] if ('TOR_PROXY_PORT' in os.environ) else '9050'
    torControlPort = os.environ['TOR_CONTROL_PORT'] if ('TOR_CONTROL_PORT' in os.environ) else '9051'
    proxyPort = None
    count = 0
    name = "linkedin"
    ua = UserAgent()
    stripspace = re.compile(r'\s+')
    stripnt = re.compile(r'\\n|\\t')
    #allowed_domains = ["linkedin.com"]
    start_urls = [
    'http://www.linkedin.com/in/nileshchakraborty',
    "http://ae.linkedin.com/pub/pradeep-kothari/4b/223/890",
    "http://in.linkedin.com/in/peddipradeep",
    "http://in.linkedin.com/in/pradeepbasu",
    "http://in.linkedin.com/in/pradeepbs",
    "http://in.linkedin.com/in/pradeepch",
    "http://in.linkedin.com/in/pradeepcharan",
    "http://in.linkedin.com/in/pradeepchopra",
    "http://in.linkedin.com/in/pradeepkarki",
    "http://in.linkedin.com/in/pradeepksharma",
    "http://in.linkedin.com/in/pradeepkumarjain1964",
    "http://in.linkedin.com/in/pradeepnahataindia",
    "http://in.linkedin.com/in/pradeepnair4",
    "http://in.linkedin.com/in/pradeeppradhanmumbai",
    "http://in.linkedin.com/pub/col-pradeep-singh-bhatnagar/5/528/300",
    "http://in.linkedin.com/pub/dir/Pradeep/+",
    "http://in.linkedin.com/pub/dir/Pradeep/+/in-7127-Bengaluru-Area%2C-India",
    "http://in.linkedin.com/pub/dir/Pradeep/+/in-7150-Mumbai-Area%2C-India",
    "http://in.linkedin.com/pub/dir/Pradeep/+/in-7151-New-Delhi-Area%2C-India",
    "http://in.linkedin.com/pub/dr-pradeep-kautish/17/8b/786",
    "http://in.linkedin.com/pub/eadara-pradeep-lion-15k-connection/28/779/850",
    "http://in.linkedin.com/pub/pradeep-hirani/4/b47/587",
    "http://in.linkedin.com/pub/pradeep-k-p/2b/50b/b03",
    "http://in.linkedin.com/pub/pradeep-kumar/9/851/636",
    "http://in.linkedin.com/pub/pradeep-nahata/18/b31/15",
    "http://in.linkedin.com/pub/pradeep-porwal/27/b52/686",
    "http://in.linkedin.com/pub/pradeep-shukla/13/7a6/1a8",
    "http://in.linkedin.com/pub/pradeep-shukla/20/58a/80b",
    "http://in.linkedin.com/pub/r-pradeep-balakumar-deputy-general-manager-corp-hr/4/777/1aa",
    "http://uk.linkedin.com/in/pradeepkumarg",
    "http://us.linkedin.com/pub/dir/Pradeep/+",
    ]

    def make_requests_from_url(self, url):
        if self.proxyPort == None:
            self.proxyPort = self.getProxyPort()
        # yield seed URLs for profiles to be parsed
        return Request(url, headers={'User-Agent':self.ua.random, 'Connection':'Keep-Alive'},
            meta={'proxy':"http://%s:%s" % (self.serverIP, self.torProxyPort)}, callback=self.parse, dont_filter=True)

    def parse(self, response):
        if response.status == 999:
            self.changeTorIP()
            self.log("Code 999 received. Changing Tor IP and sleeping 4s.", level=log.WARNING)
            time.sleep(4)
            yield Request(url=response.url, headers={'User-Agent':self.ua.random, 'Connection':'Keep-Alive'},
                meta={'proxy':"http://%s:%s" % (self.serverIP, self.torProxyPort)}, callback=self.parse)

        self.count += 1
        if self.count % 500 == 0:
            self.log("Count = %d." % self.count, level=log.WARNING)
        if self.count % 500 == 0:
            self.changeTorIP()

        for i in parser.getProfilePageURLs(response):
            if "http" not in i or "in.linkedin" not in i:
                continue
            #print "FOUND:%s" % i
            # yield URLs for profiles to be parsed
            yield Request(url=i, headers={'User-Agent':self.ua.random, 'Connection':'Keep-Alive'},
                meta={'proxy':"http://%s:%s" % (self.serverIP, self.torProxyPort)}, callback=self.parse)

        if "in.linkedin" in response.url:
            item = parser.parseProfile(response)
            fn = item['first_name']
            ln = item['last_name']
            # yield search URL requests to mine profiles via name search
            searchURI = 'http://in.linkedin.com/pub/dir/?first=%s&last=%s&search=Search&searchType=fps'
            for u in ((fn, ''), (ln, ''), ('', fn), ('', ln)):
                yield Request(url=searchURI % u, headers={'User-Agent':self.ua.random, 'Connection':'Keep-Alive'},
                    meta={'proxy':"http://%s:%s" % (self.serverIP, self.torProxyPort)}, callback=self.parseSearchPage)
            yield item

    def parseSearchPage(self, response):
        p = pq(response.body)
        for i in p('.vcard a[title]:not(.profile-photo)'):
            u = i.get('href')
            if 'in.linkedin' in u:
                # yield URLs for profiles to be parsed
                yield Request(url=u, headers={'User-Agent':self.ua.random, 'Connection':'Keep-Alive'},
                    meta={'proxy':"http://%s:%s" % (self.serverIP, self.torProxyPort)}, callback=self.parse)

    def changeTorIP(self):
        tn = Telnet(self.serverIP, int(self.torControlPort))
        tn.write("AUTHENTICATE\r\n")
        tn.read_until("250 OK", 2)
        tn.write("signal NEWNYM\r\n")
        tn.read_until("250 OK", 2)
        tn.write("QUIT\r\n")
        tn.close()

    def getProxyPort(self):
        i = int(self.torProxyPort)
        while True:
            yield i
            i = (i + 1) if i < (int(self.torProxyPort) + 5) else int(self.torProxyPort)