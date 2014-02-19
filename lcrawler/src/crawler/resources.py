from scrapy.webservice import JsonResource
from  twisted.web.resource import Resource
import json

class StatusResource(Resource):

	ws_name = "status"
	isLeaf = True

	def __init__(self, crawler, spider_name=None):
		self.crawler = crawler
		self._spider_name = spider_name
		# self.isLeaf = spider_name is not None

	def render_GET(self, request):
		stats = self.crawler.stats.get_stats()
		stats['start_time'] = str(stats['start_time'])
		dump = json.dumps(stats, indent=4, sort_keys=True).replace("\n", "\n<br/>")
		return "<html><body>%s</body></html>" % dump