"""
This provides a RESTFULL service which 
"""
import sys
import json
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.internet import reactor
from twisted.web.server import Site, NOT_DONE_YET
from twisted.web.resource import Resource

from seCrawler.common.crawlersManager import CrawlersManager
from seCrawler.settings import SERVICE_PORT
from twisted.python import log
log.startLogging(sys.stdout)

REQUEST_PARAMS = ("se",  # search engine name (for this home work only "google" is implemented)
                 "keyword",  # keyword to search
                 "pages")  # maximum number of pages to scan



class CrawlerAPI(Resource):
    def render_GET(self, request):
        """
        Handler for GET request. 
        Here we set the content type for the response, since it always should be in
        a json type.
        :param request: twisted.web.http.Request
        :return: NOT_DONE_YET: The response will be processed asynchronously
        """

        request.responseHeaders.addRawHeader(b"content-type", b"application/json")

        # Schedule request processing
        reactor.callLater(0, self._process_request, request)
        return NOT_DONE_YET

    @inlineCallbacks
    def _process_request(self, request):

        """ 
        We check that all REQUEST_PARAMS are present in a request.
        If not, respond with 422 error (missing parameter)
        Then, fetch the parameters from the request and start crawling.
        When crawling is done, get results from crawler.items and send them as a response
        :param request: 
        """

        for arg in REQUEST_PARAMS:
            if arg not in request.args:
                request.setResponseCode(422)
                body = json.dumps({"error": "parameter is missing: %s" % arg})
                self.send_response(request, body)

        se, keyword, pages = [request.args.get(p)[0] for p in REQUEST_PARAMS]
        crawler = yield CrawlersManager.start_crawler(keyword, se, pages)
        body = json.dumps({"results": crawler.spider.items})
        self.send_response(request, body)

    def send_response(self, request, body):
        """
        Send responsee and close the request
        :param request: request to respond to
        :param body: json string
        """
        request.write(body)
        request.finish()


if __name__ == '__main__':
    root = Resource()
    root.putChild('crawl', CrawlerAPI())

    # Define the Site with custom logFormatter
    site = Site(root)
    reactor.listenTCP(SERVICE_PORT, site)
    reactor.run()
