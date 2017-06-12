"""
GoogleSpider derived from keywordSpider, so the crawling process remains the same (start url and pagination).
The minor changes are as following:
1. List of "items" defined in spider to store the items, this allows to get a fast access to them from the runner.
2. "parse" method is overridden to handle googles results structure.
"""
from seCrawler.spiders.keywordSpider import keywordSpider


class GoogleSpider(keywordSpider):
    name = 'google'

    def parse(self, response):

        for container in self._xpath(response, "//div[@class='rc']", False):
            item = dict()
            item["url"] = self._xpath(container, './/h3/a/@href')
            item["title"] = self._xpath(container, './/h3/a//text()')
            item["desc"] = self._xpath(container, './/span[@class="st"]//text()')
            self.items.append(item)
            yield item

