from scrapy.contrib.exporter import JsonLinesItemExporter
from scrapy.contrib.exporter import ScrapyJSONEncoder
from bz2 import BZ2File

class Bz2JsonLineExporter(JsonLinesItemExporter):
    def __init__(self, file, **kwargs):
        self._configure(kwargs, dont_fail=True)
        file.close()
        self.file = BZ2File(file.name, "w")
        self.encoder = ScrapyJSONEncoder(**kwargs)

    def finish_exporting(self):
        self.file.close()
