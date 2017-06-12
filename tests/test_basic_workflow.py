"""
End to end test. It starts from running the instance of CrawlerAPI service
then passes the dummy request to CrawlerAPI.render_GET and checks that the
request was processed as expected - right results came from the crawler.
WARNING: This test actually access google to get the search results.
"""

import json
from twisted.trial import unittest
from twisted.internet.defer import inlineCallbacks
from twisted.web.test.requesthelper import DummyRequest
from seCrawler.server.main import CrawlerAPI


class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.crawler_api = CrawlerAPI()

    @inlineCallbacks
    def test_work_flow(self):
        # Create a dummy request to google with keyword "recongate"
        request = DummyRequest(["crawl"])
        request.args = {"se": ["google"], "keyword": ["recongate"], "pages": ["1"]}

        # Invoke render_GET with dummy request
        self.crawler_api.render_GET(request)

        # Wait till request is finished
        yield request.notifyFinish()

        # Read the response output (results)
        output = json.loads(request.written[0])
        self.assertEqual(9, len(output["results"]))

        # Remaining code checks we got those 3 urls in among results
        expected_urls = ["http://recongate.com/",
                         "https://www.facebook.com/ReconGate-1367244313333677/"]

        for r in output["results"]:
            url = r["url"]
            if url in expected_urls:
                expected_urls.remove(url)
        self.assertListEqual([], expected_urls)
