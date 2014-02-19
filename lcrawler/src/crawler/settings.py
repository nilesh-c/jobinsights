# Scrapy settings for crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

# DUMPSTATS_ENABLED = True
# DUMPSTATS_INTERVAL = 2
DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'
CONCURRENT_REQUESTS = 25
CONCURRENT_REQUESTS_PER_DOMAIN = 25
# WEBSERVICE_ENABLED = False
WEBSERVICE_HOST = os.environ['OPENSHIFT_PYTHON_IP'] if ('OPENSHIFT_PYTHON_IP' in os.environ) else '127.0.0.1'
WEBSERVICE_PORT = 8080
TELNETCONSOLE_ENABLED = False
COOKIES_ENABLED = False
SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'
DEFAULT_ITEM_CLASS = 'crawler.items.Profile'
DOWNLOADER_MIDDLEWARES = { 'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 1, }
DOWNLOAD_HANDLERS = {
	'http': 'crawler.http.TorProxyDownloadHandler'
}
# EXTENSIONS = {
# 	'crawler.extensions.DumpStats': 0
# }
WEBSERVICE_RESOURCES = {
	'crawler.resources.StatusResource': 1
}
FEED_EXPORTERS = {
    'bz2json':'crawler.feedformats.Bz2JsonLineExporter',
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawler (+http://www.yourdomain.com)'
