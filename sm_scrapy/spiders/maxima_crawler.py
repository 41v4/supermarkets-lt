import json

import scrapy
from scrapy.loader import ItemLoader

from sm_scrapy.items import MaximaHtmlItem


class MaximaCrawler(scrapy.Spider):
    name = "maxima_crawler"
    allowed_domains = ["maxima.lt"]
    start_urls = ["https://www.maxima.lt/akcijos"]
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'CONCURRENT_REQUESTS_PER_IP': 1
    }

    def parse(self, response):
        partial_urls = response.css("div.swiper-slide[data-controller='offerCard']::attr(data-offercard-url-value)").getall()
        for partial_url in partial_urls:
            full_url = response.urljoin(partial_url)
            yield scrapy.Request(
            url=full_url,
            method='POST',
            body=json.dumps({
                'filterData': {
                    'dataSource': None,
                    'includeSubFolders': None,
                    'category': None,
                    'tags': [],
                    'sortBy': None,
                    'sortMethod': None,
                    'presentAs': None,
                    'limitResult': None,
                    'page': 1,
                    'hasNextPage': False,
                    'paginated': False,
                    'categoryRoot': 'MG_root_offers',
                    'categoriesParameter': 'categories',
                    'tagsParameter': 'tags',
                    'audienceTargeting': None,
                    'categories': [],
                    'categoryOperator': None,
                    'tagOperator': None,
                    'types': None,
                    'excluded': [
                        'd1739fb9-2223-4018-a5bc-e8eb7dbd8204',
                    ],
                    'websiteTags': [],
                    'websiteTagsOperator': 'OR',
                    'websiteCategories': [],
                    'websiteCategoriesOperator': 'OR',
                },
            }),
            headers={
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                # 'Accept-Encoding': 'gzip, deflate, br',
                'Content-Type': 'application/json; charset=utf-8',
                'X-Requested-With': 'XMLHttpRequest',
                'Origin': 'https://www.maxima.lt',
                'Alt-Used': 'www.maxima.lt',
                'Connection': 'keep-alive',
                'Referer': 'https://www.maxima.lt/akcijos',
                # 'Cookie': 'CookieConsent={stamp:%27DFVBqJ8vjmfI75gP1I15x9HKgJwaFfuY7hPETvL7hcqzZjeA41Mq7w==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1673284764462%2Cregion:%27lt%27}; MAXIMASESSID=qbo4mulsq3k5s71e6ulticn7pp',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                # Requests doesn't support trailers
                # 'TE': 'trailers',
            },
            callback=self.dump_product_html
        )
    
    def dump_product_html(self, response):
        item_loader = ItemLoader(item=MaximaHtmlItem(), selector=response)
        html = response.text
        item_loader.add_value('html', html)
        yield item_loader.load_item()
        
