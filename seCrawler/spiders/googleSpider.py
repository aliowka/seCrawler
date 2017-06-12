"""
GoogleSpider derived from keywordSpider, so the crawling process remains the same (start url and pagination).
The minor changes are as following:
1. List of "items" defined in spider to store the items, this allows to get a fast access to them from the runner.
2. "__xpath" method defined to help extract different xpathes from the given selector
3. "parse" method is overridden to handle googles search results structure.
"""
from seCrawler.spiders.keywordSpider import keywordSpider


class GoogleSpider(keywordSpider):
    name = 'google'

    def __init__(self, *args, **kwargs):
        super(GoogleSpider, self).__init__(*args, **kwargs)
        self.items = []

    def __xpath(self, selector, xp, extract=True):
        res = selector.xpath(xp).extract() if extract else selector.xpath(xp)
        if res and type(res) == list:
            return " ".join(res)
        return res

    def parse(self, response):

        for container in self.__xpath(response, "//div[@class='rc']", False):
            item = dict()
            item["url"] = self.__xpath(container, './/h3/a/@href')
            item["title"] = self.__xpath(container, './/h3/a//text()')
            item["desc"] = self.__xpath(container, './/span[@class="st"]//text()')
            self.items.append(item)
            yield item
