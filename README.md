# REST API overview
This doc describes a couple of changes wich were made to seCrawler.

REST API server was added. Provided by `CrawlerAPI` class it currently
supports only GET request of the following format:

> `http://host:port/crawl?se=google&keyword=hello&pages=10`

Where each parameter is mandatory:

   * keyword - string specifying the keyword to search
   * se - string sepcifying search enginge to use (Currently only 'google' is supported)
   * pages - string specifying max number of pages to crawl

The original `keywordsSpider` was slightly modified:

   * `items = []` field added to store extracted items, so that it would be easily accessed from the runner
   * `_xpath` method was added to simplify xpath extraction from given selector. This should be used in derived classes.

There was `CrawlersManager` class added, which is responsible for dynamic loading
of spiders from spiders directory.

Now adding the extraction of results from a new search engine boils down to
adding `SearchEngines` start url and adding a new spider to spiders directory.

It should be derived from the `keywordsSpider` and it should be named with unique
name, so that it will be referred with from url parameter `se`.

There was a basic test added: `tests.test_basic_workflow` which makes end to end
sunnity check by running `CrawlerAPI.render_GET` with the dummy request and
 by running the a crawler infront of a search engine, and checking first couple
 result (urls).

 Run the test with:

 > `trial tests/test_basic_workflow.py`