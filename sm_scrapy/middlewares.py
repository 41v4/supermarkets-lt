# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class SmScrapySpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class SmScrapyDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        if spider.name == 'maxima_crawler':
            request.headers.update({
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                # 'Accept-Encoding': 'gzip, deflate, br',
                'Alt-Used': 'www.maxima.lt',
                'Connection': 'keep-alive',
                # 'Cookie': 'CookieConsent={stamp:%27DFVBqJ8vjmfI75gP1I15x9HKgJwaFfuY7hPETvL7hcqzZjeA41Mq7w==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1673284764462%2Cregion:%27lt%27}; MAXIMASESSID=f9rttolvvjk33l8l46gurli8dm',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'cross-site',
            })
        elif spider.name == 'iki_spider':
            request.headers['User-Agent'] = 'Custom User-Agent 2'
            # set other headers specific to website2
        elif spider.name == 'lidl_spider':
            request.headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                # 'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Referer': 'https://www.lidl.lt/',
                # 'Cookie': 'CookieConsent={stamp:%27V2Z+AUpettizqW8dACzXz7QZDD1GdKYBRKjMaATk8rSFer1yKLyEkg==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1678363759766%2Cregion:%27lt%27}; ak_bmsc=55EAFB433E7DD07F21624AC00EC8B855~000000000000000000000000000000~YAAQlzQQYMKxl2+HAQAAQ/OtiROMIlw2qc84NbpXSGc+GzevHqFo6GiXbAr/odEDaBTmGtx7pRRwsaps8SqWjiwmdJvCiWgpOdrA3CmJ7mkjBzUvJQ9ZbeeyD5X6Va+DT0ecU1g6AjVyl4jLP6SKbh254+ODQ86E1Xdr8wWSuqq3oJetlnyHAa87DE5KOQj0/InRC2SZKKgX31a6mjBx2DKo8fwxPOnOLd16xEWENVFQxqzKBodKTsiB1HjK2RSef6JliuGoEtCwFyrkuDouupTmS2apD+cztrFpVT42RwxSqqrXtV+R9QvRIMyvXAN0zwTOQjll1NEIH/qEyXjbrsToMrWHX3l6/gWeYjTjunuzhvO9CGHGi3LCsfhlhzThvyLBbGNk1BU=; bm_sv=FF0246770101137D376106071BD86EEA~YAAQlzQQYMaxl2+HAQAAQ/atiRPYnDNaFwnod9BPNQElPMzEUj5DQF7737FNLDdIMbo+EWJe5BxOvqgZDo8CMWxYcl9IJHZQezy8ca43qm2ceHLnpAOx5IolgRo+fv3DA/rPkXShDp0i/dfE+oqvbfbqCjVVlQlhS6lnxDilVddVk4f4YwcJ0oBT0NM4QIZsEb6Lbnt3eFEKnTCXVe85ejFKMdmOI2UeWjXEnhakh/+lYojwLdkkAM52FoY2~1',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-User': '?1',
            }
            # set other headers specific to website3
        elif spider.name == 'rimi_spider':
            request.headers['User-Agent'] = 'Custom User-Agent 4'
            # set other headers specific to website4
        elif spider.name == 'norfa_spider':
            request.headers['User-Agent'] = 'Custom User-Agent 4'
            # set other headers specific to website4

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
