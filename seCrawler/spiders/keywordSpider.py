__author__ = 'tixie'
from scrapy.spiders import Spider
from seCrawler.common.searResultPages import searResultPages
from seCrawler.common.searchEngines import SearchEngineResultSelectors
from scrapy.selector import  Selector

class keywordSpider(Spider):
    name = 'keywordSpider'
    allowed_domains = ['bing.com','google.com','baidu.com']
    start_urls = []
    keyword = None
    searchEngine = None
    selector = None
    items = []

    def __init__(self, keyword, se = 'bing', pages = 50,  *args, **kwargs):
        super(keywordSpider, self).__init__(*args, **kwargs)
        self.keyword = keyword.lower()
        self.searchEngine = se.lower()
        self.selector = SearchEngineResultSelectors[self.searchEngine]
        pageUrls = searResultPages(keyword, se, int(pages))
        for url in pageUrls:
            print(url)
            self.start_urls.append(url)

    def _xpath(self, selector, xp, extract=True):
        res = selector.xpath(xp).extract() if extract else selector.xpath(xp)
        if res and type(res) == list:
            return " ".join(res)
        return res

    def parse(self, response):
        for url in Selector(response).xpath(self.selector).extract():
            yield {'url':url}

        pass
