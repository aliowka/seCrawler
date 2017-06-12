from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet.defer import inlineCallbacks, returnValue


class CrawlersManager(object):

    @staticmethod
    @inlineCallbacks
    def start_crawler(keyword, se_name, pages):
        """
        Load a spider dynamical by it's name which should correspond to se_name.
        Currently only 'google' spider is implemented.
        Run a crawler with seCrawler.settings and when the crawling is done,
        returns the crawler instance.
        :param keyword: keyword to search for
        :param se: search engine to use
        :param pages: max number of pages to scan
        :return: crawler instance
        """

        settings = get_project_settings()
        runner = CrawlerRunner(settings)
        spider = runner.spider_loader.load(se_name)
        assert spider, "The spider for the given search engine is not implemented"

        runner.crawl(spider, keyword=keyword, se=se_name, pages=pages)
        crawler = list(runner.crawlers)[0]
        yield runner.join()
        returnValue(crawler)

