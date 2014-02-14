# Scrapy settings for crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

COOKIES_ENABLED = False
SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'
DEFAULT_ITEM_CLASS = 'crawler.items.Profile'
DOWNLOADER_MIDDLEWARES = { 'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 1, }
FEED_EXPORTERS = {
    'bz2json':'crawler.feedformats.Bz2JsonLineExporter',
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawler (+http://www.yourdomain.com)'
