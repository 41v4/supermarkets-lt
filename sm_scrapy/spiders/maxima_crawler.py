import scrapy
from scrapy.loader import ItemLoader

from sm_scrapy.items import MaximaHtmlItem


class MaximaCrawler(scrapy.Spider):
    name = "maxima_crawler"
    allowed_domains = ["maxima.lt"]
    start_urls = ["https://www.maxima.lt/akcijos"]

    def parse(self, response):
        item_loader = ItemLoader(item=MaximaHtmlItem(), selector=response)
        html = response.text
        item_loader.add_value('page_num', "0")
        item_loader.add_value('html', html)
        yield item_loader.load_item()
        
