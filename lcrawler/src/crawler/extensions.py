from scrapy import signals, log
import json
from scrapy.exceptions import NotConfigured

class DumpStats(object):

    def __init__(self, interval, stats):
        self.stats = stats
        self.interval = interval
        self.items_scraped = 0

    @classmethod
    def from_crawler(cls, crawler):
        # first check if the extension should be enabled and raise
        # NotConfigured otherwise
        if not crawler.settings.getbool('DUMPSTATS_ENABLED'):
            raise NotConfigured

        interval = crawler.settings.getint('DUMPSTATS_INTERVAL')
        # instantiate the extension object
        ext = cls(interval, crawler.stats)

        # connect the extension object to signals
        crawler.signals.connect(ext.item_scraped, signal=signals.response_received)

        # return the extension object
        return ext

    def item_scraped(self,  spider):
        self.items_scraped += 1
        if self.items_scraped % self.interval == 0:
            stats = self.stats.get_stats()
            stats['start_time'] = str(stats['start_time'])
            spider.log(str(json.dumps(stats, indent=4, sort_keys=True)), level=log.WARNING)