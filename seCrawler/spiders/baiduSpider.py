"""
BaiduSpider derived from keywordSpider, so the crawling process remains the same (start url and pagination).
The minor changes are as following:
1. List of "items" defined in spider to store the items, this allows to get a fast access to them from the runner.
2. "parse" method should be overridden to handle baidu results structure.
"""
from seCrawler.spiders.keywordSpider import keywordSpider


class BaiduSpider(keywordSpider):
    name = 'baidu'

    def parse(self, response):
        raise NotImplementedError()
